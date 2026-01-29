"""
Audit log schemas for response validation.
"""
import uuid
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class AuditLogRead(BaseModel):
    """Schema for reading audit log data."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(
        ...,
        description="Audit log entry unique identifier"
    )
    
    actor_id: Optional[uuid.UUID] = Field(
        None,
        description="ID of user who performed the action"
    )
    
    action: str = Field(
        ...,
        description="Action performed",
        examples=["create_user", "create_patient"]
    )
    
    resource_type: str = Field(
        ...,
        description="Type of resource affected",
        examples=["user", "patient", "organization"]
    )
    
    resource_id: Optional[uuid.UUID] = Field(
        None,
        description="ID of the affected resource"
    )
    
    timestamp: datetime = Field(
        ...,
        description="When the action occurred"
    )
    
    extra_data: Optional[dict[str, Any]] = Field(
        None,
        description="Additional metadata about the action"
    )
