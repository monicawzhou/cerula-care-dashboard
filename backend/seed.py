"""
Seed file for populating the database with initial data:
- Patients
- Care team members (3)
- Care team assignments (a few patients assigned to each member)
- Health screenings (one score per patient per month for the last 6 months)

Run this file using: python seed.py
"""

from database import SessionLocal
from models import (
    Patient,
    Gender,
    PatientStatus,
    CareTeamMember,
    CareTeamRole,
    PatientCareTeam,
    HealthScreening,
)
from datetime import datetime, date
import random


# ----------------------------
# Patient data to seed
# ----------------------------
PATIENT_DATA = [
    {
        "first_name": "Alice",
        "last_name": "Johnson",
        "date_of_birth": "1985-04-12",
        "gender": "female",
        "email": "alice.johnson@example.com",
        "status": "active",
    },
    {
        "first_name": "Bob",
        "last_name": "Smith",
        "date_of_birth": "1990-07-23",
        "gender": "male",
        "email": "bob.smith@example.com",
        "status": "inactive",
    },
    {
        "first_name": "Carla",
        "last_name": "Williams",
        "date_of_birth": "1978-11-05",
        "gender": "female",
        "email": "carla.williams@example.com",
        "status": "active",
    },
    {
        "first_name": "David",
        "last_name": "Brown",
        "date_of_birth": "2000-01-19",
        "gender": "male",
        "email": "david.brown@example.com",
        "status": "active",
    },
    {
        "first_name": "Eva",
        "last_name": "Davis",
        "date_of_birth": "1995-09-30",
        "gender": "female",
        "email": "eva.davis@example.com",
        "status": "inactive",
    },
    {
        "first_name": "Frank",
        "last_name": "Miller",
        "date_of_birth": "1982-06-15",
        "gender": "male",
        "email": "frank.miller@example.com",
        "status": "active",
    },
    {
        "first_name": "Grace",
        "last_name": "Wilson",
        "date_of_birth": "1975-03-22",
        "gender": "female",
        "email": "grace.wilson@example.com",
        "status": "inactive",
    },
    {
        "first_name": "Henry",
        "last_name": "Moore",
        "date_of_birth": "1988-12-10",
        "gender": "male",
        "email": "henry.moore@example.com",
        "status": "active",
    },
    {
        "first_name": "Isla",
        "last_name": "Taylor",
        "date_of_birth": "1992-05-17",
        "gender": "female",
        "email": "isla.taylor@example.com",
        "status": "active",
    },
    {
        "first_name": "Jack",
        "last_name": "Anderson",
        "date_of_birth": "1980-08-28",
        "gender": "male",
        "email": "jack.anderson@example.com",
        "status": "inactive",
    },
]

# ----------------------------
# Care team members to seed (exactly 3)
# ----------------------------
CARE_TEAM_DATA = [
    {
        "first_name": "Hannah",
        "last_name": "Coach",
        "role": "health_coach",
        "email": "hannah.coach@cerula.example",
    },
    {
        "first_name": "Ben",
        "last_name": "Bhcm",
        "role": "bhcm",
        "email": "ben.bhcm@cerula.example",
    },
    {
        "first_name": "Priya",
        "last_name": "Psych",
        "role": "psychiatrist",
        "email": "priya.psych@cerula.example",
    },
]


# ----------------------------
# Helpers
# ----------------------------
def first_day_of_month(d: date) -> date:
    return date(d.year, d.month, 1)


def add_months(d: date, delta_months: int) -> date:
    """Return the first day of the month delta_months away from d."""
    y = d.year
    m = d.month + delta_months
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    return date(y, m, 1)


def last_n_month_starts(n: int) -> list[date]:
    """
    Returns a list of month-start dates for the current month and previous n-1 months.
    Sorted ascending.
    """
    anchor = first_day_of_month(date.today())
    months = [add_months(anchor, -i) for i in range(n)]
    return sorted(months)


# ----------------------------
# Seeding functions
# ----------------------------
def seed_patients(db):
    added = 0
    skipped = 0

    for info in PATIENT_DATA:
        existing = db.query(Patient).filter(Patient.email == info["email"]).first()
        if existing:
            skipped += 1
            continue

        dob = datetime.strptime(info["date_of_birth"], "%Y-%m-%d").date()
        gender_enum = Gender[info["gender"]]
        status_enum = PatientStatus[info["status"]]

        patient = Patient(
            first_name=info["first_name"],
            last_name=info["last_name"],
            date_of_birth=dob,
            gender=gender_enum,
            email=info["email"],
            status=status_enum,
        )
        db.add(patient)
        added += 1

    db.commit()
    print(f"✅ Seeded patients (added {added}, skipped {skipped}).")


