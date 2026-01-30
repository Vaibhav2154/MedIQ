"""
User API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.services import user_service, audit_service
from app.services.auth_service import AuthService


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with email, role, and password. Password will be hashed before storage."
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
) -> UserRead:
    """
    Create a new user.
    
    - **email**: Valid email address (must be unique)
    - **role**: User role (patient, doctor, hospital_admin, researcher, regulator)
    - **password**: Password (min 8 characters, will be hashed)
    """
    # Create user
    user = await user_service.create_user(db, user_data)
    
    # Log action
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_user",
        resource_type="user",
        resource_id=user.id,
        actor_id=actor_id,
        extra_data={"email": user.email, "role": user.role.value}
    )
    
    await db.commit()
    
    return UserRead.model_validate(user)


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get user by ID",
    description="Retrieve a user by their unique identifier."
)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> UserRead:
    """
    Get user by ID.
    
    - **user_id**: User's unique identifier (UUID)
    """
    user = await user_service.get_user_by_id(db, user_id)
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate a user and return a JWT access token."
)
async def login(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Authenticate a user and return an access token.
    
    - **email**: User's email address
    - **password**: User's password
    """
    user = await AuthService.authenticate_user(db, user_login.email, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return AuthService.create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role.value})
