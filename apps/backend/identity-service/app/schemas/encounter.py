"""
Encounter schemas.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class EncounterCreate(BaseModel):
    encounter_type: str = Field(..., min_length=1, max_length=50)
    reason: Optional[str] = Field(None, max_length=255)
    organization_id: Optional[uuid.UUID] = Field(None)
    start_at: datetime = Field(...)
    end_at: Optional[datetime] = Field(None)


class EncounterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    organization_id: Optional[uuid.UUID]
    encounter_type: str
    reason: Optional[str]
    start_at: datetime
    end_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
