"""
Encounter service for business logic.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.encounter import Encounter
from app.services.patient_service import get_patient_by_id
from app.schemas.encounter import EncounterCreate


async def create_encounter(
    db: AsyncSession,
    patient_id: uuid.UUID,
    data: EncounterCreate,
) -> Encounter:
    await get_patient_by_id(db, patient_id)
    encounter = Encounter(
        patient_id=patient_id,
        organization_id=data.organization_id,
        encounter_type=data.encounter_type,
        reason=data.reason,
        start_at=data.start_at,
        end_at=data.end_at,
    )
    db.add(encounter)
    await db.flush()
    await db.refresh(encounter)
    return encounter


async def list_encounters(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> list[Encounter]:
    await get_patient_by_id(db, patient_id)
    result = await db.execute(
        select(Encounter)
        .where(Encounter.patient_id == patient_id)
        .order_by(Encounter.start_at.desc())
    )
    return list(result.scalars().all())
