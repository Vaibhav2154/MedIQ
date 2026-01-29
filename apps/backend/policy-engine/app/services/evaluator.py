from typing import List, Tuple
from ..schemas.request import PolicyRequest, PolicyDecision
from datetime import datetime

def evaluate_policy(request: PolicyRequest) -> PolicyDecision:
    # 1. Confidence check
    if request.confidence < 0.75:
        return PolicyDecision(
            decision="DENY",
            allowed_fields=[],
            denied_fields=request.requested_fields,
            reason="Consent confidence too low for automated decision."
        )

    consent = request.consent
    
    # 2. Purpose binding
    allowed_purposes = [p.lower() for p in consent.get("purpose", [])]
    if request.purpose.lower() not in allowed_purposes:
        return PolicyDecision(
            decision="DENY",
            allowed_fields=[],
            denied_fields=request.requested_fields,
            reason=f"Purpose '{request.purpose}' not authorized by patient."
        )

    # 3. Expiry check
    expiry_str = consent.get("expiry")
    if expiry_str:
        try:
            expiry_date = datetime.fromisoformat(expiry_str)
            if request.request_time > expiry_date:
                return PolicyDecision(
                    decision="DENY",
                    allowed_fields=[],
                    denied_fields=request.requested_fields,
                    reason="Consent has expired."
                )
        except ValueError:
            # If date format is weird, fallback to deny for safety
            return PolicyDecision(
                decision="DENY",
                allowed_fields=[],
                denied_fields=request.requested_fields,
                reason="Invalid consent expiry format."
            )

    # 4. Field-level enforcement
    requested = set(request.requested_fields)
    consent_allowed = set(consent.get("allowed_data", []))
    consent_denied = set(consent.get("denied_data", []))

    final_allowed = requested & consent_allowed
    final_denied = (requested & consent_denied) | (requested - consent_allowed)

    if not final_allowed:
        return PolicyDecision(
            decision="DENY",
            allowed_fields=[],
            denied_fields=list(requested),
            reason="No requested fields are authorized."
        )

    if final_denied:
        return PolicyDecision(
            decision="PARTIAL",
            allowed_fields=list(final_allowed),
            denied_fields=list(final_denied),
            reason="Some requested fields were restricted by consent."
        )

    return PolicyDecision(
        decision="ALLOW",
        allowed_fields=list(final_allowed),
        denied_fields=[],
        reason="Access granted based on valid consent."
    )
