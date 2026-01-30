# MedIQ Consent Services Architecture Guide

## Overview

Your MedIQ platform has **3 microservices** working together to handle the complete consent lifecycle:

1. **Consent Ingestion Service** - Captures and stores consent documents
2. **Consent Intelligence Service** - Interprets consent using AI
3. **Policy Engine Service** - Evaluates access requests against consent policies

## Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Flow                                │
└─────────────────────────────────────────────────────────────────┘

1. Patient uploads consent form (PDF/Image)
                    ↓
   ┌────────────────────────────────┐
   │  Consent Ingestion Service     │
   │  - OCR extraction              │
   │  - Language detection          │
   │  - Version management          │
   │  - Store raw text              │
   └────────────────┬───────────────┘
                    ↓
        Sends raw_text to Intelligence
                    ↓
   ┌────────────────────────────────┐
   │  Consent Intelligence Service  │
   │  - LLM interpretation (Gemini) │
   │  - Extract structured policy   │
   │  - Confidence scoring          │
   │  - Generate FHIR Consent       │
   └────────────────┬───────────────┘
                    ↓
        Returns interpreted policy
                    ↓
   ┌────────────────────────────────┐
   │  Policy Engine Service         │
   │  - Evaluate access requests    │
   │  - Match against consent       │
   │  - Return allow/deny decision  │
   └────────────────────────────────┘
```

---

## 1. Consent Ingestion Service

**Purpose**: First point of contact for consent documents. Handles OCR, versioning, and storage.

### Key Features
- **OCR Processing**: Extracts text from PDF/images
- **Language Detection**: Identifies document language
- **Version Management**: Tracks consent updates over time
- **Checksum Verification**: Ensures document integrity

### API Endpoints

#### Upload Consent
```http
POST /consents/upload
Content-Type: multipart/form-data

Parameters:
- patient_id: UUID (from Identity Service)
- file: PDF or Image file

Response:
{
  "consent_id": "uuid",
  "version": 1,
  "language": "en",
  "raw_text": "extracted text...",
  "checksum": "sha256..."
}
```

#### Get Consent
```http
GET /consents/{consent_id}

Response:
{
  "consent": {...},
  "latest_version": {...}
}
```

### Database Schema
```sql
-- Logical consent entity
CREATE TABLE consents (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL,
    status VARCHAR(20) -- 'active', 'revoked', 'expired'
);

-- Version history
CREATE TABLE consent_versions (
    id UUID PRIMARY KEY,
    consent_id UUID REFERENCES consents(id),
    version_number INTEGER,
    raw_text TEXT,
    fhir_consent JSONB,
    extracted_policy JSONB,
    created_at TIMESTAMP
);
```

---

## 2. Consent Intelligence Service

**Purpose**: AI-powered interpretation of consent text into structured policies.

### Key Features
- **LLM Interpretation**: Uses Google Gemini to understand consent
- **Confidence Scoring**: Determines if human review is needed
- **FHIR Generation**: Creates standard FHIR Consent resources
- **Policy Extraction**: Converts natural language to structured rules

### API Endpoints

#### Interpret Consent
```http
POST /consents/interpret

Body:
{
  "consent_id": "uuid",
  "raw_text": "I consent to share my lab results..."
}

Response:
{
  "consent_id": "uuid",
  "interpreted": {
    "allowed_data_types": ["lab_results", "prescriptions"],
    "allowed_purposes": ["research"],
    "allowed_recipients": ["research_org_123"],
    "restrictions": {...}
  },
  "confidence_score": 0.92,
  "needs_review": false
}
```

#### Generate FHIR
```http
POST /consents/fhir

Body:
{
  "interpreted": {...},
  "patient_id": "uuid"
}

Response:
{
  "fhir_consent": {
    "resourceType": "Consent",
    "status": "active",
    ...
  }
}
```

### LLM Interpretation Logic
The Gemini service extracts:
- **Data Types**: What medical data can be shared
- **Purposes**: Why data can be used (research, treatment, etc.)
- **Recipients**: Who can access the data
- **Time Restrictions**: Validity period
- **Conditions**: Special requirements or limitations

---

## 3. Policy Engine Service

**Purpose**: Real-time evaluation of data access requests against consent policies.

### Key Features
- **Policy Matching**: Compares request against consent rules
- **Decision Making**: Returns allow/deny with reasoning
- **Audit Trail**: Logs all evaluation decisions

### API Endpoints

#### Evaluate Access Request
```http
POST /policy/evaluate

Body:
{
  "patient_id": "uuid",
  "requester_id": "uuid",
  "requester_role": "researcher",
  "requested_data_types": ["lab_results"],
  "purpose": "research",
  "research_study_id": "study_123"
}

Response:
{
  "decision": "allow",  // or "deny"
  "reason": "Consent permits lab results for research purposes",
  "consent_id": "uuid",
  "evaluated_at": "2026-01-29T16:38:00Z"
}
```

### Evaluation Logic
```python
# Pseudocode from evaluator.py
def evaluate_policy(request):
    # 1. Fetch patient's active consent
    consent = get_active_consent(request.patient_id)
    
    # 2. Check data types
    if not all_data_types_allowed(request.requested_data_types, consent):
        return deny("Data type not permitted")
    
    # 3. Check purpose
    if request.purpose not in consent.allowed_purposes:
        return deny("Purpose not permitted")
    
    # 4. Check recipient
    if not is_recipient_allowed(request.requester_id, consent):
        return deny("Recipient not authorized")
    
    # 5. Check time validity
    if consent_expired(consent):
        return deny("Consent has expired")
    
    return allow("All conditions met")
