"""
Utility dependencies for FastAPI route handlers.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import auth_service
from app.models.researcher import Researcher


# HTTP Bearer token scheme
security = HTTPBearer()


def get_current_researcher(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Researcher:
    """
    Dependency to get the current authenticated researcher.
    
    Extracts and validates the JWT token from the Authorization header,
    then retrieves the corresponding researcher from the database.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        db: Database session
        
    Returns:
        Authenticated Researcher object
        
    Raises:
        HTTPException: If token is invalid or researcher not found
    """
    token = credentials.credentials
    return auth_service.get_current_researcher(db, token)
