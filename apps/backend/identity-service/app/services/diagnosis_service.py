"""
Diagnosis service for business logic.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.diagnosis import Diagnosis
from app.services.patient_service import get_patient_by_id
from app.schemas.diagnosis import DiagnosisCreate


async def create_diagnosis(
    db: AsyncSession,
    patient_id: uuid.UUID,
    data: DiagnosisCreate,
    encounter_id: uuid.UUID | None = None,
) -> Diagnosis:
    await get_patient_by_id(db, patient_id)
    diag = Diagnosis(
        patient_id=patient_id,
        encounter_id=encounter_id,
        code=data.code,
        description=data.description,
        clinical_status=data.clinical_status,
        recorded_at=data.recorded_at,
    )
    db.add(diag)
    await db.flush()
    await db.refresh(diag)
    return diag


async def list_diagnoses(
    db: AsyncSession,
    patient_id: uuid.UUID,
) -> list[Diagnosis]:
    await get_patient_by_id(db, patient_id)
    result = await db.execute(
        select(Diagnosis)
        .where(Diagnosis.patient_id == patient_id)
        .order_by(Diagnosis.recorded_at.desc())
    )
    return list(result.scalars().all())
