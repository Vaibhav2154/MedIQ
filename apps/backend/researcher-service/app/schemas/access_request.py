from pydantic import BaseModel
from typing import List, Optional


class AccessRequest(BaseModel):
    """
    Access Request Schema
    
    Represents a request for data access with consent validation.
    """
    subject_id: str
    purpose: str
    requested_fields: List[str]
    study_id: Optional[str] = None
    query: str
    