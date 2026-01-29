"""
Organization schemas for request/response validation.
"""
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.enums import OrgType


class OrganizationCreate(BaseModel):
    """Schema for creating a new organization."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Organization name",
        examples=["Apollo Hospital"]
    )
    
    org_type: OrgType = Field(
        ...,
        description="Type of organization"
    )


class OrganizationRead(BaseModel):
    """Schema for reading organization data."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(
        ...,
        description="Organization's unique identifier"
    )
    
    name: str = Field(
        ...,
        description="Organization name"
    )
    
    org_type: OrgType = Field(
        ...,
        description="Organization type"
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp of organization creation"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp of last update"
    )
