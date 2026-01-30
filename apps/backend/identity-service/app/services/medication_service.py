"""
Medication service for business logic.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medication import Medication
from app.services.patient_service import get_patient_by_id
from app.schemas.medication import MedicationCreate


async def create_medication(
    db: AsyncSession,
    patient_id: uuid.UUID,
    data: MedicationCreate,
    encounter_id: uuid.UUID | None = None,
) -> Medication:
    await get_patient_by_id(db, patient_id)
    med = Medication(
        patient_id=patient_id,
        encounter_id=encounter_id,
        name=data.name,
        dose=data.dose,
        unit=data.unit,
        frequency=data.frequency,
        route=data.route,
        start_at=data.start_at,
        end_at=data.end_at,
    )
    db.add(med)
    await db.flush()
    await db.refresh(med)
    return med


async def list_medications(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> list[Medication]:
    await get_patient_by_id(db, patient_id)
    result = await db.execute(
        select(Medication)
        .where(Medication.patient_id == patient_id)
        .order_by(Medication.created_at.desc())
    )
    return list(result.scalars().all())
