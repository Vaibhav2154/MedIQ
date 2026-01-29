"""
Organization API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.services import organization_service, audit_service


router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post(
    "",
    response_model=OrganizationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new organization",
    description="Create a new organization (hospital, research org, or government entity)."
)
async def create_organization(
    org_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
) -> OrganizationRead:
    """
    Create a new organization.
    
    - **name**: Organization name
    - **org_type**: Type of organization (hospital, research_org, government)
    """
    # Create organization
    organization = await organization_service.create_organization(db, org_data)
    
    # Log action
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_organization",
        resource_type="organization",
        resource_id=organization.id,
        actor_id=actor_id,
        extra_data={"name": organization.name, "org_type": organization.org_type.value}
    )
    
    await db.commit()
    
    return OrganizationRead.model_validate(organization)


@router.get(
    "/{org_id}",
    response_model=OrganizationRead,
    summary="Get organization by ID",
    description="Retrieve an organization by its unique identifier."
)
async def get_organization(
    org_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> OrganizationRead:
    """
    Get organization by ID.
    
    - **org_id**: Organization's unique identifier (UUID)
    """
    organization = await organization_service.get_organization_by_id(db, org_id)
    return OrganizationRead.model_validate(organization)
