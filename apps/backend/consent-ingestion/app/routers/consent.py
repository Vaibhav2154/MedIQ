from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import os
import httpx
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
    
    # 2. Extract text based on file type
    if file.content_type == "application/pdf":
        raw_text = ocr.extract_text_from_pdf(content)
    elif file.content_type == "text/plain" or file.filename.endswith('.txt'):
        # Handle plain text files directly
        raw_text = content.decode('utf-8')
    else:
        # Assume image and use OCR
        raw_text = ocr.extract_text_from_image(content)
    
    raw_text = ocr.normalize_text(raw_text)
    
    # 3. Metadata
    lang = language.detect_language(raw_text)
    checksum = versioning.calculate_checksum(raw_text)
    
    # 4. Verify patient exists in identity-service
    patient_uuid = uuid.UUID(patient_id)
    identity_url = os.getenv("IDENTITY_SERVICE_URL", "http://localhost:8000")
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{identity_url}/api/v1/patients/{patient_uuid}")
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Patient not found in identity-service")
        elif resp.status_code >= 500:
            raise HTTPException(status_code=502, detail="Identity-service unavailable")

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

    # 6. Persist version (initial)
    new_version = models.ConsentVersion(
        consent_id=consent_id,
        version_number=new_version_num,
        raw_text=raw_text,
        fhir_consent={},
        extracted_policy={}
    )
    db.add(new_version)
    db.commit()
    db.refresh(new_version)

    # 7. Interpret consent via consent-intelligence and persist results
    intelligence_url = os.getenv("CONSENT_INTELLIGENCE_URL", "http://localhost:8001")
    async with httpx.AsyncClient(timeout=20) as client:
        interp_resp = await client.post(
            f"{intelligence_url}/consents/interpret",
            json={
                "consent_id": str(consent_id),
                "raw_text": raw_text,
                "language": lang,
            },
        )
        if interp_resp.status_code != 200:
            # Return partial success but mark needs_review
            return {
                "consent_id": str(consent_id),
                "version": new_version_num,
                "language": lang,
                "raw_text": raw_text,
                "checksum": checksum,
                "note": "Interpretation failed; review required",
            }
        interp = interp_resp.json()

        # Update confidence score on Consent
        consent_obj = db.query(models.Consent).filter(models.Consent.id == consent_id).first()
        if consent_obj:
            consent_obj.confidence_score = interp.get("confidence_score")
            db.add(consent_obj)
            db.commit()

        # Generate FHIR Consent
        fhir_resp = await client.post(
            f"{intelligence_url}/consents/fhir",
            json=interp,
        )
        fhir_payload = fhir_resp.json() if fhir_resp.status_code == 200 else {"fhir_consent": {}}

    # 8. Persist interpreted policy + FHIR in version
    new_version.extracted_policy = interp.get("interpreted", {}) if 'interp' in locals() else {}
    new_version.fhir_consent = fhir_payload.get("fhir_consent", {})
    db.add(new_version)
    db.commit()
    db.refresh(new_version)

    return {
        "consent_id": str(consent_id),
        "version": new_version_num,
        "language": lang,
        "checksum": checksum,
        "confidence_score": float(consent_obj.confidence_score) if consent_obj and consent_obj.confidence_score is not None else None,
        "needs_review": interp.get("needs_review") if 'interp' in locals() else True,
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
