"""
Pydantic schemas for data access requests.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DataAccessRequestCreate(BaseModel):
    """Schema for creating a data access request."""
    purpose: str = Field(..., min_length=3, description="Research purpose (e.g., 'diabetes_research')")
    justification: Optional[str] = Field(None, description="Detailed justification for data access")
    requested_fields: List[str] = Field(..., min_items=1, description="List of requested data fields")


class DataAccessRequestResponse(BaseModel):
    """Schema for data access request response."""
    id: str
    researcher_id: str
    purpose: str
    justification: Optional[str]
    requested_fields: List[str]
    status: str
    access_token: Optional[str]
    permitted_fields: Optional[List[str]]
    created_at: datetime
    approved_at: Optional[datetime]
    expires_at: Optional[datetime]
    decision_reason: Optional[str]
    
    class Config:
        from_attributes = True


class ConsentAwareDataQuery(BaseModel):
    """Schema for querying consent-aware data."""
    purpose: str = Field(..., description="Research purpose matching the access request")
    filters: Optional[dict] = Field(None, description="Optional filters for the query")
    limit: int = Field(default=100, ge=1, le=1000)
