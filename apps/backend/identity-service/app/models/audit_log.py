"""
Audit log model for tracking all create operations.
"""
import uuid
from typing import Optional, Any
from datetime import datetime
from sqlalchemy import String, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AuditLog(Base):
    """
    Audit log for tracking system operations.
    
    Records all create operations with actor information,
    action type, and resource details.
    
    Attributes:
        id: UUID primary key
        actor_id: UUID of the user performing the action (from X-User-Id header)
        action: Action name (e.g., "create_user", "create_patient")
        resource_type: Type of resource (e.g., "user", "patient", "organization")
        resource_id: UUID of the created/modified resource
        timestamp: When the action occurred
        extra_data: Additional JSON metadata about the action
    """
    
    __tablename__ = "audit_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        nullable=True,
        index=True,
        comment="User ID from X-User-Id header"
    )
    
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )
    
    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    
    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        nullable=True,
        index=True
    )
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    
    extra_data: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        comment="Additional metadata about the action"
    )
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource_type}/{self.resource_id})>"
