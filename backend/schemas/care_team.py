from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
import uuid


class CareTeamRole(str, Enum):
    health_coach = "health_coach"
    bhcm = "bhcm"
    psychiatrist = "psychiatrist"


class CareTeamMemberResponse(BaseModel):
    """Response model for a care team member."""
    id: uuid.UUID
    first_name: str
    last_name: str
    role: str  # health_coach | bhcm | psychiatrist (from CareTeamRole)
    email: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PatientCareTeamAssignmentResponse(BaseModel):
    """Response model for a patient–care-team assignment."""
    id: uuid.UUID
    patient_id: uuid.UUID
    care_team_member_id: uuid.UUID
    assigned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
