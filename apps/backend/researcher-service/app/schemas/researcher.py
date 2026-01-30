"""
Pydantic schemas for researcher authentication and profile management.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ResearcherSignup(BaseModel):
    """Schema for researcher registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    institution: Optional[str] = None
    research_interests: Optional[str] = None
    credentials: Optional[str] = None


class ResearcherLogin(BaseModel):
    """Schema for researcher login."""
    email: EmailStr
    password: str


class ResearcherProfile(BaseModel):
    """Schema for researcher profile response."""
    id: str
    email: str
    full_name: str
    institution: Optional[str] = None
    research_interests: Optional[str] = None
    credentials: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ResearcherUpdate(BaseModel):
    """Schema for updating researcher profile."""
    full_name: Optional[str] = None
    institution: Optional[str] = None
    research_interests: Optional[str] = None
    credentials: Optional[str] = None


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    researcher: ResearcherProfile
