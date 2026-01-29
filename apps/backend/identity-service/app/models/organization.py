"""
Organization model for hospitals, research organizations, and government entities.
"""
import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class OrgType(str, enum.Enum):
    """Organization type enumeration."""
    HOSPITAL = "hospital"
    RESEARCH_ORG = "research_org"
    GOVERNMENT = "government"


class Organization(Base, UUIDMixin, TimestampMixin):
    """
    Organization model.
    
    Attributes:
        id: UUID primary key
        name: Organization name
        org_type: Type of organization (hospital, research_org, government)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "organizations"
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    org_type: Mapped[OrgType] = mapped_column(
        Enum(OrgType, native_enum=False, length=50),
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name={self.name}, type={self.org_type})>"
