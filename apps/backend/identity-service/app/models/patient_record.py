"""
Patient record model for storing references to external EHR/FHIR records.
"""
import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.patient import Patient


class PatientRecord(Base, UUIDMixin, TimestampMixin):
    """
    Patient record reference model.
    
    This model stores metadata and references to actual medical records
    stored in external EHR/FHIR systems. It does NOT store the actual
    medical data.
    
    Attributes:
        id: UUID primary key
        patient_id: Foreign key to patient
        record_type: Type of record (lab, imaging, prescription, etc.)
        record_ref: External reference/pointer to the actual record
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        patient: Relationship to patient
    """
    
    __tablename__ = "patient_records"
    
    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    record_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    
    record_ref: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="External reference to EHR/FHIR system"
    )
    
    # Relationship to patient
    patient: Mapped["Patient"] = relationship(
        "Patient",
        back_populates="records"
    )
    
    def __repr__(self) -> str:
        return f"<PatientRecord(id={self.id}, patient_id={self.patient_id}, type={self.record_type})>"
