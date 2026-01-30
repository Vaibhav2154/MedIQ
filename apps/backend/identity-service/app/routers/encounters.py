"""
Encounter API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.encounter import EncounterCreate, EncounterRead
from app.services import encounter_service, audit_service
from app.services.consent_enforcement_service import enforce_and_log


router = APIRouter(prefix="/patients", tags=["encounters"])


@router.post(
    "/{patient_id}/encounters",
    response_model=EncounterRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an encounter",
    description="Create a new patient encounter (visit/episode)."
)
async def create_encounter(
    patient_id: uuid.UUID,
    data: EncounterCreate,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> EncounterRead:
    encounter = await encounter_service.create_encounter(db, patient_id, data)
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_encounter",
        resource_type="encounter",
        resource_id=encounter.id,
        actor_id=actor_id,
        extra_data={"patient_id": str(patient_id), "encounter_type": encounter.encounter_type},
    )
    await db.commit()
    return EncounterRead.model_validate(encounter)


@router.get(
    "/{patient_id}/encounters",
    response_model=list[EncounterRead],
    summary="List encounters",
    description="List all encounters for a patient."
)
async def list_encounters(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[EncounterRead]:
    encounters = await encounter_service.list_encounters(db, patient_id)
    return [EncounterRead.model_validate(e) for e in encounters]


@router.post(
    "/{patient_id}/encounters/enforced",
    response_model=EncounterRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an encounter with consent enforcement",
    description="Create a new encounter only if consent permits the purpose."
)
async def create_encounter_enforced(
    patient_id: uuid.UUID,
    data: EncounterCreate,
    consent_id: uuid.UUID,
    purpose: str,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> EncounterRead:
    # Use category 'encounter' for policy matching
    resource, app_log = await enforce_and_log(
        db=db,
        patient_id=patient_id,
        consent_id=consent_id,
        category="encounter",
        purpose=purpose,
        create_fn=encounter_service.create_encounter,
        create_payload={
            "db": db,
            "patient_id": patient_id,
            "data": data,
        },
        resource_type="encounter",
    )
    if resource is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Consent does not permit this encounter")

    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_encounter_enforced",
        resource_type="encounter",
        resource_id=resource.id,
        actor_id=actor_id,
        extra_data={"consent_id": str(consent_id), "purpose": purpose, "policy": app_log.policy_snapshot},
    )
    await db.commit()
    return EncounterRead.model_validate(resource)
