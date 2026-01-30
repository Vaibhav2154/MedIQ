"""
Observation API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.observation import ObservationCreate, ObservationRead
from app.services import observation_service, audit_service
from app.services.consent_enforcement_service import enforce_and_log


router = APIRouter(prefix="/patients", tags=["observations"])


@router.post(
    "/{patient_id}/observations",
    response_model=ObservationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an observation",
    description="Create a new observation (lab/vital). Optional encounter linkage via query param."
)
async def create_observation(
    patient_id: uuid.UUID,
    data: ObservationCreate,
    encounter_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> ObservationRead:
    obs = await observation_service.create_observation(db, patient_id, data, encounter_id)
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_observation",
        resource_type="observation",
        resource_id=obs.id,
        actor_id=actor_id,
        extra_data={"patient_id": str(patient_id), "code": obs.code, "value": obs.value},
    )
    await db.commit()
    return ObservationRead.model_validate(obs)


@router.get(
    "/{patient_id}/observations",
    response_model=list[ObservationRead],
    summary="List observations",
    description="List all observations for a patient."
)
async def list_observations(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[ObservationRead]:
    observations = await observation_service.list_observations(db, patient_id)
    return [ObservationRead.model_validate(o) for o in observations]


@router.post(
    "/{patient_id}/observations/enforced",
    response_model=ObservationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an observation with consent enforcement",
    description="Create a new observation only if consent permits the category/purpose."
)
async def create_observation_enforced(
    patient_id: uuid.UUID,
    data: ObservationCreate,
    consent_id: uuid.UUID,
    purpose: str,
    encounter_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id"),
) -> ObservationRead:
    resource, app_log = await enforce_and_log(
        db=db,
        patient_id=patient_id,
        consent_id=consent_id,
        category=data.category,
        purpose=purpose,
        create_fn=observation_service.create_observation,
        create_payload={
            "db": db,
            "patient_id": patient_id,
            "data": data,
            "encounter_id": encounter_id,
        },
        resource_type="observation",
    )
    if resource is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Consent does not permit this observation")

    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_observation_enforced",
        resource_type="observation",
        resource_id=resource.id,
        actor_id=actor_id,
        extra_data={"consent_id": str(consent_id), "purpose": purpose, "policy": app_log.policy_snapshot},
    )
    await db.commit()
    return ObservationRead.model_validate(resource)
