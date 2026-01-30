"""
Diagnosis API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisRead
from app.services import diagnosis_service, audit_service
from app.services.consent_enforcement_service import enforce_and_log


router = APIRouter(prefix="/patients", tags=["diagnoses"])


@router.post(
    "/{patient_id}/diagnoses",
    response_model=DiagnosisRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a diagnosis",
    description="Create a new diagnosis record. Optional encounter linkage via query param."
)
async def create_diagnosis(
    patient_id: uuid.UUID,
    data: DiagnosisCreate,
    encounter_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> DiagnosisRead:
    diag = await diagnosis_service.create_diagnosis(db, patient_id, data, encounter_id)
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_diagnosis",
        resource_type="diagnosis",
        resource_id=diag.id,
        actor_id=actor_id,
        extra_data={"patient_id": str(patient_id), "code": diag.code},
    )
    await db.commit()
    return DiagnosisRead.model_validate(diag)


@router.get(
    "/{patient_id}/diagnoses",
    response_model=list[DiagnosisRead],
    summary="List diagnoses",
    description="List all diagnoses for a patient."
)
async def list_diagnoses(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[DiagnosisRead]:
    diagnoses = await diagnosis_service.list_diagnoses(db, patient_id)
    return [DiagnosisRead.model_validate(d) for d in diagnoses]


@router.post(
    "/{patient_id}/diagnoses/enforced",
    response_model=DiagnosisRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a diagnosis with consent enforcement",
    description="Create a new diagnosis only if consent permits the category/purpose."
)
async def create_diagnosis_enforced(
    patient_id: uuid.UUID,
    data: DiagnosisCreate,
    consent_id: uuid.UUID,
    purpose: str,
    encounter_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> DiagnosisRead:
    resource, app_log = await enforce_and_log(
        db=db,
        patient_id=patient_id,
        consent_id=consent_id,
        category="diagnoses",
        purpose=purpose,
        create_fn=diagnosis_service.create_diagnosis,
        create_payload={
            "db": db,
            "patient_id": patient_id,
            "data": data,
            "encounter_id": encounter_id,
        },
        resource_type="diagnosis",
    )
    if resource is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Consent does not permit this diagnosis")

    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_diagnosis_enforced",
        resource_type="diagnosis",
        resource_id=resource.id,
        actor_id=actor_id,
        extra_data={"consent_id": str(consent_id), "purpose": purpose, "policy": app_log.policy_snapshot},
    )
    await db.commit()
    return DiagnosisRead.model_validate(resource)
