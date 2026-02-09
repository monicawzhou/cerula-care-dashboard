"""
Patient-related endpoints.
"""
import uuid
from fastapi import APIRouter, status, HTTPException

from deps import db_dependency
from schemas import (
    PatientCreateRequest,
    PatientUpdateRequest,
    HealthScreeningResponse,
    CareTeamMemberResponse,
    PatientCareTeamAssignmentResponse,
)
from services import (
    get_patients,
    get_patient_by_id,
    get_patient_by_email,
    create_patient,
    update_patient,
    get_health_screenings_last_6_months,
    get_care_team_members,
    get_all_care_team_members,
    get_care_team_member_by_id,
    get_existing_assignment,
    create_care_team_assignment,
    delete_care_team_assignment,
)


router = APIRouter()


def _parse_patient_id(patient_id: str):
    try:
        return uuid.UUID(patient_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid patient ID format. Must be a valid UUID.",
        )


def _parse_member_id(care_team_member_id: str):
    try:
        return uuid.UUID(care_team_member_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid care team member ID format. Must be a valid UUID.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return get_patients(db)


@router.get("/patient/{patient_id}", status_code=status.HTTP_200_OK)
async def read_patient(db: db_dependency, patient_id: str):
    patient_uuid = _parse_patient_id(patient_id)
    patient_model = get_patient_by_id(db, patient_uuid)
    if patient_model is not None:
        return patient_model
    raise HTTPException(status_code=404, detail="Patient not found.")


@router.post("/patients", status_code=status.HTTP_201_CREATED)
def create_patient_endpoint(payload: PatientCreateRequest, db: db_dependency):
    if payload.email:
        existing_patient = get_patient_by_email(db, payload.email)
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A patient with this email already exists.",
            )
    return create_patient(
        db,
        first_name=payload.first_name,
        last_name=payload.last_name,
        date_of_birth=payload.date_of_birth,
        gender=payload.gender,
        email=payload.email,
        status=payload.status,
    )


@router.put("/patients/{patient_id}", status_code=status.HTTP_200_OK)
def update_patient_endpoint(patient_id: str, payload: PatientUpdateRequest, db: db_dependency):
    patient_uuid = _parse_patient_id(patient_id)
    patient_model = get_patient_by_id(db, patient_uuid)
    if patient_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )
    if payload.email and payload.email != patient_model.email:
        existing_patient = get_patient_by_email(db, payload.email)
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A patient with this email already exists.",
            )
    return update_patient(
        db,
        patient_model,
        first_name=payload.first_name,
        last_name=payload.last_name,
        date_of_birth=payload.date_of_birth,
        gender=payload.gender,
        email=payload.email,
        status=payload.status,
    )


@router.get(
    "/patients/{patient_id}/health-screening-scores",
    status_code=status.HTTP_200_OK,
    response_model=list[HealthScreeningResponse],
)
def get_patient_health_screening_scores_last_6_months(patient_id: str, db: db_dependency):
    patient_uuid = _parse_patient_id(patient_id)
    patient = get_patient_by_id(db, patient_uuid)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )
    return get_health_screenings_last_6_months(db, patient_uuid)


@router.get("/care-team-members", status_code=status.HTTP_200_OK, response_model=list[CareTeamMemberResponse])
def list_all_care_team_members(db: db_dependency):
    """List all care team members (for assignment dropdowns)."""
    return get_all_care_team_members(db)


@router.get(
    "/patients/{patient_id}/care-team",
    status_code=status.HTTP_200_OK,
    response_model=list[CareTeamMemberResponse],
)
def get_patient_care_team(patient_id: str, db: db_dependency):
    patient_uuid = _parse_patient_id(patient_id)
    members = get_care_team_members(db, patient_uuid)
    if members is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )
    return members


@router.post(
    "/patients/{patient_id}/care-team/{care_team_member_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=PatientCareTeamAssignmentResponse,
)
def assign_care_team_member_to_patient(
    patient_id: str,
    care_team_member_id: str,
    db: db_dependency,
):
    patient_uuid = _parse_patient_id(patient_id)
    member_uuid = _parse_member_id(care_team_member_id)
    if get_patient_by_id(db, patient_uuid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found.",
        )
    if get_care_team_member_by_id(db, member_uuid) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Care team member not found.",
        )
    if get_existing_assignment(db, patient_uuid, member_uuid):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This care team member is already assigned to this patient.",
        )
    return create_care_team_assignment(db, patient_uuid, member_uuid)


@router.delete(
    "/patients/{patient_id}/care-team/{care_team_member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unassign_care_team_member_from_patient(
    patient_id: str,
    care_team_member_id: str,
    db: db_dependency,
):
    patient_uuid = _parse_patient_id(patient_id)
    member_uuid = _parse_member_id(care_team_member_id)
    deleted = delete_care_team_assignment(db, patient_uuid, member_uuid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This care team member is not assigned to this patient.",
        )