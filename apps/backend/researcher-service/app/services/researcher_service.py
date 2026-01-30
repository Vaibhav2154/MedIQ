"""
Researcher service for profile management.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime

from app.models.researcher import Researcher
from app.schemas.researcher import ResearcherSignup, ResearcherUpdate
from app.services.auth_service import hash_password


def create_researcher(db: Session, signup_data: ResearcherSignup) -> Researcher:
    """
    Create a new researcher account.
    
    Args:
        db: Database session
        signup_data: Researcher signup information
        
    Returns:
        Created Researcher object
        
    Raises:
        HTTPException: If email already exists
    """
    # Check if email already exists
    existing = db.query(Researcher).filter(Researcher.email == signup_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new researcher
    researcher = Researcher(
        email=signup_data.email,
        hashed_password=hash_password(signup_data.password),
        full_name=signup_data.full_name,
        institution=signup_data.institution,
        research_interests=signup_data.research_interests,
        credentials=signup_data.credentials,
        is_active=True,
        is_verified=False  # Can implement email verification later
    )
    
    try:
        db.add(researcher)
        db.commit()
        db.refresh(researcher)
        return researcher
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


def update_researcher(db: Session, researcher_id: str, update_data: ResearcherUpdate) -> Researcher:
    """
    Update researcher profile.
    
    Args:
        db: Database session
        researcher_id: Researcher ID
        update_data: Updated profile data
        
    Returns:
        Updated Researcher object
        
    Raises:
        HTTPException: If researcher not found
    """
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    
    if not researcher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Researcher not found"
        )
    
    # Update only provided fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(researcher, field, value)
    
    db.commit()
    db.refresh(researcher)
    return researcher


def update_last_login(db: Session, researcher_id: str) -> None:
    """
    Update researcher's last login timestamp.
    
    Args:
        db: Database session
        researcher_id: Researcher ID
    """
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    if researcher:
        researcher.last_login = datetime.utcnow()
        db.commit()
