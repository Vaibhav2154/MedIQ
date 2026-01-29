from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..db.session import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    abha_id = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())

class Consent(Base):
    __tablename__ = "consents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    source = Column(String)
    status = Column(String, nullable=False)  # active, revoked, expired
    confidence_score = Column(Numeric(3, 2))
    created_at = Column(DateTime, server_default=func.now())

class ConsentVersion(Base):
    __tablename__ = "consent_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consent_id = Column(UUID(as_uuid=True), ForeignKey("consents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    raw_text = Column(String)
    fhir_consent = Column(JSONB, nullable=False)
    extracted_policy = Column(JSONB, nullable=False)
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
