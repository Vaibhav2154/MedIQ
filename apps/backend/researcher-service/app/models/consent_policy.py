from sqlalchemy import Column, String, Float, DateTime, JSON
from app.database import Base


class ConsentPolicy(Base):
    """
    Consent Policy ORM Model
    
    Stores consent records with policy definitions.
    Supports FHIR-like consent structure with confidence scoring.
    """
    __tablename__ = "consent_policies"
    
    id = Column(String, primary_key=True, index=True)
    subject_id = Column(String, index=True, nullable=False)
    purpose = Column(String, index=True, nullable=False)
    policy_json = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