def seed_care_team_members(db):
    added = 0
    skipped = 0

    for info in CARE_TEAM_DATA:
        existing = db.query(CareTeamMember).filter(CareTeamMember.email == info["email"]).first()
        if existing:
            skipped += 1
            continue

        role_enum = CareTeamRole[info["role"]]
        member = CareTeamMember(
            first_name=info["first_name"],
            last_name=info["last_name"],
            role=role_enum,
            email=info["email"],
        )
        db.add(member)
        added += 1

    db.commit()
    print(f"✅ Seeded care team members (added {added}, skipped {skipped}).")


def seed_care_team_assignments(db):
    """
    Assign a few existing patients to each of the 3 care team members.

    - Coach: first 6 patients
    - BHCM: middle 6 patients
    - Psychiatrist: first 4 patients

    Overlaps are fine; duplicate pairs are skipped.
    """
    patients = db.query(Patient).order_by(Patient.last_name, Patient.first_name).all()
    if not patients:
        print("⚠️  No patients found; skipping care team assignments.")
        return

    coach = db.query(CareTeamMember).filter(CareTeamMember.email == "hannah.coach@cerula.example").first()
    bhcm = db.query(CareTeamMember).filter(CareTeamMember.email == "ben.bhcm@cerula.example").first()
    psych = db.query(CareTeamMember).filter(CareTeamMember.email == "priya.psych@cerula.example").first()

    if not (coach and bhcm and psych):
        print("⚠️  Missing care team members; run seed_care_team_members first.")
        return

    coach_patients = patients[: min(6, len(patients))]
    bhcm_patients = patients[max(0, len(patients) // 2 - 3) : min(len(patients), len(patients) // 2 + 3)]
    psych_patients = patients[: min(4, len(patients))]

    def ensure_assignment(p: Patient, m: CareTeamMember) -> bool:
        existing = (
            db.query(PatientCareTeam)
            .filter(
                PatientCareTeam.patient_id == p.id,
                PatientCareTeam.care_team_member_id == m.id,
            )
            .first()
        )
        if existing:
            return False

        db.add(
            PatientCareTeam(
                patient_id=p.id,
                care_team_member_id=m.id,
            )
        )
        return True

    added = 0
    for p in coach_patients:
        added += 1 if ensure_assignment(p, coach) else 0
    for p in bhcm_patients:
        added += 1 if ensure_assignment(p, bhcm) else 0
    for p in psych_patients:
        added += 1 if ensure_assignment(p, psych) else 0

    db.commit()
    print(f"✅ Seeded care team assignments (added {added}, skipped duplicates).")


def seed_health_screenings(db):
    """
    Create one HealthScreening per patient per month for the past 6 months.

    Uses screening_month as the first day of each month (YYYY-MM-01).
    """
    patients = db.query(Patient).all()
    if not patients:
        print("⚠️  No patients found; skipping health screenings.")
        return

    months = last_n_month_starts(6)

    # Deterministic so reviewers see consistent charts
    random.seed(42)

    added = 0
    skipped = 0

    for patient in patients:
        # Give each patient a baseline + a mild trend so charts look realistic
        baseline = random.randint(2, 8)
        trend = random.choice([-1, 0, 1])  # improving, flat, worsening

        for i, month_start in enumerate(months):
            existing = (
                db.query(HealthScreening)
                .filter(
                    HealthScreening.patient_id == patient.id,
                    HealthScreening.screening_month == month_start,
                )
                .first()
            )
            if existing:
                skipped += 1
                continue

            noise = random.choice([-1, 0, 0, 1])  # mostly stable
            score = baseline + (trend * i) + noise
            score = max(0, min(10, score))

            db.add(
                HealthScreening(
                    patient_id=patient.id,
                    screening_month=month_start,
                    score=score,
                )
            )
            added += 1

    db.commit()
    print(f"✅ Seeded health screenings (added {added}, skipped {skipped}).")


def run_seed():
    db = SessionLocal()
    try:
        seed_patients(db)
        seed_care_team_members(db)
        seed_care_team_assignments(db)
        seed_health_screenings(db)
        print("✨ Seeding complete!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Starting database seeding...")
    run_seed()
