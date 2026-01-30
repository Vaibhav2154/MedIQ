-- Consent Ingestion Database Schema
-- This script creates all tables for the Consent Ingestion Service

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Consents table (logical consent object)
CREATE TABLE IF NOT EXISTS consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID NOT NULL,  -- References patients in identity_db (logical reference)
    status VARCHAR(50) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'revoked', 'expired')),
    confidence_score NUMERIC(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Consent Versions table (versioned consent documents)
CREATE TABLE IF NOT EXISTS consent_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consent_id UUID NOT NULL REFERENCES consents(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    raw_text TEXT NOT NULL,
    fhir_consent JSONB NOT NULL DEFAULT '{}',
    extracted_policy JSONB NOT NULL DEFAULT '{}',
    language VARCHAR(10) DEFAULT 'en',
    checksum VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(consent_id, version_number)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_consents_patient ON consents(patient_id);
CREATE INDEX IF NOT EXISTS idx_consents_status ON consents(status);
CREATE INDEX IF NOT EXISTS idx_consent_versions_consent ON consent_versions(consent_id);
CREATE INDEX IF NOT EXISTS idx_consent_versions_version ON consent_versions(consent_id, version_number);

-- Display created tables
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

\echo '✓ Consent Ingestion schema created successfully!'
