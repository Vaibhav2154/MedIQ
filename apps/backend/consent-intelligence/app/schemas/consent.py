from pydantic import BaseModel, Field
from typing import List, Optional

class InterpretedConsent(BaseModel):
    allowed_data: List[str] = Field(description="List of medical data categories allowed (e.g., labs, imaging, vitals)")
    denied_data: List[str] = Field(description="List of medical data categories explicitly denied")
    purpose: List[str] = Field(description="List of allowed purposes (e.g., care, research, AI_training)")
    expiry: Optional[str] = Field(None, description="ISO formatting date of consent expiry")
    conditions: List[str] = Field(description="Special conditions like anonymized_only or aggregated_only")
    ambiguity_flags: List[str] = Field(description="List of potential issues like vague_language or conflicting_statements")

class InterpretationRequest(BaseModel):
    consent_id: str
    raw_text: str
    language: str = "en"

class InterpretationResponse(BaseModel):
    consent_id: str
    interpreted: InterpretedConsent
    confidence_score: float
    needs_review: bool
