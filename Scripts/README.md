# MedIQ Database Seeding Scripts

This directory contains SQL and Python scripts to seed the MedIQ databases with realistic sample data for development and testing.

## Overview

The seeding scripts populate:
- **Identity Service**: 625 patients across 5 disease categories with comprehensive medical records
- **Consent Ingestion**: ~625 consent documents with varied scenarios

## Prerequisites

1. **PostgreSQL** installed and running
2. **Python 3.8+** with `requests` library
3. **Services running**:
   - Identity Service (port 8000)
   - Consent Ingestion (port 8002)
   - Consent Intelligence (port 8001)

## Quick Start

### 1. Set Database Connection

```bash
export DATABASE_URL='postgresql://user:password@localhost:5432/identity_db'
```

### 2. Run All Seeds

```bash
cd /path/to/MedIQ/Scripts
./run_all_seeds.sh
```

This will seed:
- 11 organizations
- 31 users (doctors, researchers, admins, regulators)
- 625 patients (125 per disease category)
- Medical data (encounters, observations, diagnoses, medications)
- ~625 consents

## Manual Seeding

### Identity Service (SQL Scripts)

Execute in order:

```bash
# 1. Organizations
psql $DATABASE_URL -f identity-service/01_seed_organizations.sql

# 2. Users
psql $DATABASE_URL -f identity-service/02_seed_users.sql

# 3. Patients
psql $DATABASE_URL -f identity-service/03_seed_patients.sql

# 4-8. Medical Data by Disease Category
psql $DATABASE_URL -f identity-service/04_seed_diabetes_data.sql
psql $DATABASE_URL -f identity-service/05_seed_hypertension_data.sql
psql $DATABASE_URL -f identity-service/06_seed_cardiovascular_data.sql
psql $DATABASE_URL -f identity-service/07_seed_respiratory_data.sql
psql $DATABASE_URL -f identity-service/08_seed_cancer_data.sql
```

### Consent Ingestion (Python Script)

Requires services to be running:

```bash
cd consent-ingestion
python3 seed_consents.py
```

Options:
- `--dry-run`: Preview without uploading
- `--identity-url URL`: Custom Identity Service URL
- `--consent-url URL`: Custom Consent Ingestion URL

## Disease Categories

Each category has 125 patients with realistic medical histories:

| Category | ABHA Prefix | Conditions | Medications |
|----------|-------------|------------|-------------|
| **Diabetes** | 91-2345 | Type 1 & 2 Diabetes, complications | Metformin, Insulin |
| **Hypertension** | 91-3456 | Essential & Secondary HTN | ACE inhibitors, Beta blockers |
| **Cardiovascular** | 91-4567 | CAD, Heart Failure, AFib | Statins, Anticoagulants |
| **Respiratory** | 91-5678 | Asthma, COPD, Pneumonia | Bronchodilators, Corticosteroids |
| **Cancer** | 91-6789 | Breast, Lung, Colorectal, Prostate, Ovarian | Chemotherapy agents |

## Data Volume

- **Organizations**: 11
- **Users**: 31
- **Patients**: 625
- **Encounters**: ~1,875 (3 per patient)
- **Observations**: ~11,250 (6 per encounter avg)
- **Diagnoses**: ~1,000
- **Medications**: ~1,500
- **Consents**: ~625

## Resetting Data

**WARNING**: This deletes ALL data!

```bash
./reset_databases.sh
```

You will be prompted for confirmation multiple times.

## Performance

The scripts are optimized for bulk inserts:
- Patient seeding uses `generate_series()` for efficient bulk creation
- Medical data uses batch inserts within procedural blocks
- Typical execution time: 2-5 minutes for complete seeding

## Consent Types

The consent seeding creates varied scenarios:
- **Full Research**: Broad permissions for research use
- **Limited Care**: Care coordination only
- **Disease-Specific**: Targeted research consent
- **Partial**: Selective data sharing with exclusions
- **Ambiguous**: Low confidence scenarios for testing
- **Expired**: Past validity period
- **Revoked**: Withdrawn consent

## Troubleshooting

### "DATABASE_URL not set"
```bash
export DATABASE_URL='postgresql://user:password@localhost:5432/dbname'
```

### "Service not responding"
Ensure all services are running:
```bash
# Identity Service
cd apps/backend/identity-service
uv run uvicorn main:app --reload --port 8000

# Consent Ingestion
cd apps/backend/consent-ingestion
uvicorn app.main:app --reload --port 8002

# Consent Intelligence
cd apps/backend/consent-intelligence
uvicorn app.main:app --reload --port 8001
```

### Slow execution
- Check database connection
- Ensure adequate system resources
- Consider running medical data scripts individually

## User Credentials

All seeded users have password: `Password123!`

Example logins:
- Doctor: `dr.sharma@apollo.com`
- Researcher: `researcher.agarwal@icmr.gov.in`
- Admin: `admin@apollo.com`
- Regulator: `regulator@mohfw.gov.in`

## Notes

- UUIDs are deterministic for patients to enable consistent testing
- ABHA IDs follow the pattern: `91-XXXX-XXXX-XXXX`
- Medical data includes realistic progression over time (6-12 months)
- Consent documents are text files uploaded via API

## Support

For issues or questions, refer to:
- `/docs/identity-consent-integration.md` - Integration guide
- Service-specific READMEs in `apps/backend/`
