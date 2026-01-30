"""
Access Service - Orchestrator

Handles the complete access request flow:
1. Fetch consent policy
2. Evaluate policy
3. Deny if decision is DENY
4. Rewrite query
5. Return decision with justifications
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.access_request import AccessRequest
from app.services.policy_service import fetch_consent_policy
from app.services.policy_evaluator import evaluate_policy, PolicyDecision
from app.services.query_rewriter import rewrite_query, validate_query


class AccessRequestResult:
    """Result of access request handling."""
    
    def __init__(
        self,
        decision: str,
        permitted_fields: list,
        rewritten_query: str,
        justifications: list,
        request_id: str = None
    ):
        self.decision = decision
        self.permitted_fields = permitted_fields
        self.rewritten_query = rewritten_query
        self.justifications = justifications
        self.request_id = request_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to response dictionary."""
        return {
            "decision": self.decision,
            "permitted_fields": self.permitted_fields,
            "rewritten_query": self.rewritten_query,
            "justifications": self.justifications,
            "request_id": self.request_id
        }


def handle_access_request(
    request: AccessRequest,
    user: Dict[str, Any],
    db: Session,
    request_id: str = None
) -> AccessRequestResult:
    """
    Handle access request with full consent workflow.
    
    STEP 4: Access Request Handler
    
    Complete flow:
    1. Fetch consent policy from database
    2. Evaluate policy against requested fields
    3. Check decision - DENY = error
    4. Rewrite query to include only permitted fields
    5. Return decision with rewritten query and justifications
    
    Args:
        request: AccessRequest with subject_id, purpose, requested_fields, query
        user: Authenticated user dict (user_id, role, org)
        db: SQLAlchemy database session
        request_id: Request ID for tracing
    
    Returns:
        AccessRequestResult: decision, permitted_fields, rewritten_query, justifications
    
    Raises:
        HTTPException: If consent missing, confidence low, or policy denies access
    """
    
    # STEP 1: Fetch Consent Policy
    try:
        policy = fetch_consent_policy(
            db=db,
            subject_id=request.subject_id,
            purpose=request.purpose
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch consent policy: {str(e)}"
        )
    
    # STEP 2: Evaluate Policy
    try:
        policy_decision: PolicyDecision = evaluate_policy(
            policy=policy,
            requested_fields=request.requested_fields
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to evaluate policy: {str(e)}"
        )
    
    # STEP 3: Check Decision - DENY
    if policy_decision.decision == "DENY":
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: {'; '.join(policy_decision.justifications)}"
        )
    
    # STEP 4: Rewrite Query
    rewritten_query = None
    try:
        # Validate query is SELECT statement
        if not validate_query(request.query):
            raise ValueError("Query must be a SELECT statement")
        
        # Rewrite query to include only permitted fields
        rewritten_query = rewrite_query(
            original_sql=request.query,
            allowed_fields=policy_decision.permitted_fields
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid query: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to rewrite query: {str(e)}"
        )
    
    # STEP 5: Return Decision with Rewritten Query
    return AccessRequestResult(
        decision=policy_decision.decision,
        permitted_fields=policy_decision.permitted_fields,
        rewritten_query=rewritten_query,
        justifications=policy_decision.justifications,
        request_id=request_id
    )


def validate_access_request(request: AccessRequest) -> Optional[str]:
    """
    Validate access request before processing.
    
    Args:
        request: AccessRequest to validate
    
    Returns:
        str: Error message if invalid, None if valid
    """
    
    # Check required fields
    if not request.subject_id:
        return "subject_id is required"
    
    if not request.purpose:
        return "purpose is required"
    
    if not request.requested_fields:
        return "requested_fields cannot be empty"
    
    if not request.query:
        return "query is required"
    
    # Check query is SELECT
    if not validate_query(request.query):
        return "query must be a SELECT statement"
    
    # Check for valid purpose values
    valid_purposes = {"RESEARCH", "TREATMENT", "PUBLIC_HEALTH"}
    if request.purpose.upper() not in valid_purposes:
        return f"purpose must be one of: {', '.join(valid_purposes)}"
    
    return None


def check_permission(
    user: Dict[str, Any],
    required_role: str = None
) -> bool:
    """
    Check if user has permission for access.
    
    Args:
        user: User dict with role
        required_role: Required role (optional)
    
    Returns:
        bool: True if authorized
    """
    
    if required_role and user.get("role") != required_role:
        return False
    
    return True
