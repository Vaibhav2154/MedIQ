"""
Session Audit Service

Handles audit logging for research sessions.
Provides immutable audit trail for all session activities.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import Request

from app.models.session_audit_log import SessionAuditLog


class SessionAuditService:
    """Service for managing session audit logs."""
    
    @staticmethod
    def log_action(
        db: Session,
        session_id: str,
        researcher_id: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
    ) -> SessionAuditLog:
        """
        Log an action performed within a session.
        
        Args:
            db: Database session
            session_id: Session ID
            researcher_id: Researcher ID
            action: Action type (e.g., "session_created", "data_accessed")
            details: Action-specific details
            request: FastAPI request object for IP and user agent
            
        Returns:
            Created audit log entry
        """
        # Extract request context if available
        ip_address = None
        user_agent = None
        
        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")
        
        # Create audit log
        audit_log = SessionAuditLog(
            session_id=session_id,
            researcher_id=researcher_id,
            action=action,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        return audit_log
    
    @staticmethod
    def get_session_logs(
        db: Session,
        session_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[SessionAuditLog], int]:
        """
        Get audit logs for a specific session.
        
        Args:
            db: Database session
            session_id: Session ID
            limit: Maximum number of logs to return
            offset: Pagination offset
            
        Returns:
            Tuple of (logs, total_count)
        """
        query = db.query(SessionAuditLog).filter(
            SessionAuditLog.session_id == session_id
        ).order_by(SessionAuditLog.timestamp.desc())
        
        total = query.count()
        logs = query.limit(limit).offset(offset).all()
        
        return logs, total
    
    @staticmethod
    def get_researcher_logs(
        db: Session,
        researcher_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[SessionAuditLog], int]:
        """
        Get all audit logs for a researcher across all sessions.
        
        Args:
            db: Database session
            researcher_id: Researcher ID
            limit: Maximum number of logs to return
            offset: Pagination offset
            
        Returns:
            Tuple of (logs, total_count)
        """
        query = db.query(SessionAuditLog).filter(
            SessionAuditLog.researcher_id == researcher_id
        ).order_by(SessionAuditLog.timestamp.desc())
        
        total = query.count()
        logs = query.limit(limit).offset(offset).all()
        
        return logs, total
