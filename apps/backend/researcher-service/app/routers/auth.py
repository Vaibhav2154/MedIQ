"""
Authentication router for researcher signup and login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.researcher import (
    ResearcherSignup,
    ResearcherLogin,
    ResearcherProfile,
    ResearcherUpdate,
    TokenResponse
)
from app.services import auth_service, researcher_service
from app.core.config import settings
from app.utils.dependencies import get_current_researcher
from app.models.researcher import Researcher


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(
    signup_data: ResearcherSignup,
    db: Session = Depends(get_db)
):
    """
    Register a new researcher account.
    
    Creates a new researcher with the provided information and returns
    an access token for immediate authentication.
    """
    # Create researcher
    researcher = researcher_service.create_researcher(db, signup_data)
    
    # Generate access token
    access_token = auth_service.create_access_token(
        data={"sub": researcher.id, "email": researcher.email, "type": "researcher"}
    )
    
    # Update last login
    researcher_service.update_last_login(db, researcher.id)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        researcher=ResearcherProfile.model_validate(researcher)
    )


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: ResearcherLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate a researcher and return an access token.
    
    Validates credentials and returns a JWT token for API access.
    """
    # Authenticate researcher
    researcher = auth_service.authenticate_researcher(
        db,
        login_data.email,
        login_data.password
    )
    
    if not researcher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token
    access_token = auth_service.create_access_token(
        data={"sub": researcher.id, "email": researcher.email, "type": "researcher"}
    )
    
    # Update last login
    researcher_service.update_last_login(db, researcher.id)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        researcher=ResearcherProfile.model_validate(researcher)
    )


@router.get("/me", response_model=ResearcherProfile)
def get_profile(
    current_researcher: Researcher = Depends(get_current_researcher)
):
    """
    Get the current authenticated researcher's profile.
    
    Requires a valid JWT token in the Authorization header.
    """
    return ResearcherProfile.model_validate(current_researcher)


@router.put("/profile", response_model=ResearcherProfile)
def update_profile(
    update_data: ResearcherUpdate,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
):
    """
    Update the current researcher's profile.
    
    Allows updating profile information like institution, research interests, etc.
    """
    updated_researcher = researcher_service.update_researcher(
        db,
        current_researcher.id,
        update_data
    )
    
    return ResearcherProfile.model_validate(updated_researcher)
