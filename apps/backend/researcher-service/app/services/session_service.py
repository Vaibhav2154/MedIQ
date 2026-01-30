"""
Session Service

Handles CRUD operations for research sessions.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.research_session import ResearchSession, SessionStatus
from app.schemas.session import SessionCreate, SessionUpdate


class SessionService:
    """Service for managing research sessions."""
    
    @staticmethod
    def create_session(
        db: Session,
        researcher_id: str,
        session_data: SessionCreate
    ) -> ResearchSession:
        """
        Create a new research session.
        
        Args:
            db: Database session
            researcher_id: ID of the researcher creating the session
            session_data: Session creation data
            
        Returns:
            Created research session
        """
        # Create session
        session = ResearchSession(
            researcher_id=researcher_id,
            title=session_data.title,
            purpose=session_data.purpose,
            description=session_data.description,
            institution=session_data.institution,
            irb_approval_number=session_data.irb_approval_number,
            requested_fields=session_data.requested_fields,
            data_scope=session_data.data_scope,
            start_date=session_data.start_date or datetime.utcnow(),
            end_date=session_data.end_date,
            session_metadata=session_data.session_metadata,
            status=SessionStatus.ACTIVE,
            data_access_count="0"
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session
    
    @staticmethod
    def get_session(
        db: Session,
        session_id: str,
        researcher_id: str
    ) -> ResearchSession:
        """
        Get a specific session.
        
        Args:
            db: Database session
            session_id: Session ID
            researcher_id: Researcher ID (for authorization)
            
        Returns:
            Research session
            
        Raises:
            HTTPException: If session not found or unauthorized
        """
        session = db.query(ResearchSession).filter(
            ResearchSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Check authorization
        if session.researcher_id != researcher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this session"
            )
        
        return session
    
    @staticmethod
    def list_sessions(
        db: Session,
        researcher_id: str,
        status_filter: Optional[SessionStatus] = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[ResearchSession], int]:
        """
        List sessions for a researcher.
        
        Args:
            db: Database session
            researcher_id: Researcher ID
            status_filter: Optional status filter
            limit: Maximum number of sessions to return
            offset: Pagination offset
            
        Returns:
            Tuple of (sessions, total_count)
        """
        query = db.query(ResearchSession).filter(
            ResearchSession.researcher_id == researcher_id
        )
        
        if status_filter:
            query = query.filter(ResearchSession.status == status_filter)
        
        query = query.order_by(ResearchSession.created_at.desc())
        
        total = query.count()
        sessions = query.limit(limit).offset(offset).all()
        
        return sessions, total
    
    @staticmethod
    def update_session(
        db: Session,
        session_id: str,
        researcher_id: str,
        update_data: SessionUpdate
    ) -> ResearchSession:
        """
        Update a session.
        
        Args:
            db: Database session
            session_id: Session ID
            researcher_id: Researcher ID (for authorization)
            update_data: Update data
            
        Returns:
            Updated session
            
        Raises:
            HTTPException: If session not found or unauthorized
        """
        session = SessionService.get_session(db, session_id, researcher_id)
        
        # Update fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(session, field, value)
        
        session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(session)
        
        return session
    
    @staticmethod
    def delete_session(
        db: Session,
        session_id: str,
        researcher_id: str
    ) -> ResearchSession:
        """
        Archive a session (soft delete).
        
        Args:
            db: Database session
            session_id: Session ID
            researcher_id: Researcher ID (for authorization)
            
        Returns:
            Archived session
            
        Raises:
            HTTPException: If session not found or unauthorized
        """
        session = SessionService.get_session(db, session_id, researcher_id)
        
        session.status = SessionStatus.ARCHIVED
        session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(session)
        
        return session
    
    @staticmethod
    def increment_access_count(
        db: Session,
        session_id: str
    ) -> None:
        """
        Increment data access count for a session.
        
        Args:
            db: Database session
            session_id: Session ID
        """
        session = db.query(ResearchSession).filter(
            ResearchSession.id == session_id
        ).first()
        
        if session:
            current_count = int(session.data_access_count) if session.data_access_count else 0
            session.data_access_count = str(current_count + 1)
            session.last_accessed_at = datetime.utcnow()
            db.commit()
