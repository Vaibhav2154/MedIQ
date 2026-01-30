"""
Session Audit Log Model

Tracks all actions performed within a research session.
Provides immutable audit trail for compliance and transparency.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey

from app.database import Base


class SessionAuditLog(Base):
    """
    Session Audit Log Model
    
    Immutable record of all actions performed within a research session.
    Used for compliance, security auditing, and transparency.
    """
    __tablename__ = "session_audit_logs"
    
    # Primary identifiers
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("research_sessions.id"), nullable=False, index=True)
    researcher_id = Column(String, ForeignKey("researcher_users.id"), nullable=False, index=True)
    
    # Action details
    action = Column(String, nullable=False, index=True)  # e.g., "session_created", "data_accessed"
    details = Column(JSON, nullable=True)  # Action-specific details
    
    # Request context
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamp (immutable)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<SessionAuditLog(id={self.id}, action={self.action}, timestamp={self.timestamp})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "researcher_id": self.researcher_id,
            "action": self.action,
            "details": self.details,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
