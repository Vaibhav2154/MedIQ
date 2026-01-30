"""
Research Session Model

Represents a research session created by a researcher.
Each session has a specific purpose, scope, and timeline.
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Text, DateTime, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class SessionStatus(str, PyEnum):
    """Session status enumeration."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ResearchSession(Base):
    """
    Research Session Model
    
    Represents an isolated research context with specific purpose and scope.
    All data access within a session is tracked and audited.
    """
    __tablename__ = "research_sessions"
    
    # Primary identifiers
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    researcher_id = Column(String, ForeignKey("researcher_users.id"), nullable=False, index=True)
    
    # Session metadata
    title = Column(String, nullable=False)
    purpose = Column(String, nullable=False, index=True)  # e.g., "diabetes_research"
    description = Column(Text, nullable=True)
    institution = Column(String, nullable=True)
    irb_approval_number = Column(String, nullable=True)  # Ethics approval
    
    # Timeline
    start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)  # Expected or actual end date
    
    # Status
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.ACTIVE, nullable=False, index=True)
    
    # Data scope and permissions
    requested_fields = Column(JSON, nullable=False)  # List of fields needed
    data_scope = Column(JSON, nullable=True)  # Filters/constraints on data
    session_metadata = Column(JSON, nullable=True)  # Additional metadata (renamed from metadata)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Statistics (updated by triggers or application logic)
    data_access_count = Column(String, nullable=True, default="0")  # Number of data queries
    last_accessed_at = Column(DateTime, nullable=True)  # Last data access time
    
    def __repr__(self):
        return f"<ResearchSession(id={self.id}, title={self.title}, status={self.status})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "researcher_id": self.researcher_id,
            "title": self.title,
            "purpose": self.purpose,
            "description": self.description,
            "institution": self.institution,
            "irb_approval_number": self.irb_approval_number,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status.value if isinstance(self.status, SessionStatus) else self.status,
            "requested_fields": self.requested_fields,
            "data_scope": self.data_scope,
            "session_metadata": self.session_metadata,
            "data_access_count": int(self.data_access_count) if self.data_access_count else 0,
            "last_accessed_at": self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
