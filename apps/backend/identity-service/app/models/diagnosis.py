"""
Diagnosis model representing patient conditions identified during care.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Diagnosis(Base, UUIDMixin, TimestampMixin):
    """
    Diagnosis model for patient conditions.
    """

    __tablename__ = "diagnoses"

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

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    clinical_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Diagnosis(id={self.id}, patient_id={self.patient_id}, code={self.code})>"
