"""
User API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services import user_service, audit_service


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
