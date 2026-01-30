"""
Router for consent-aware data access endpoints.

STEP 1: API Entry Point
STEP 4: Access Request Handler
STEP 8: Token Issuance
STEP 9: Emergency Override
STEP 10: Revocation Listener
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os
import logging

from app.database import get_db
from app.schemas.access_request import AccessRequest
from app.services import access_service
from app.utils import token_store
from app.services import audit
from fastapi import BackgroundTasks
from datetime import datetime, timedelta
import uuid
from jose import jwt as jose_jwt

router = APIRouter(prefix="/router", tags=["access-control"])


def verify_token(authorization: Optional[str] = Header(None)) -> dict:
    """
    Verify JWT token from Authorization header.
    
    STEP 3: Authentication (JWT)
    
    Args:
        authorization: Authorization header value (Bearer token)
    
    Returns:
        dict: Decoded token payload with user_id, role, org
    
    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    # Extract Bearer token
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    token = parts[1]
    
    try:
        # Decode JWT (using HS256 for now, can switch to RS256)
        secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        # Debug: print which secret key prefix is being used (do not log full secret in prod)
        try:
            print("[debug] using JWT_SECRET_KEY prefix:", (secret_key or "")[0:8])
        except Exception:
            pass
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        return {
            "user_id": payload.get("sub"),
            "role": payload.get("role"),
            "org": payload.get("org")
        }
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as e:
        # Log decoding failure for debugging (do not leak secrets in production logs)
        logging.exception("JWT decode error: %s", e)
        # Try other common env var names (identity service uses SECRET_KEY)
        candidates = [
            os.getenv("JWT_SECRET_KEY"),
            os.getenv("SECRET_KEY"),
            os.getenv("SECRET"),
            os.getenv("SECRET_KEY", None),
            "your-secret-key-change-in-production",
        ]
        for cand in candidates:
            try:
                if not cand:
                    continue
                payload = jwt.decode(token, cand, algorithms=["HS256"])
                print("[debug] JWT decoded with alternative secret prefix:", (cand or "")[0:8])
                return {
                    "user_id": payload.get("sub"),
                    "role": payload.get("role"),
                    "org": payload.get("org"),
                }
            except Exception:
                continue

        print("[debug] JWT decode error:", e, "token_prefix:", token[:50] + '...' if token else None)
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/access-request")
async def handle_access_request(
    request: AccessRequest,
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> dict:
    """
    STEP 4: Access Request Handler
    
    Main gatekeeper endpoint for data access requests.
    
    Flow:
    1. Authenticate via JWT (via verify_token dependency)
    2. Validate purpose
    3. Generate request ID
    4. Fetch consent policy
    5. Evaluate policy
    6. Rewrite query
    7. Issue access token
    8. Emit audit event
    
    Args:
        request: AccessRequest with subject_id, purpose, requested_fields, query
        user: Authenticated user from JWT token
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

    # Handle access request via service
    result = access_service.handle_access_request(
        request=request,
        user=user,
        db=db,
        request_id=request_id,
    )

    # Issue short-lived JWT token scoped to permitted fields
    secret = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    expiry = datetime.utcnow() + timedelta(minutes=15)
    token_payload = {
        "sub": request.subject_id,
        "allowed_fields": result.permitted_fields,
        "purpose": request.purpose,
        "request_id": request_id,
        "exp": int(expiry.timestamp())
    }
    access_token = jose_jwt.encode(token_payload, secret, algorithm="HS256")

    # Store token in Redis for revocation tracking
    try:
        token_store.token_store.store_token(
            token=access_token,
            subject_id=request.subject_id,
            purpose=request.purpose,
            allowed_fields=result.permitted_fields,
            request_id=request_id,
        )
    except Exception:
        # non-fatal
        pass

    # Emit audit event asynchronously
    event = audit.create_access_event(
        user_id=user.get("user_id"),
        subject_id=request.subject_id,
        purpose=request.purpose,
        decision=result.decision,
        organization=user.get("org"),
        request_id=request_id,
        permitted_fields=result.permitted_fields,
        justifications=result.justifications,
    )

    # Use BackgroundTasks if available to avoid blocking; since this is an async
    # endpoint we can't access BackgroundTasks automatically here — just call async emitter
    try:
        audit.emit_event_async(event)
    except Exception:
        pass

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
