from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from ..db.session import get_db
from ..models import consent as models
from ..services import ocr, language, versioning

router = APIRouter(prefix="/consents", tags=["consents"])

@router.post("/upload")
async def upload_consent(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Read file
    content = await file.read()
    
    # 2. OCR logic
    if file.content_type == "application/pdf":
        raw_text = ocr.extract_text_from_pdf(content)
    else:
        raw_text = ocr.extract_text_from_image(content)
    
    raw_text = ocr.normalize_text(raw_text)
    
    # 3. Metadata
    lang = language.detect_language(raw_text)
    checksum = versioning.calculate_checksum(raw_text)
    
    # 4. Check if patient exists, if not create (for MVP simplicity)
    patient_uuid = uuid.UUID(patient_id)
    patient = db.query(models.Patient).filter(models.Patient.id == patient_uuid).first()
    if not patient:
        patient = models.Patient(id=patient_uuid)
        db.add(patient)
        db.commit()

    # 5. Versioning logic
    # Find existing active consent for this patient
    existing_consent = db.query(models.Consent).filter(
        models.Consent.patient_id == patient_uuid,
        models.Consent.status == "active"
    ).first()
    
    if existing_consent:
        # Get latest version number
        latest_version = db.query(models.ConsentVersion).filter(
            models.ConsentVersion.consent_id == existing_consent.id
        ).order_by(models.ConsentVersion.version_number.desc()).first()
        
        new_version_num = versioning.get_next_version(latest_version.version_number if latest_version else 0)
        consent_id = existing_consent.id
    else:
        # Create new logical consent
        new_consent = models.Consent(
            patient_id=patient_uuid,
            status="active"
        )
        db.add(new_consent)
        db.commit()
        db.refresh(new_consent)
        consent_id = new_consent.id
        new_version_num = 1

    # 6. Persist version
    new_version = models.ConsentVersion(
        consent_id=consent_id,
        version_number=new_version_num,
        raw_text=raw_text,
        fhir_consent={}, # To be filled by intelligence service
        extracted_policy={} # To be filled by intelligence service
    )
    db.add(new_version)
    db.commit()
    db.refresh(new_version)
    
    return {
        "consent_id": str(consent_id),
        "version": new_version_num,
        "language": lang,
        "raw_text": raw_text,
        "checksum": checksum
    }

@router.get("/{consent_id}")
async def get_consent(consent_id: str, db: Session = Depends(get_db)):
    consent = db.query(models.Consent).filter(models.Consent.id == uuid.UUID(consent_id)).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    
    latest_version = db.query(models.ConsentVersion).filter(
        models.ConsentVersion.consent_id == consent.id
    ).order_by(models.ConsentVersion.version_number.desc()).first()
    
    return {
        "consent": consent,
        "latest_version": latest_version
    }
