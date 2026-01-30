"""
Researcher model - represents researchers who access consent-aware data.
Uses 'researcher_' prefix for table isolation in shared database.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import uuid


class Researcher(Base):
    """
    Researcher user model.
    
    Researchers self-register to access consent-aware patient data
    for research purposes. All researchers have equal access rights,
    controlled by consent policies rather than user roles.
    """
    __tablename__ = "researcher_users"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Authentication
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    
    # Profile information
    full_name = Column(String, nullable=False)
    institution = Column(String, nullable=True)
    research_interests = Column(Text, nullable=True)
    credentials = Column(String, nullable=True)  # e.g., "PhD, MD"
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Researcher(id={self.id}, email={self.email}, name={self.full_name})>"
