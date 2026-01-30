"""
Sessions Router

API endpoints for managing research sessions.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.utils.dependencies import get_current_researcher
from app.models.researcher import Researcher
from app.models.research_session import SessionStatus
from app.schemas.session import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionListResponse,
    AuditLogResponse,
    AuditLogListResponse
)
from app.services.session_service import SessionService
from app.services.session_audit_service import SessionAuditService


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    request: Request,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Create a new research session.
    
    A session represents an isolated research context with specific purpose,
    scope, and timeline. All data access within a session is tracked and audited.
    """
    # Create session
    session = SessionService.create_session(
        db=db,
        researcher_id=current_researcher.id,
        session_data=session_data
    )
    
    # Log session creation
    SessionAuditService.log_action(
        db=db,
        session_id=session.id,
        researcher_id=current_researcher.id,
        action="session_created",
        details={
            "title": session.title,
            "purpose": session.purpose,
            "requested_fields": session.requested_fields
        },
        request=request
    )
    
    return SessionResponse(**session.to_dict())


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    status_filter: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    List all sessions for the current researcher.
    
    Supports filtering by status and pagination.
    """
    # Parse status filter
    status_enum = None
    if status_filter:
        try:
            status_enum = SessionStatus(status_filter)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}"
            )
    
    # Get sessions
    sessions, total = SessionService.list_sessions(
        db=db,
        researcher_id=current_researcher.id,
        status_filter=status_enum,
        limit=limit,
        offset=offset
    )
    
    return SessionListResponse(
        sessions=[SessionResponse(**s.to_dict()) for s in sessions],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific session.
    """
    session = SessionService.get_session(
        db=db,
        session_id=session_id,
        researcher_id=current_researcher.id
    )
    
    return SessionResponse(**session.to_dict())


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    update_data: SessionUpdate,
    request: Request,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Update a session's details.
    
    Can update title, description, status, end date, and other metadata.
    """
    # Update session
    session = SessionService.update_session(
        db=db,
        session_id=session_id,
        researcher_id=current_researcher.id,
        update_data=update_data
    )
    
    # Log update
    SessionAuditService.log_action(
        db=db,
        session_id=session.id,
        researcher_id=current_researcher.id,
        action="session_updated",
        details=update_data.dict(exclude_unset=True),
        request=request
    )
    
    return SessionResponse(**session.to_dict())


@router.delete("/{session_id}", response_model=SessionResponse)
async def delete_session(
    session_id: str,
    request: Request,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Archive a session (soft delete).
    
    The session will be marked as archived but data will be retained
    for audit purposes.
    """
    # Archive session
    session = SessionService.delete_session(
        db=db,
        session_id=session_id,
        researcher_id=current_researcher.id
    )
    
    # Log archival
    SessionAuditService.log_action(
        db=db,
        session_id=session.id,
        researcher_id=current_researcher.id,
        action="session_archived",
        details={"reason": "User requested deletion"},
        request=request
    )
    
    return SessionResponse(**session.to_dict())


@router.get("/{session_id}/audit-logs", response_model=AuditLogListResponse)
async def get_session_audit_logs(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Get audit trail for a specific session.
    
    Returns all actions performed within the session in reverse chronological order.
    """
    # Verify session access
    SessionService.get_session(
        db=db,
        session_id=session_id,
        researcher_id=current_researcher.id
    )
    
    # Get audit logs
    logs, total = SessionAuditService.get_session_logs(
        db=db,
        session_id=session_id,
        limit=limit,
        offset=offset
    )
    
    return AuditLogListResponse(
        logs=[AuditLogResponse(**log.to_dict()) for log in logs],
        total=total,
        limit=limit,
        offset=offset
    )
