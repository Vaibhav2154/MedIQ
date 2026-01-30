"""
ConsentApplication model logs enforcement decisions applied to medical data.
"""
import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class ConsentApplication(Base):
    """
    Records when a medical resource is created under a specific consent.
    """

    __tablename__ = "consent_applications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    consent_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    purpose: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    allowed: Mapped[bool] = mapped_column(nullable=False)
    needs_review: Mapped[bool] = mapped_column(nullable=False, default=False)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, index=True)
    policy_snapshot: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    fhir_consent: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<ConsentApplication(id={self.id}, consent_id={self.consent_id}, resource={self.resource_type}/{self.resource_id}, allowed={self.allowed})>"
