"""
Patient record schemas for request/response validation.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PatientRecordCreate(BaseModel):
    """Schema for creating a new patient record reference."""
    
    record_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Type of medical record",
        examples=["lab", "imaging", "prescription", "note"]
    )
    
    record_ref: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="External reference to EHR/FHIR system",
        examples=["fhir://server.example.com/Observation/12345"]
    )


class PatientRecordRead(BaseModel):
    """Schema for reading patient record data."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(
        ...,
        description="Record's unique identifier"
    )
    
    patient_id: uuid.UUID = Field(
        ...,
        description="Patient's unique identifier"
    )
    
    record_type: str = Field(
        ...,
        description="Type of medical record"
    )
    
    record_ref: str = Field(
        ...,
        description="External reference to EHR/FHIR system"
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp of record creation"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp of last update"
    )
