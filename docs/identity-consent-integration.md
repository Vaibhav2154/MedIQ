# Identity–Consent Integration and Data Population Guide

This guide documents the consent flow across services, the fixes applied between Identity and Consent modules, and practical methodologies to populate the databases with realistic demo data.

## Big-Picture Flow

- Identity Service: System of record for `users`, `organizations`, `patients`, and full medical data: `encounters`, `observations`, `diagnoses`, `medications`, plus `patient_records` (external references). It does not enforce consent policies; those are evaluated by downstream services.
- Consent Ingestion: Accepts PDF/image consent documents, extracts text, versions the consent, and stores `consents` + `consent_versions`.
- Consent Intelligence: Interprets consent text via LLM, scores confidence, and produces a FHIR `Consent` resource.
- Policy Engine / Researcher Service: Consume identity records + consent interpretations to authorize data sharing for research.

## Fixes Applied

- Removed duplicate `patients` table from Consent Ingestion to avoid schema conflicts and fragmentation.
  - Consent Ingestion now stores `patient_id` (UUID) referencing Identity Service logically, without cross-database foreign keys.
- Consent Ingestion verifies the patient exists in Identity Service before accepting a consent upload.
- Consent Ingestion automatically calls Consent Intelligence to:
  - Interpret raw consent text and compute `confidence_score`.
  - Generate FHIR `Consent` and persist it alongside the `extracted_policy` in `consent_versions`.
  - Update `consents.confidence_score` for quick summary queries.
- Identity Service gains:
  - `GET /api/v1/patients` for listing patients (with `limit`/`offset`).
  - `GET /api/v1/patients/by-abha/{abha_id}` to resolve a patient by ABHA ID.

## Environment Setup

- Identity Service: `.env` must include `DATABASE_URL` pointing to PostgreSQL.
- Consent Ingestion: `.env` must include `DATABASE_URL`, plus optional:
  - `IDENTITY_SERVICE_URL` (default `http://localhost:8000`)
  - `CONSENT_INTELLIGENCE_URL` (default `http://localhost:8001`)
- Consent Intelligence: `.env` must include any model settings (e.g., Gemini) and `DATABASE_URL` only if you plan to persist outputs separately.

## Quick Start Commands

### Run Identity Service

```bash
cd apps/backend/identity-service
uv sync
uv run uvicorn main:app --reload --port 8000
```

### Run Consent Ingestion

```bash
cd apps/backend/consent-ingestion
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### Run Consent Intelligence

```bash
cd apps/backend/consent-intelligence
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Populate Identity Database

1. Create organizations
```bash
curl -X POST http://localhost:8000/api/v1/organizations \
  -H "Content-Type: application/json" \
  -d '{"name": "Apollo Hospital", "org_type": "hospital"}'
```

2. Create users (doctor/researcher/patient regs)
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email": "researcher@example.com", "role": "researcher", "password": "StrongPass123"}'
```

3. Register patients
```bash
curl -X POST http://localhost:8000/api/v1/patients \
  -H "Content-Type: application/json" \
  -d '{"abha_id": "12-3456-7890-1234"}'
```

4. Optional: Resolve by ABHA and list
```bash
curl http://localhost:8000/api/v1/patients/by-abha/12-3456-7890-1234
curl http://localhost:8000/api/v1/patients?limit=100&offset=0
```

5. Add patient record references (EHR/FHIR pointers)
```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_uuid}/records \
  -H "Content-Type: application/json" \
  -d '{"record_type": "lab", "record_ref": "fhir://server.example.com/Observation/12345"}'
```

## Capture and Interpret Consent

1. Upload consent for a patient (PDF/image)
```bash
curl -X POST http://localhost:8002/consents/upload \
  -F "patient_id={patient_uuid}" \
  -F "file=@/path/to/consent.pdf"
