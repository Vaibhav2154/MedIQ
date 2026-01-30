"""
Router for consent-aware data access endpoints.

Integrated with researcher authentication system.
Provides consent-aware query rewriting and policy evaluation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from app.database import get_db
from app.schemas.access_request importCustom SQL with complex joins AccessRequest
from app.services import access_service
from app.utils import token_store
from app.services import audit
from app.utils.dependencies import get_current_researcher
from app.models.researcher import Researcher
from datetime import datetime, timedelta
import uuid
from jose import jwt as jose_jwt
from app.core.config import settings

router = APIRouter(prefix="/router", tags=["consent-aware-data-access"])


@router.post("/access-request")
async def handle_access_request(
    request: AccessRequest,
    current_researcher: Researcher = Depends(get_current_researcher),
    db: Session = Depends(get_db)
) -> dict:
    """
    Consent-Aware Data Access Request Handler.
    
    This endpoint provides advanced consent-aware data access with:
    1. JWT authentication (researcher must be logged in)
    2. Consent policy fetching from database
    3. Policy evaluation against requested fields
    4. SQL query rewriting to filter denied fields
    5. Access token issuance for approved requests
    6. Audit logging
    
    Flow:
    1. Authenticate researcher via JWT
    2. Validate request (purpose, fields, query)
    3. Fetch consent policy for subject
    4. Evaluate policy against requested fields
    5. Rewrite SQL query to include only permitted fields
    6. Issue short-lived access token
    7. Emit audit event
    
    Args:
        request: AccessRequest with subject_id, purpose, requested_fields, query
        current_researcher: Authenticated researcher from JWT token
        db: Database session
    
    Returns:
        dict: Access decision with token and rewritten query
    
    Raises:
        HTTPException: If purpose invalid, consent missing, or access denied
    """
    
    # Validate request
    err = access_service.validate_access_request(request)
    if err:
        raise HTTPException(status_code=400, detail=err)

    # Generate request id
    request_id = str(uuid.uuid4())

    # Convert researcher to user dict for compatibility with existing service
    user = {
        "user_id": current_researcher.id,
        "role": "researcher",
        "org": current_researcher.institution or "unknown"
    }

    # Handle access request via service
    result = access_service.handle_access_request(
        request=request,
        user=user,
        db=db,
        request_id=request_id,
    )

    # Issue short-lived JWT token scoped to permitted fields
    expiry = datetime.utcnow() + timedelta(minutes=15)
    token_payload = {
        "sub": request.subject_id,
        "researcher_id": current_researcher.id,
        "allowed_fields": result.permitted_fields,
        "purpose": request.purpose,
        "request_id": request_id,
        "type": "data_access",
        "exp": int(expiry.timestamp())
    }
    access_token = jose_jwt.encode(token_payload, settings.secret_key, algorithm="HS256")

    # Store token in Redis for revocation tracking
    try:
        token_store.token_store.store_token(
            token=access_token,
            subject_id=request.subject_id,
            purpose=request.purpose,
            allowed_fields=result.permitted_fields,
            request_id=request_id,
        )
    except Exception as e:
        # non-fatal - log but continue
        logging.warning(f"Failed to store token in Redis: {e}")

    # Emit audit event asynchronously
    event = audit.create_access_event(
        user_id=current_researcher.id,
        subject_id=request.subject_id,
        purpose=request.purpose,
        decision=result.decision,
        organization=current_researcher.institution or "unknown",
        request_id=request_id,
        permitted_fields=result.permitted_fields,
        justifications=result.justifications,
    )

    try:
        audit.emit_event_async(event)
    except Exception as e:
        logging.warning(f"Failed to emit audit event: {e}")

    return {
        "request_id": request_id,
        "status": result.decision,
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 15 * 60,
        "permitted_fields": result.permitted_fields,
        "rewritten_query": result.rewritten_query,
        "justifications": result.justifications,
    }


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Consent-Aware Data Router",
        "version": "1.0.0"
    }
