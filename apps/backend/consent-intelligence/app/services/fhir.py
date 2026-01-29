from ..schemas.consent import InterpretedConsent
import uuid
from datetime import datetime

def generate_fhir_consent(interpreted: InterpretedConsent, patient_id: str = None) -> dict:
    """
    Generates a minimal FHIR Consent resource.
    """
    consent_id = str(uuid.uuid4())
    
    fhir_resource = {
        "resourceType": "Consent",
        "id": consent_id,
        "status": "active",
        "scope": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/consentscope",
                "code": "research" if "research" in interpreted.purpose else "patient-privacy"
            }]
        },
        "category": [{
            "coding": [{
                "system": "http://loinc.org",
                "code": "59284-0",
                "display": "Patient Consent"
            }]
        }],
        "patient": {
            "reference": f"Patient/{patient_id}" if patient_id else "Patient/unknown"
        },
        "dateTime": datetime.now().isoformat(),
        "provision": {
            "type": "permit",
            "period": {
                "end": interpreted.expiry
            } if interpreted.expiry else {},
            "purpose": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
                    "code": p.upper()
                } for p in interpreted.purpose
            ],
            "data": [
                {
                    "meaning": "instance",
                    "reference": f"List/{d}"
                } for d in interpreted.allowed_data
            ]
        }
    }
    
    return fhir_resource
