from app.database import SessionLocal, Base, engine
from app.models.consent_policy import ConsentPolicy
from datetime import datetime, timedelta
import uuid

# Create tables
Base.metadata.create_all(bind=engine)

session = SessionLocal()

consent = ConsentPolicy(
    id=str(uuid.uuid4()),
    subject_id="patient-123",
    purpose="RESEARCH",
    policy_json={
        "allowed_fields": ["age", "gender", "medical_history"],
        "denied_fields": ["name", "ssn", "aadhaar"],
        "conditions": {
            "anonymization_required": True,
            "study_id_required": None,
            "aggregation_level": None,
            "max_records": 1000
        }
    },
    confidence_score=0.95,
    expires_at=datetime.utcnow() + timedelta(days=30)
)

session.add(consent)
session.commit()
print("Inserted consent id:", consent.id)
session.close()
