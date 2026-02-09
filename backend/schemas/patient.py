from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel, Field, EmailStr


class PatientStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    discharged = "discharged"


class Gender(str, Enum):
    female = "female"
    male = "male"
    non_binary = "non_binary"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class PatientCreateRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr] = None
    status: PatientStatus = PatientStatus.active


class PatientUpdateRequest(BaseModel):
    """
    Request model for updating a patient.
    All fields are optional - only provided fields will be updated.
    """
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr] = None
    status: Optional[PatientStatus] = None
