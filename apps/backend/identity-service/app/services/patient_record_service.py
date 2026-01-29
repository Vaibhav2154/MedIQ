"""
Patient record service for business logic related to patient records.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.patient_record import PatientRecord
from app.schemas.patient_record import PatientRecordCreate
from app.services.patient_service import get_patient_by_id


async def create_patient_record(
    db: AsyncSession,
    patient_id: uuid.UUID,
    record_data: PatientRecordCreate
) -> PatientRecord:
    """
    Create a new patient record reference.
    
    Args:
        db: Database session
        patient_id: Patient UUID
        record_data: Record creation data
        
    Returns:
        Created patient record
        
    Raises:
        HTTPException: If patient not found
    """
    # Verify patient exists
    await get_patient_by_id(db, patient_id)
    
    # Create record
    record = PatientRecord(
        patient_id=patient_id,
        record_type=record_data.record_type,
        record_ref=record_data.record_ref
    )
    
    db.add(record)
    await db.flush()
    await db.refresh(record)
    
    return record


async def get_patient_records(
    db: AsyncSession,
    patient_id: uuid.UUID
) -> list[PatientRecord]:
    """
    Get all records for a patient.
    
    Args:
        db: Database session
        patient_id: Patient UUID
        
    Returns:
        List of patient records
        
    Raises:
        HTTPException: If patient not found
    """
    # Verify patient exists
    await get_patient_by_id(db, patient_id)
    
    # Get records
    result = await db.execute(
        select(PatientRecord)
        .where(PatientRecord.patient_id == patient_id)
        .order_by(PatientRecord.created_at.desc())
    )
    records = result.scalars().all()
    
    return list(records)
