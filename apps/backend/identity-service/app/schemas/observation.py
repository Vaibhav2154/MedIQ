"""
Observation schemas.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ObservationCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=100)
    value: str = Field(..., min_length=1, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    effective_at: datetime = Field(...)


class ObservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: Optional[uuid.UUID]
    category: str
    code: str
    value: str
    unit: Optional[str]
    effective_at: datetime
    created_at: datetime
    updated_at: datetime