```
- Consent Ingestion will:
  - OCR + normalize text
  - Create or version the logical consent (`consents` + `consent_versions`)
  - Call Consent Intelligence to interpret text and generate FHIR
  - Persist `extracted_policy` + `fhir_consent` on the latest version
  - Update `confidence_score` on the consent

2. Fetch consent summary
```bash
curl http://localhost:8002/consents/{consent_uuid}
```

## Data Seeding Methodologies

- Identity-first: Always register patients in Identity Service and use the returned `id` when operating in Consent Ingestion.
- Synthetic records: Use `record_ref` values pointing to mock FHIR endpoints or identifiers to demonstrate linkage without storing PHI if needed, while core medical data lives in Identity.
- Diverse consents: Seed multiple consent documents varying in scope, purpose, and expiry to showcase adaptability.
- Confidence scenarios: Include ambiguous texts to demonstrate `needs_review` behavior.

## Populate Medical Data

Create an encounter:
```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_uuid}/encounters \
  -H "Content-Type: application/json" \
  -d '{
    "encounter_type": "outpatient",
    "reason": "Routine checkup",
    "start_at": "2025-01-01T10:00:00Z"
  }'
```

Create observations:
```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_uuid}/observations \
  -H "Content-Type: application/json" \
  -d '{
    "category": "vitals",
    "code": "heart_rate",
    "value": "72",
    "unit": "bpm",
    "effective_at": "2025-01-01T10:15:00Z"
  }'
```

Create diagnoses:
```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_uuid}/diagnoses \
  -H "Content-Type: application/json" \
  -d '{
    "code": "I10",
    "description": "Essential (primary) hypertension",
    "clinical_status": "active",
    "recorded_at": "2025-01-01T10:30:00Z"
  }'
```

Create medications:
```bash
curl -X POST http://localhost:8000/api/v1/patients/{patient_uuid}/medications \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Amlodipine",
    "dose": "5",
    "unit": "mg",
    "frequency": "once_daily",
    "route": "oral"
  }'
```

## Integration Notes

- No cross-database foreign keys: Services are loosely coupled via IDs to support independent scaling and deployment.
- Audit trails: Identity Service logs create operations for traceability.
- Researcher workflows: The Researcher Service should query Identity for patient lists and Consent Ingestion for latest `extracted_policy`/FHIR to determine eligibility under Policy Engine.

## Next Steps


  ## Consent Enforcement Endpoints

  Enforced creation requires `consent_id` and a `purpose` (e.g., `care`, `research`):

  - Observations:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/patients/{patient_uuid}/observations/enforced?consent_id={consent_uuid}&purpose=research" \
    -H "Content-Type: application/json" \
    -d '{
      "category": "vitals",
      "code": "heart_rate",
      "value": "72",
      "unit": "bpm",
      "effective_at": "2025-01-01T10:15:00Z"
    }'
  ```

  - Diagnoses:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/patients/{patient_uuid}/diagnoses/enforced?consent_id={consent_uuid}&purpose=research" \
    -H "Content-Type: application/json" \
    -d '{
      "code": "I10",
      "description": "Essential (primary) hypertension",
      "clinical_status": "active",
      "recorded_at": "2025-01-01T10:30:00Z"
    }'
  ```

  - Medications:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/patients/{patient_uuid}/medications/enforced?consent_id={consent_uuid}&purpose=research" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Amlodipine",
      "dose": "5",
      "unit": "mg",
      "frequency": "once_daily",
      "route": "oral"
    }'
  ```

  - Encounters:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/patients/{patient_uuid}/encounters/enforced?consent_id={consent_uuid}&purpose=research" \
    -H "Content-Type: application/json" \
    -d '{
      "encounter_type": "outpatient",
      "reason": "Routine checkup",
      "start_at": "2025-01-01T10:00:00Z"
    }'
  ```
- Wire Policy Engine to evaluate `extracted_policy` against requested data categories.
- Add web UI pages to display consent summaries and confidence status per patient.
- Expand seeding scripts for batch generation of patients, records, and consents.
