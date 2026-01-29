"""
User schemas for request/response validation.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.schemas.enums import UserRole


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["doctor@example.com"]
    )
    
    role: UserRole = Field(
        ...,
        description="User's role in the system"
    )
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password (will be hashed)"
    )


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = Field(
        None,
        description="Updated email address"
    )
    
    role: Optional[UserRole] = Field(
        None,
        description="Updated role"
    )


class UserRead(BaseModel):
    """Schema for reading user data."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(
        ...,
        description="User's unique identifier"
    )
    
    email: EmailStr = Field(
        ...,
        description="User's email address"
    )
    
    role: UserRole = Field(
        ...,
        description="User's role"
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp of user creation"
    )
    
    updated_at: datetime = Field(
        ...,
        description="Timestamp of last update"
    )
