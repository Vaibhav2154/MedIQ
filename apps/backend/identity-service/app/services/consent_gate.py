"""
Consent gate service: fetch and evaluate consent policy.
"""
import uuid
from datetime import datetime
from typing import Any, Tuple
import httpx
from fastapi import HTTPException, status
from app.core.config import settings


async def fetch_consent(consent_id: uuid.UUID) -> dict[str, Any]:
    url = f"{settings.consent_ingestion_url}/consents/{consent_id}"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consent not found")
        if resp.status_code >= 500:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Consent service unavailable")
        return resp.json()


def evaluate_consent(
    consent_payload: dict[str, Any],
    patient_id: uuid.UUID,
    category: str,
    purpose: str,
) -> Tuple[bool, bool, dict[str, Any]]:
    """
    Evaluate if the given category/purpose is permitted.

    Returns: (allowed, needs_review, interpreted_policy)
    """
    consent = consent_payload.get("consent") or {}
    latest = consent_payload.get("latest_version") or {}
    interpreted = latest.get("extracted_policy") or {}

    status_val = (consent.get("status") or "active").lower()
    if status_val != "active":
        return False, False, interpreted

    # Patient linkage sanity: best-effort check if present
    # consent-ingestion stores patient_id, but GET returns raw SQLAlchemy objects; ignore strict match here.

    allowed_data = set((interpreted.get("allowed_data") or []))
    denied_data = set((interpreted.get("denied_data") or []))
    purposes = set((interpreted.get("purpose") or []))
    expiry = interpreted.get("expiry")

    now_iso = datetime.utcnow().isoformat()
    is_expired = False
    try:
        if expiry:
            is_expired = datetime.fromisoformat(expiry) < datetime.utcnow()
    except Exception:
        # malformed expiry -> require review
        is_expired = False

    if is_expired:
        return False, True, interpreted

    category_ok = (category in allowed_data) and (category not in denied_data)
    purpose_ok = purpose in purposes

    needs_review_flags = set((interpreted.get("ambiguity_flags") or []))
    needs_review = ("vague_language" in needs_review_flags) or ("conflicting_statements" in needs_review_flags) or (expiry is None)

    allowed = category_ok and purpose_ok
    # If not explicitly allowed but not denied, require review
    if not allowed and category not in denied_data:
        needs_review = True

    return allowed, needs_review, interpreted


async def generate_fhir_consent(interpreted: dict[str, Any], consent_id: uuid.UUID, patient_id: uuid.UUID, confidence_score: float | None, needs_review: bool) -> dict[str, Any]:
    payload = {
        "consent_id": str(consent_id),
        "interpreted": interpreted,
        "confidence_score": confidence_score or 1.0,
        "needs_review": needs_review,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(f"{settings.consent_intelligence_url}/consents/fhir", json=payload)
        if resp.status_code != 200:
            return {"fhir_consent": {}}
        return resp.json()
