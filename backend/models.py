from sqlalchemy import Column, String, Integer, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy import Index, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum
import uuid

# -------------------------------
# ENUM TYPES
# -------------------------------

class PatientStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    discharged = "discharged"


class Gender(enum.Enum):
    female = "female"
    male = "male"
    non_binary = "non_binary"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class CareTeamRole(enum.Enum):
    health_coach = "health_coach"
    bhcm = "bhcm"
    psychiatrist = "psychiatrist"


# -------------------------------
# PATIENTS TABLE
# -------------------------------

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    email = Column(String(255), unique=True)
    status = Column(Enum(PatientStatus), nullable=False, default=PatientStatus.active)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships: many-to-many with care team members
    care_team_members = relationship(
        "CareTeamMember",
        secondary="patient_care_team",
        back_populates="patients",
    )

    # Relationships: one-to-many with health screenings
    health_screenings = relationship(
        "HealthScreening",
        back_populates="patient",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


# -------------------------------
# CARE TEAM MEMBERS TABLE
# -------------------------------

class CareTeamMember(Base):
    __tablename__ = "care_team_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(CareTeamRole), nullable=False)
    email = Column(String(255), unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # Relationships: many-to-many with patients
    patients = relationship(
        "Patient",
        secondary="patient_care_team",
        back_populates="care_team_members",
    )


# -------------------------------
# PATIENT ↔ CARE TEAM (MANY-TO-MANY)
# -------------------------------

class PatientCareTeam(Base):
    __tablename__ = "patient_care_team"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )
    care_team_member_id = Column(
        UUID(as_uuid=True),
        ForeignKey("care_team_members.id", ondelete="CASCADE"),
        nullable=False,
    )
    assigned_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # This matches your SQL schema constraints/indexes
    __table_args__ = (
        UniqueConstraint("patient_id", "care_team_member_id", name="unique_patient_care_team"),
        Index("idx_patient_care_team_patient_id", "patient_id"),
        Index("idx_patient_care_team_member_id", "care_team_member_id"),
    )


# -------------------------------
# HEALTH SCREENINGS (MONTHLY TIME-SERIES DATA)
# -------------------------------

class HealthScreening(Base):
    __tablename__ = "health_screenings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Always store first day of month (YYYY-MM-01)
    screening_month = Column(Date, nullable=False)

    # Score from 0 (best) to 10 (worst)
    score = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("patient_id", "screening_month", name="unique_patient_screening_month"),
        CheckConstraint("score >= 0 AND score <= 10", name="health_screenings_score_range"),
        Index("idx_health_screenings_patient_month", "patient_id", "screening_month"),
    )

    # Relationship back to patient
    patient = relationship("Patient", back_populates="health_screenings")
