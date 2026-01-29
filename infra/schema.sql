-- MedIQ MVP Database Schema

-- 1. Patients (Pointer table)
CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    abha_id TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT now()
);

-- 2. Consents (Logical object)
CREATE TABLE IF NOT EXISTS consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL REFERENCES patients(id),
    source TEXT,
    status TEXT NOT NULL CHECK (
        status IN ('active', 'revoked', 'expired')
    ),
    confidence_score NUMERIC(3,2),
    created_at TIMESTAMP DEFAULT now()
);

-- 3. Consent Versions (Legal/Historical)
CREATE TABLE IF NOT EXISTS consent_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consent_id UUID NOT NULL REFERENCES consents(id),
    version_number INTEGER NOT NULL,
    raw_text TEXT,
    fhir_consent JSONB NOT NULL,
    extracted_policy JSONB NOT NULL,
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE (consent_id, version_number)
);

-- 4. Policy Rules (Executable behavior)
CREATE TABLE IF NOT EXISTS policy_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consent_version_id UUID NOT NULL REFERENCES consent_versions(id),
    purpose TEXT NOT NULL,
    allowed_fields TEXT[] NOT NULL,
    denied_fields TEXT[] NOT NULL,
    conditions JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- 5. Organizations
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    org_type TEXT NOT NULL CHECK (
        org_type IN ('hospital', 'research_org', 'government')
    ),
    created_at TIMESTAMP DEFAULT now()
);

-- 6. Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (
        role IN ('patient', 'researcher', 'admin', 'regulator')
    ),
    created_at TIMESTAMP DEFAULT now()
);

-- 7. Research Studies
CREATE TABLE IF NOT EXISTS research_studies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    purpose TEXT NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT now()
);

-- 8. Data Access Requests
CREATE TABLE IF NOT EXISTS data_access_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    study_id UUID NOT NULL REFERENCES research_studies(id),
    requester_id UUID NOT NULL REFERENCES users(id),
    requested_fields TEXT[] NOT NULL,
    request_context JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- 9. Data Access Decisions
CREATE TABLE IF NOT EXISTS data_access_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES data_access_requests(id),
    decision TEXT NOT NULL CHECK (
        decision IN ('allow', 'deny', 'partial')
    ),
    allowed_fields TEXT[],
    denied_fields TEXT[],
    explanation TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 10. Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id UUID,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id UUID,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_consents_patient ON consents(patient_id);
CREATE INDEX IF NOT EXISTS idx_policy_purpose ON policy_rules(purpose);
CREATE INDEX IF NOT EXISTS idx_requests_study ON data_access_requests(study_id);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_logs(actor_id);
