"""
Medication schemas.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MedicationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    dose: Optional[str] = Field(None, max_length=50)
    unit: Optional[str] = Field(None, max_length=20)
    frequency: Optional[str] = Field(None, max_length=50)
    route: Optional[str] = Field(None, max_length=50)
    start_at: Optional[datetime] = Field(None)
    end_at: Optional[datetime] = Field(None)


class MedicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    encounter_id: Optional[uuid.UUID]
    name: str
    dose: Optional[str]
    unit: Optional[str]
    frequency: Optional[str]
    route: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
