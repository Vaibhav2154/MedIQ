"""
Session Schemas

Pydantic schemas for research session requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    """Session status enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class SessionCreate(BaseModel):
    """Schema for creating a new research session."""
    title: str = Field(..., min_length=3, max_length=200, description="Session title")
    purpose: str = Field(..., min_length=3, max_length=100, description="Research purpose")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed description")
    institution: Optional[str] = Field(None, max_length=200, description="Research institution")
    irb_approval_number: Optional[str] = Field(None, max_length=100, description="IRB/Ethics approval number")
    requested_fields: List[str] = Field(..., min_items=1, description="List of data fields needed")
    data_scope: Optional[Dict[str, Any]] = Field(None, description="Filters/constraints on data")
    start_date: Optional[datetime] = Field(None, description="Session start date")
    end_date: Optional[datetime] = Field(None, description="Expected end date")
    session_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SessionUpdate(BaseModel):
    """Schema for updating an existing session."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[SessionStatus] = None
    end_date: Optional[datetime] = None
    requested_fields: Optional[List[str]] = None
    data_scope: Optional[Dict[str, Any]] = None
    session_metadata: Optional[Dict[str, Any]] = None


class SessionResponse(BaseModel):
    """Schema for session response."""
    id: str
    researcher_id: str
    title: str
    purpose: str
    description: Optional[str]
    institution: Optional[str]
    irb_approval_number: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    status: str
    requested_fields: List[str]
    data_scope: Optional[Dict[str, Any]]
    session_metadata: Optional[Dict[str, Any]]
    data_access_count: int
    last_accessed_at: Optional[str]
    created_at: str
    updated_at: str


class SessionListResponse(BaseModel):
    """Schema for paginated session list."""
    sessions: List[SessionResponse]
    total: int
    limit: int
    offset: int


class AuditLogResponse(BaseModel):
    """Schema for audit log entry."""
    id: str
    session_id: str
    researcher_id: str
    action: str
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    timestamp: str


class AuditLogListResponse(BaseModel):
    """Schema for paginated audit log list."""
    logs: List[AuditLogResponse]
    total: int
    limit: int
    offset: int
