"""
Data Access Request model - tracks researcher data access requests.
"""
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import uuid
import enum


class AccessStatus(str, enum.Enum):
    """Status of a data access request."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


class DataAccessRequest(Base):
    """
    Tracks researcher requests for accessing consent-aware data.
    
    Each request specifies:
    - Research purpose
    - Requested data fields
    - Time-limited access token (when approved)
    """
    __tablename__ = "researcher_data_access_requests"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Researcher reference
    researcher_id = Column(String, nullable=False, index=True)
    
    # Request details
    purpose = Column(String, nullable=False)  # e.g., "diabetes_research", "cancer_study"
    justification = Column(Text, nullable=True)
    requested_fields = Column(JSON, nullable=False)  # List of field names
    
    # Access control
    status = Column(SQLEnum(AccessStatus), default=AccessStatus.PENDING, nullable=False)
    access_token = Column(String, nullable=True)  # JWT token for data access
    permitted_fields = Column(JSON, nullable=True)  # Actual permitted fields after consent filtering
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Audit
    decision_reason = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<DataAccessRequest(id={self.id}, researcher={self.researcher_id}, purpose={self.purpose}, status={self.status})>"
