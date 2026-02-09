"""
Thin service layer for patient-related database operations.
"""
from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import Patient, HealthScreening, CareTeamMember, PatientCareTeam


def _first_day_of_month(d: date) -> date:
    """Return the first day of the month for a given date."""
    return d.replace(day=1)


def _first_day_n_months_ago(n: int) -> date:
    """Return the first day of the month n months ago from today."""
    today = date.today()
    year = today.year
    month = today.month - n
    while month <= 0:
        month += 12
        year -= 1
    return date(year, month, 1)


def get_patients(db: Session):
    return db.query(Patient).all()


def get_patient_by_id(db: Session, patient_id: UUID):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_email(db: Session, email: str):
    return db.query(Patient).filter(Patient.email == email).first()


def create_patient(db: Session, *, first_name, last_name, date_of_birth=None, gender=None, email=None, status):
    patient = Patient(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        email=email,
        status=status,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update_patient(db: Session, patient: Patient, *, first_name=None, last_name=None, date_of_birth=None, gender=None, email=None, status=None):
    if first_name is not None:
        patient.first_name = first_name
    if last_name is not None:
        patient.last_name = last_name
    if date_of_birth is not None:
        patient.date_of_birth = date_of_birth
    if gender is not None:
        patient.gender = gender
    if email is not None:
        patient.email = email
    if status is not None:
        patient.status = status
    db.commit()
    db.refresh(patient)
    return patient


def get_health_screenings_last_6_months(db: Session, patient_id: UUID):
    start_month = _first_day_n_months_ago(6)
    end_month = _first_day_of_month(date.today())
    return (
        db.query(HealthScreening)
        .filter(
            and_(
                HealthScreening.patient_id == patient_id,
                HealthScreening.screening_month >= start_month,
                HealthScreening.screening_month <= end_month,
            )
        )
        .order_by(HealthScreening.screening_month.asc())
        .all()
    )


def get_care_team_members(db: Session, patient_id: UUID):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        return None
    return list(patient.care_team_members)


def get_all_care_team_members(db: Session):
    return db.query(CareTeamMember).order_by(CareTeamMember.last_name, CareTeamMember.first_name).all()


def get_care_team_member_by_id(db: Session, member_id: UUID):
    return db.query(CareTeamMember).filter(CareTeamMember.id == member_id).first()


def get_existing_assignment(db: Session, patient_id: UUID, care_team_member_id: UUID):
    return (
        db.query(PatientCareTeam)
        .filter(
            and_(
                PatientCareTeam.patient_id == patient_id,
                PatientCareTeam.care_team_member_id == care_team_member_id,
            )
        )
        .first()
    )


def create_care_team_assignment(db: Session, patient_id: UUID, care_team_member_id: UUID):
    assignment = PatientCareTeam(
        patient_id=patient_id,
        care_team_member_id=care_team_member_id,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def delete_care_team_assignment(db: Session, patient_id: UUID, care_team_member_id: UUID):
    assignment = (
        db.query(PatientCareTeam)
        .filter(
            and_(
                PatientCareTeam.patient_id == patient_id,
                PatientCareTeam.care_team_member_id == care_team_member_id,
            )
        )
        .first()
    )
    if assignment is None:
        return False
    db.delete(assignment)
    db.commit()
    return True
