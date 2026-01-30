"""
Diagnosis schemas.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class DiagnosisCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    clinical_status: str = Field(default="active", min_length=2, max_length=30)
    recorded_at: datetime = Field(...)


class DiagnosisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: Optional[uuid.UUID]
    code: str
    description: Optional[str]
    clinical_status: str
    recorded_at: datetime
    created_at: datetime
    updated_at: datetime