```

---

## Integration Flow

### Complete Workflow Example

**Scenario**: Patient uploads consent, researcher requests data

#### Step 1: Patient Uploads Consent
```bash
# Frontend calls Ingestion Service
curl -X POST http://localhost:8001/consents/upload \
  -F "patient_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "file=@consent_form.pdf"

# Response
{
  "consent_id": "abc-123",
  "version": 1,
  "raw_text": "I consent to share my lab results for research..."
}
```

#### Step 2: Ingestion → Intelligence (Backend call)
```python
# Ingestion service calls Intelligence service
response = requests.post(
    "http://localhost:8002/consents/interpret",
    json={
        "consent_id": "abc-123",
        "raw_text": "I consent to share my lab results for research..."
    }
)

interpreted = response.json()
# {
#   "interpreted": {
#     "allowed_data_types": ["lab_results"],
#     "allowed_purposes": ["research"],
#     ...
#   },
#   "confidence_score": 0.95
# }

# Update consent_version with interpreted policy
db.update(consent_version, 
    extracted_policy=interpreted["interpreted"],
    fhir_consent=fhir_resource
)
```

#### Step 3: Researcher Requests Data
```bash
# API Gateway calls Policy Engine
curl -X POST http://localhost:8003/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "requester_id": "researcher-uuid",
    "requested_data_types": ["lab_results"],
    "purpose": "research"
  }'

# Response
{
  "decision": "allow",
  "reason": "Consent permits lab results for research",
  "consent_id": "abc-123"
}
```

---

## Service Communication

### Option 1: Synchronous (Current)
```
Ingestion → Intelligence → Update DB
```
- Simple, immediate
- Blocks upload until interpretation complete
- Good for MVP

### Option 2: Asynchronous (Production)
```
Ingestion → Queue → Intelligence Worker → Update DB
```
- Non-blocking uploads
- Better scalability
- Requires message queue (RabbitMQ, Kafka)

---

## Port Configuration

Recommended port assignments:
- **Identity Service**: `8000`
- **Consent Ingestion**: `8001`
- **Consent Intelligence**: `8002`
- **Policy Engine**: `8003`
- **API Gateway**: `8080`

---

## Environment Setup

### 1. Consent Ingestion Service
```bash
cd apps/backend/consent-ingestion
cp .env.example .env
# Edit .env with database URL
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### 2. Consent Intelligence Service
```bash
cd apps/backend/consent-intelligence
cp .env.example .env
# Add GEMINI_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### 3. Policy Engine Service
```bash
cd apps/backend/policy-engine
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

---

## API Gateway Integration

The API Gateway should route requests:

```nginx
# Consent upload
POST /api/consents/upload → consent-ingestion:8001

# Consent retrieval
GET /api/consents/{id} → consent-ingestion:8001

# Policy evaluation (called by data services)
POST /api/policy/evaluate → policy-engine:8003
```

---

## Key Design Decisions

### 1. **Separation of Concerns**
- **Ingestion**: Document processing only
- **Intelligence**: AI/ML interpretation only
- **Policy Engine**: Decision making only

### 2. **Versioning**
- Each consent update creates a new version
- Maintains full audit trail
- Can rollback to previous versions

### 3. **Confidence Scoring**
- Low confidence → Human review required
- High confidence → Auto-approve
- Threshold configurable

### 4. **FHIR Compliance**
- Standard healthcare data format
- Interoperable with other systems
- Future-proof

---

## Next Steps

1. **Set up all three services** with proper environment variables
2. **Test the flow** end-to-end
3. **Add API Gateway** to coordinate calls
4. **Implement async processing** for production
5. **Add monitoring** and logging
6. **Create admin dashboard** for reviewing low-confidence consents

---

## Testing the Services

### Quick Test Script
```bash
# 1. Upload consent
CONSENT_RESPONSE=$(curl -X POST http://localhost:8001/consents/upload \
  -F "patient_id=$(uuidgen)" \
  -F "file=@test_consent.pdf")

CONSENT_ID=$(echo $CONSENT_RESPONSE | jq -r '.consent_id')

# 2. Get consent details
curl http://localhost:8001/consents/$CONSENT_ID

# 3. Evaluate access
curl -X POST http://localhost:8003/policy/evaluate \
  -H "Content-Type: application/json" \
  -d "{
    \"patient_id\": \"$PATIENT_ID\",
    \"requester_id\": \"researcher-123\",
    \"requested_data_types\": [\"lab_results\"],
    \"purpose\": \"research\"
  }"
```

---

## Summary

Your consent architecture is **well-designed** with clear separation of concerns:

✅ **Ingestion** handles document processing  
✅ **Intelligence** handles AI interpretation  
✅ **Policy Engine** handles access decisions  

This modular design allows each service to scale independently and makes the system maintainable and testable.
