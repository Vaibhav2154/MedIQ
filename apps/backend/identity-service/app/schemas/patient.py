"""
Patient schemas for request/response validation.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PatientCreate(BaseModel):
    """Schema for creating a new patient."""
    
    abha_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Ayushman Bharat Health Account ID",
        examples=["12-3456-7890-1234"]
    )


class PatientRead(BaseModel):
    """Schema for reading patient data."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(
        ...,
        description="Patient's unique identifier"
    )
    
    abha_id: Optional[str] = Field(
        None,
        description="Ayushman Bharat Health Account ID"
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp of patient registration"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp of last update"
    )
