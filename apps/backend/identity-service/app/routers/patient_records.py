"""
Patient record API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.patient_record import PatientRecordCreate, PatientRecordRead
from app.services import patient_record_service, audit_service


router = APIRouter(prefix="/patients", tags=["patient-records"])


@router.post(
    "/{patient_id}/records",
    response_model=PatientRecordRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a patient record reference",
    description="Link a new medical record reference to a patient."
)
async def create_patient_record(
    patient_id: uuid.UUID,
    record_data: PatientRecordCreate,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
) -> PatientRecordRead:
    """
    Create a patient record reference.
    
    - **patient_id**: Patient's unique identifier (UUID)
    - **record_type**: Type of record (e.g., lab, imaging, prescription)
    - **record_ref**: External reference to EHR/FHIR system
    """
    # Create record
    record = await patient_record_service.create_patient_record(
        db, patient_id, record_data
    )
    
    # Log action
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_patient_record",
        resource_type="patient_record",
        resource_id=record.id,
        actor_id=actor_id,
        extra_data={
            "patient_id": str(patient_id),
            "record_type": record.record_type,
            "record_ref": record.record_ref
        }
    )
    
    await db.commit()
    
    return PatientRecordRead.model_validate(record)


@router.get(
    "/{patient_id}/records",
    response_model=list[PatientRecordRead],
    summary="Get patient records",
    description="Retrieve all record references for a patient."
)
async def get_patient_records(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> list[PatientRecordRead]:
    """
    Get all records for a patient.
    
    - **patient_id**: Patient's unique identifier (UUID)
    
    Returns a list of record references ordered by creation date (newest first).
    """
    records = await patient_record_service.get_patient_records(db, patient_id)
    return [PatientRecordRead.model_validate(record) for record in records]
