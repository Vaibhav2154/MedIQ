"""
Patient API endpoints.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.patient import PatientCreate, PatientRead
from app.services import patient_service, audit_service


router = APIRouter(prefix="/patients", tags=["patients"])


@router.post(
    "",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient",
    description="Register a new patient with optional ABHA ID."
)
async def create_patient(
    patient_data: PatientCreate,
    db: AsyncSession = Depends(get_db),
    x_user_id: Optional[str] = Header(None, alias="X-User-Id")
) -> PatientRead:
    """
    Create a new patient.
    
    - **abha_id**: Optional Ayushman Bharat Health Account ID (must be unique if provided)
    """
    # Create patient
    patient = await patient_service.create_patient(db, patient_data)
    
    # Log action
    actor_id = uuid.UUID(x_user_id) if x_user_id else None
    await audit_service.log_action(
        db=db,
        action="create_patient",
        resource_type="patient",
        resource_id=patient.id,
        actor_id=actor_id,
        extra_data={"abha_id": patient.abha_id}
    )
    
    await db.commit()
    
    return PatientRead.model_validate(patient)


@router.get(
    "/{patient_id}",
    response_model=PatientRead,
    summary="Get patient by ID",
    description="Retrieve a patient by their unique identifier."
)
async def get_patient(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> PatientRead:
    """
    Get patient by ID.
    
    - **patient_id**: Patient's unique identifier (UUID)
    """
    patient = await patient_service.get_patient_by_id(db, patient_id)
    return PatientRead.model_validate(patient)
