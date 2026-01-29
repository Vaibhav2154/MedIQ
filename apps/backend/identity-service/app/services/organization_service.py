"""
Organization service for business logic related to organizations.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate


async def create_organization(
    db: AsyncSession,
    org_data: OrganizationCreate
) -> Organization:
    """
    Create a new organization.
    
    Args:
        db: Database session
        org_data: Organization creation data
        
    Returns:
        Created organization
    """
    organization = Organization(
        name=org_data.name,
        org_type=org_data.org_type
    )
    
    db.add(organization)
    await db.flush()
    await db.refresh(organization)
    
    return organization


async def get_organization_by_id(
    db: AsyncSession,
    org_id: uuid.UUID
) -> Organization:
    """
    Get organization by ID.
    
    Args:
        db: Database session
        org_id: Organization UUID
        
    Returns:
        Organization object
        
    Raises:
        HTTPException: If organization not found
    """
    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    organization = result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {org_id} not found"
        )
    
    return organization
