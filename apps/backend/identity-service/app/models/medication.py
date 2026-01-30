"""
Medication model representing medications prescribed or taken by a patient.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Medication(Base, UUIDMixin, TimestampMixin):
    """
    Medication model for prescriptions/medication statements.
    """

    __tablename__ = "medications"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    encounter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("encounters.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    dose: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    unit: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    frequency: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    route: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    start_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    end_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Medication(id={self.id}, patient_id={self.patient_id}, name={self.name})>"
