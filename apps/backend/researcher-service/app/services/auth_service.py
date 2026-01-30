"""
Authentication service for researcher users.
Handles password hashing, JWT token generation, and user authentication.
"""
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.researcher import Researcher
from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # Convert password to bytes and hash it
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_researcher(db: Session, email: str, password: str) -> Optional[Researcher]:
    """
    Authenticate a researcher by email and password.
    
    Args:
        db: Database session
        email: Researcher email
        password: Plain text password
        
    Returns:
        Researcher object if authentication successful, None otherwise
    """
    researcher = db.query(Researcher).filter(Researcher.email == email).first()
    
    if not researcher:
        return None
    
    if not verify_password(password, researcher.hashed_password):
        return None
    
    if not researcher.is_active:
        return None
    
    return researcher


def get_current_researcher(db: Session, token: str) -> Researcher:
    """
    Get the current authenticated researcher from a JWT token.
    
    Args:
        db: Database session
        token: JWT access token
        
    Returns:
        Researcher object
        
    Raises:
        HTTPException: If token is invalid or researcher not found
    """
    payload = decode_access_token(token)
    
    researcher_id: str = payload.get("sub")
    if researcher_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    
    if researcher is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Researcher not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not researcher.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Researcher account is inactive",
        )
    
    return researcher

