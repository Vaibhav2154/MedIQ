"""
Patient model for patient identity and ABHA ID management.
"""
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.patient_record import PatientRecord


class Patient(Base, UUIDMixin, TimestampMixin):
    """
    Patient model.
    
    Attributes:
        id: UUID primary key
        abha_id: Ayushman Bharat Health Account ID (unique, optional)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        records: Relationship to patient records
    """
    
    __tablename__ = "patients"
    
    abha_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=True
    )
    
    # Relationship to patient records
    records: Mapped[list["PatientRecord"]] = relationship(
        "PatientRecord",
        back_populates="patient",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, abha_id={self.abha_id})>"
