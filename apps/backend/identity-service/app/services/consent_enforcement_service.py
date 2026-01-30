"""
Consent enforcement orchestration for medical data creation.
"""
import uuid
from typing import Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.consent_application import ConsentApplication
from app.services.consent_gate import fetch_consent, evaluate_consent, generate_fhir_consent


async def enforce_and_log(
    db: AsyncSession,
    patient_id: uuid.UUID,
    consent_id: uuid.UUID,
    category: str,
    purpose: str,
    create_fn,
    create_payload,
    resource_type: str,
) -> Tuple[Any, ConsentApplication]:
    """
    Enforce consent, create resource if allowed, and log application.
    """
    consent_payload = await fetch_consent(consent_id)

    allowed, needs_review, interpreted = evaluate_consent(
        consent_payload, patient_id, category=category, purpose=purpose
    )

    # Perform resource creation only if allowed or needs_review but soft-allow? Here we allow only if allowed.
    if not allowed:
        # Create a denial log
        app_log = ConsentApplication(
            patient_id=patient_id,
            consent_id=consent_id,
            resource_type=resource_type,
            resource_id=uuid.uuid4(),  # placeholder when denied
            purpose=purpose,
            allowed=False,
            needs_review=needs_review,
            policy_snapshot=interpreted,
            notes="Creation blocked by consent"
        )
        db.add(app_log)
        await db.flush()
        return None, app_log

    # Create resource via provided function
    resource = await create_fn(**create_payload)

    # Generate FHIR consent snapshot
    consent_conf = (consent_payload.get("consent") or {}).get("confidence_score")
    fhir_obj = await generate_fhir_consent(
        interpreted=interpreted,
        consent_id=consent_id,
        patient_id=patient_id,
        confidence_score=consent_conf,
        needs_review=needs_review,
    )

    # Persist application log
    app_log = ConsentApplication(
        patient_id=patient_id,
        consent_id=consent_id,
        resource_type=resource_type,
        resource_id=getattr(resource, "id"),
        purpose=purpose,
        allowed=True,
        needs_review=needs_review,
        policy_snapshot=interpreted,
        fhir_consent=fhir_obj.get("fhir_consent"),
    )
    db.add(app_log)
    await db.flush()

    return resource, app_log
