-- =====================================================
-- EXTENSIONS
-- =====================================================

-- Needed for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- DROP TABLES (order matters because of foreign keys)
-- =====================================================

DROP TABLE IF EXISTS health_screenings;
DROP TABLE IF EXISTS patient_care_team;
DROP TABLE IF EXISTS care_team_members;
DROP TABLE IF EXISTS patients;

DROP TYPE IF EXISTS care_team_role;
DROP TYPE IF EXISTS patient_status;
DROP TYPE IF EXISTS gender;

-- =====================================================
-- ENUM TYPES
-- =====================================================

CREATE TYPE patient_status AS ENUM (
    'active',
    'inactive',
    'discharged'
);

CREATE TYPE gender AS ENUM (
    'female',
    'male',
    'non_binary',
    'other',
    'prefer_not_to_say'
);

CREATE TYPE care_team_role AS ENUM (
    'health_coach',
    'bhcm',
    'psychiatrist'
);

-- =====================================================
-- PATIENTS
-- =====================================================

CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,

    date_of_birth DATE,
    gender gender,

    email VARCHAR(255) UNIQUE,
    status patient_status NOT NULL DEFAULT 'active',

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_patients_status ON patients(status);

-- =====================================================
-- CARE TEAM MEMBERS
-- =====================================================

CREATE TABLE care_team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    first_name VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,

    role care_team_role NOT NULL,
    email VARCHAR(255) UNIQUE,

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_care_team_members_role
    ON care_team_members(role);

-- =====================================================
-- PATIENT ↔ CARE TEAM (MANY-TO-MANY)
-- =====================================================

CREATE TABLE patient_care_team (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID NOT NULL
        REFERENCES patients(id)
        ON DELETE CASCADE,

    care_team_member_id UUID NOT NULL
        REFERENCES care_team_members(id)
        ON DELETE CASCADE,

    assigned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

    CONSTRAINT unique_patient_care_team
        UNIQUE (patient_id, care_team_member_id)
);

CREATE INDEX idx_patient_care_team_patient_id
    ON patient_care_team(patient_id);

CREATE INDEX idx_patient_care_team_member_id
    ON patient_care_team(care_team_member_id);

-- =====================================================
-- HEALTH SCREENINGS (MONTHLY TIME-SERIES DATA)
-- =====================================================

CREATE TABLE health_screenings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    patient_id UUID NOT NULL
        REFERENCES patients(id)
        ON DELETE CASCADE,

    -- Always store the first day of the month (YYYY-MM-01)
    screening_month DATE NOT NULL,

    -- Score from 0 (best) to 10 (worst)
    score INT NOT NULL
        CHECK (score BETWEEN 0 AND 10),

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

    -- One screening per patient per month
    CONSTRAINT unique_patient_screening_month
        UNIQUE (patient_id, screening_month)
);

CREATE INDEX idx_health_screenings_patient_month
    ON health_screenings(patient_id, screening_month);
