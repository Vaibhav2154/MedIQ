"""
Patient service for business logic related to patients.
"""
import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.patient import Patient
from app.schemas.patient import PatientCreate


async def create_patient(
    db: AsyncSession,
    patient_data: PatientCreate
) -> Patient:
    """
    Create a new patient.
    
    Args:
        db: Database session
        patient_data: Patient creation data
        
    Returns:
        Created patient
        
    Raises:
        HTTPException: If ABHA ID already exists
    """
    # Check if ABHA ID already exists (if provided)
    if patient_data.abha_id:
        existing_patient = await get_patient_by_abha_id(db, patient_data.abha_id)
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Patient with ABHA ID {patient_data.abha_id} already exists"
            )
    
    # Create patient
    patient = Patient(
        abha_id=patient_data.abha_id
    )
    
    db.add(patient)
    await db.flush()
    await db.refresh(patient)
    
    return patient


async def get_patient_by_id(
    db: AsyncSession,
    patient_id: uuid.UUID
) -> Patient:
    """
    Get patient by ID.
    
    Args:
        db: Database session
        patient_id: Patient UUID
        
    Returns:
        Patient object
        
    Raises:
        HTTPException: If patient not found
    """
    result = await db.execute(
        select(Patient).where(Patient.id == patient_id)
    )
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )
    
    return patient


async def get_patient_by_abha_id(
    db: AsyncSession,
    abha_id: str
) -> Optional[Patient]:
    """
    Get patient by ABHA ID.
    
    Args:
        db: Database session
        abha_id: ABHA ID
        
    Returns:
        Patient object or None if not found
    """
    result = await db.execute(
        select(Patient).where(Patient.abha_id == abha_id)
    )
    return result.scalar_one_or_none()
