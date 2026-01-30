"""
STEP 11: Async Audit Emit

Audit event emission without blocking request flow.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import uuid4


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AuditEvent:
    """Structured audit event."""
    
    def __init__(
        self,
        event_type: str,
        user_id: str,
        subject_id: str,
        purpose: str,
        decision: str,
        organization: str,
        request_id: str = None,
        permitted_fields: list = None,
        justifications: list = None
    ):
        """
        Create audit event.
        
        Args:
            event_type: Type of event (ACCESS_REQUESTED, ALLOWED, DENIED, REVOKED)
            user_id: User making request
            subject_id: Subject/patient being accessed
            purpose: Purpose of access
            decision: Decision made (ALLOW, PARTIAL_ALLOW, DENY)
            organization: Organization of user
            request_id: Request ID for tracing
            permitted_fields: Fields that were allowed
            justifications: Reasons for decision
        """
        self.event_id = str(uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.event_type = event_type
        self.user_id = user_id
        self.subject_id = subject_id
        self.purpose = purpose
        self.decision = decision
        self.organization = organization
        self.request_id = request_id
        self.permitted_fields = permitted_fields or []
        self.justifications = justifications or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "subject_id": self.subject_id,
            "purpose": self.purpose,
            "decision": self.decision,
            "organization": self.organization,
            "request_id": self.request_id,
            "permitted_fields": self.permitted_fields,
            "justifications": self.justifications
        }


def emit_event(event: AuditEvent) -> None:
    """
    Emit audit event without blocking request.
    
    STEP 11: Async Audit Emit
    
    For now, prints to stdout.
    Can be extended to send to audit service asynchronously.
    
    Args:
        event: AuditEvent to emit
    """
    
    try:
        # Print to stdout (stdout is non-blocking)
        event_json = json.dumps(event.to_dict(), indent=2)
        print(f"[AUDIT] {event_json}")
        
        # Also log with logger
        logger.info(f"Audit Event: {event.event_type} - {event.decision}")
    
    except Exception as e:
        # Never fail the request due to audit logging
        logger.error(f"Failed to emit audit event: {str(e)}", exc_info=True)


def emit_event_async(event: AuditEvent) -> None:
    """
    Emit audit event asynchronously (via background task).
    
    Use this with FastAPI BackgroundTasks:
        @router.post("/access-request")
        def endpoint(background_tasks: BackgroundTasks):
            background_tasks.add_task(emit_event_async, event)
    
    Args:
        event: AuditEvent to emit
    """
    
    # Simply call emit_event (can be extended for async HTTP calls)
    emit_event(event)


def create_access_event(
    user_id: str,
    subject_id: str,
    purpose: str,
    decision: str,
    organization: str,
    request_id: str = None,
    permitted_fields: list = None,
    justifications: list = None
) -> AuditEvent:
    """
    Create access request audit event.
    
    Args:
        user_id: User making request
        subject_id: Subject being accessed
        purpose: Purpose of access
        decision: Decision (ALLOW, PARTIAL_ALLOW, DENY)
        organization: User's organization
        request_id: Request ID
        permitted_fields: Allowed fields
        justifications: Decision justifications
    
    Returns:
        AuditEvent: Constructed event
    """
    
    return AuditEvent(
        event_type="ACCESS_REQUESTED",
        user_id=user_id,
        subject_id=subject_id,
        purpose=purpose,
        decision=decision,
        organization=organization,
        request_id=request_id,
        permitted_fields=permitted_fields,
        justifications=justifications
    )


def create_revocation_event(
    user_id: str,
    subject_id: str,
    organization: str,
    request_id: str = None
) -> AuditEvent:
    """
    Create token revocation audit event.
    
    Args:
        user_id: User revoking
        subject_id: Subject/consent being revoked
        organization: User's organization
        request_id: Request ID
    
    Returns:
        AuditEvent: Constructed event
    """
    
    return AuditEvent(
        event_type="REVOKED",
        user_id=user_id,
        subject_id=subject_id,
        purpose="N/A",
        decision="REVOKED",
        organization=organization,
        request_id=request_id
    )


def create_emergency_event(
    user_id: str,
    subject_id: str,
    organization: str,
    justification: str,
    request_id: str = None
) -> AuditEvent:
    """
    Create emergency override audit event.
    
    Args:
        user_id: Clinician making override
        subject_id: Patient being accessed
        organization: User's organization
        justification: Reason for override
        request_id: Request ID
    
    Returns:
        AuditEvent: Constructed event
    """
    
    return AuditEvent(
        event_type="EMERGENCY_OVERRIDE",
        user_id=user_id,
        subject_id=subject_id,
        purpose="EMERGENCY_TREATMENT",
        decision="ALLOW",
        organization=organization,
        request_id=request_id,
        justifications=[justification]
    )
