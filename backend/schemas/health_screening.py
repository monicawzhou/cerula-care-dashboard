from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel
import uuid


class HealthScreeningResponse(BaseModel):
    """Response model for a single health screening record."""
    id: uuid.UUID
    patient_id: uuid.UUID
    screening_month: date
    score: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
