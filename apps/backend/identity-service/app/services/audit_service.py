"""
Audit service for logging system operations.
"""
import uuid
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog


async def log_action(
    db: AsyncSession,
    action: str,
    resource_type: str,
    resource_id: Optional[uuid.UUID] = None,
    actor_id: Optional[uuid.UUID] = None,
    extra_data: Optional[dict[str, Any]] = None
) -> AuditLog:
    """
    Create an audit log entry.
    
    Args:
        db: Database session
        action: Action performed (e.g., "create_user")
        resource_type: Type of resource (e.g., "user")
        resource_id: UUID of the affected resource
        actor_id: UUID of the user performing the action
        extra_data: Additional metadata
        
    Returns:
        Created audit log entry
    """
    audit_log = AuditLog(
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        extra_data=extra_data
    )
    
    db.add(audit_log)
    await db.flush()
    
    return audit_log
