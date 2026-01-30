"""
Medication API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.medication import MedicationCreate, MedicationRead
from app.services import medication_service, audit_service
from app.services.consent_enforcement_service import enforce_and_log


router = APIRouter(prefix="/patients", tags=["medications"])


@router.post(
    "/{patient_id}/medications",
    response_model=MedicationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a medication",
    description="Create a new medication record. Optional encounter linkage via query param."
)
async def create_medication(
    patient_id: uuid.UUID,
    data: MedicationCreate,
    encounter_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> MedicationRead:
    med = await medication_service.create_medication(db, patient_id, data, encounter_id)
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_medication",
        resource_type="medication",
        resource_id=med.id,
        actor_id=actor_id,
        extra_data={"patient_id": str(patient_id), "name": med.name},
    )
    await db.commit()
    return MedicationRead.model_validate(med)


@router.get(
    "/{patient_id}/medications",
    response_model=list[MedicationRead],
    summary="List medications",
    description="List all medications for a patient."
)
async def list_medications(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[MedicationRead]:
    meds = await medication_service.list_medications(db, patient_id)
    return [MedicationRead.model_validate(m) for m in meds]


@router.post(
    "/{patient_id}/medications/enforced",
    response_model=MedicationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a medication with consent enforcement",
    description="Create a new medication only if consent permits the category/purpose."
)
async def create_medication_enforced(
    patient_id: uuid.UUID,
    data: MedicationCreate,
    consent_id: uuid.UUID,
    purpose: str,
    encounter_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> MedicationRead:
    resource, app_log = await enforce_and_log(
        db=db,
        patient_id=patient_id,
        consent_id=consent_id,
        category="medications",
        purpose=purpose,
        create_fn=medication_service.create_medication,
        create_payload={
            "db": db,
            "patient_id": patient_id,
            "data": data,
            "encounter_id": encounter_id,
        },
        resource_type="medication",
    )
    if resource is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Consent does not permit this medication")

    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_medication_enforced",
        resource_type="medication",
        resource_id=resource.id,
        actor_id=actor_id,
        extra_data={"consent_id": str(consent_id), "purpose": purpose, "policy": app_log.policy_snapshot},
    )
    await db.commit()
    return MedicationRead.model_validate(resource)
