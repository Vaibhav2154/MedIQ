"""
User model representing all types of users in the system.
"""
import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class UserRole(str, enum.Enum):
    """User role enumeration."""
    PATIENT = "patient"
    DOCTOR = "doctor"
    HOSPITAL_ADMIN = "hospital_admin"
    RESEARCHER = "researcher"
    REGULATOR = "regulator"


class User(Base, UUIDMixin, TimestampMixin):
    """
    User model for all system users.
    
    Attributes:
        id: UUID primary key
        email: Unique email address
        role: User role (patient, doctor, hospital_admin, researcher, regulator)
        password_hash: Hashed password
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False, length=50),
        nullable=False
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
