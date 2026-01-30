"""
Observation model representing clinical measurements or lab results.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Observation(Base, UUIDMixin, TimestampMixin):
    """
    Observation model for labs/vitals measurements.
    """

    __tablename__ = "observations"

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

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    unit: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    effective_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Observation(id={self.id}, patient_id={self.patient_id}, code={self.code}, value={self.value})>"
