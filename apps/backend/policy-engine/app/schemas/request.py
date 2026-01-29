from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class PolicyRequest(BaseModel):
    requester_role: str
    purpose: str
    requested_fields: List[str]
    consent: Dict[str, Any]  # The 'interpreted' object from intelligence service
    confidence: float
    request_time: datetime = Field(default_factory=datetime.now)

class PolicyDecision(BaseModel):
    decision: str  # ALLOW, DENY, PARTIAL
    allowed_fields: List[str]
    denied_fields: List[str]
    reason: str
