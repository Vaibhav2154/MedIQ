"""
Encounter model representing patient visits or episodes of care.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Encounter(Base, UUIDMixin, TimestampMixin):
    """
    Encounter model for patient visits.
    """

    __tablename__ = "encounters"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    encounter_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    reason: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Encounter(id={self.id}, patient_id={self.patient_id}, type={self.encounter_type})>"
