"""
Observation service for business logic.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.observation import Observation
from app.services.patient_service import get_patient_by_id
from app.schemas.observation import ObservationCreate


async def create_observation(
    db: AsyncSession,
    patient_id: uuid.UUID,
    data: ObservationCreate,
    encounter_id: uuid.UUID | None = None,
) -> Observation:
    await get_patient_by_id(db, patient_id)
    obs = Observation(
        patient_id=patient_id,
        encounter_id=encounter_id,
        category=data.category,
        code=data.code,
        value=data.value,
        unit=data.unit,
        effective_at=data.effective_at,
    )
    db.add(obs)
    await db.flush()
    await db.refresh(obs)
    return obs


async def list_observations(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> list[Observation]:
    await get_patient_by_id(db, patient_id)
    result = await db.execute(
        select(Observation)
        .where(Observation.patient_id == patient_id)
        .order_by(Observation.effective_at.desc())
    )
    return list(result.scalars().all())
