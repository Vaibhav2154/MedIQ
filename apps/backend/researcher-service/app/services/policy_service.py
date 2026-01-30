"""
STEP 5: Consent Policy Fetcher Service

Fetch and validate consent policies from database.
Apply confidence gate and time validation.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException

from app.models.consent_policy import ConsentPolicy


def fetch_consent_policy(
    db: Session,
    subject_id: str,
    purpose: str
) -> Dict[str, Any]:
    """
    Fetch and validate consent policy from database.
    
    STEP 5: Consent Policy Fetcher
    
    Queries consent table with:
    - subject_id matches
    - purpose matches
    - expires_at > now (not expired)
    
    Applies confidence gate:
    - confidence_score must be >= 0.85
    
    Args:
        db: SQLAlchemy database session
        subject_id: Patient/subject identifier
        purpose: Purpose of access (RESEARCH, TREATMENT, PUBLIC_HEALTH)
    
    Returns:
        dict: policy_json from ConsentPolicy record
    
    Raises:
        HTTPException: 403 if consent missing, expired, or confidence too low
    """
    
    try:
        now = datetime.utcnow()
        
        # Query consent policy with all conditions
        policy_record = db.query(ConsentPolicy).filter(
            ConsentPolicy.subject_id == subject_id,
            ConsentPolicy.purpose == purpose,
            ConsentPolicy.expires_at > now
        ).first()
        
        # No consent found
        if not policy_record:
            raise HTTPException(
                status_code=403,
                detail=f"No valid consent found for subject {subject_id} with purpose {purpose}"
            )
        
        # Confidence gate (>= 0.85 = 85% confidence)
        if policy_record.confidence_score < 0.85:
            raise HTTPException(
                status_code=403,
                detail=f"Consent confidence too low: {policy_record.confidence_score:.2f} < 0.85"
            )
        
        # Return policy_json only
        return policy_record.policy_json
    
    finally:
        # Ensure DB session is closed safely
        db.close()


def get_consent_policy_safe(
    db: Session,
    subject_id: str,
    purpose: str
) -> Optional[Dict[str, Any]]:
    """
    Fetch consent policy without raising exceptions.
    
    Returns None if not found or confidence too low.
    Useful for non-critical checks.
    
    Args:
        db: SQLAlchemy database session
        subject_id: Patient/subject identifier
        purpose: Purpose of access
    
    Returns:
        dict: policy_json if valid, None otherwise
    """
    
    try:
        now = datetime.utcnow()
        
        policy_record = db.query(ConsentPolicy).filter(
            ConsentPolicy.subject_id == subject_id,
            ConsentPolicy.purpose == purpose,
            ConsentPolicy.expires_at > now
        ).first()
        
        if not policy_record:
            return None
        
        # Confidence gate
        if policy_record.confidence_score < 0.85:
            return None
        
        return policy_record.policy_json
    
    finally:
        db.close()
