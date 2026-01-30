#!/bin/bash
# Verify Database Seeding
# This script checks record counts in all tables to verify seeding was successful

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Disable psql pager
export PAGER=cat

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "MedIQ Database Seeding Verification"
echo "======================================================================"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}Error: DATABASE_URL environment variable is not set${NC}"
    echo "Please set it to your PostgreSQL connection string"
    exit 1
fi

echo -e "${BLUE}Checking Identity Service Database...${NC}"
echo ""

# Run verification query
psql "$DATABASE_URL" <<EOF
-- Disable pager
\pset pager off

-- Set output format
\pset border 2

-- Overall Summary
SELECT 
    '=== OVERALL SUMMARY ===' as section;

SELECT 
    'Organizations' as table_name,
    COUNT(*) as total_records,
    CASE WHEN COUNT(*) = 11 THEN '✓ PASS' ELSE '✗ FAIL' END as status
FROM organizations
UNION ALL
SELECT 
    'Users',
    COUNT(*),
    CASE WHEN COUNT(*) = 31 THEN '✓ PASS' ELSE '✗ FAIL' END
FROM users
UNION ALL
SELECT 
    'Patients',
    COUNT(*),
    CASE WHEN COUNT(*) = 625 THEN '✓ PASS' ELSE '✗ FAIL' END
FROM patients
UNION ALL
SELECT 
    'Encounters',
    COUNT(*),
    CASE WHEN COUNT(*) >= 1800 THEN '✓ PASS' ELSE '✗ FAIL' END
FROM encounters
UNION ALL
SELECT 
    'Observations',
    COUNT(*),
    CASE WHEN COUNT(*) >= 10000 THEN '✓ PASS' ELSE '✗ FAIL' END
FROM observations
UNION ALL
SELECT 
    'Diagnoses',
    COUNT(*),
    CASE WHEN COUNT(*) >= 800 THEN '✓ PASS' ELSE '✗ FAIL' END
FROM diagnoses
UNION ALL
SELECT 
    'Medications',
    COUNT(*),
    CASE WHEN COUNT(*) >= 1200 THEN '✓ PASS' ELSE '✗ FAIL' END
FROM medications;

-- Patients by Disease Category
SELECT 
    '' as blank_line;

SELECT 
    '=== PATIENTS BY DISEASE CATEGORY ===' as section;

SELECT 
    CASE 
        WHEN abha_id LIKE '91-2345%' THEN 'Diabetes'
        WHEN abha_id LIKE '91-3456%' THEN 'Hypertension'
        WHEN abha_id LIKE '91-4567%' THEN 'Cardiovascular'
        WHEN abha_id LIKE '91-5678%' THEN 'Respiratory'
        WHEN abha_id LIKE '91-6789%' THEN 'Cancer'
        ELSE 'Other'
    END as disease_category,
    COUNT(*) as patient_count,
    CASE WHEN COUNT(*) = 125 THEN '✓ PASS' ELSE '✗ FAIL' END as status
FROM patients
GROUP BY disease_category
ORDER BY disease_category;

-- Medical Data by Disease Category
SELECT 
    '' as blank_line;

SELECT 
    '=== MEDICAL DATA BY DISEASE CATEGORY ===' as section;

WITH categorized_patients AS (
    SELECT 
        p.id,
        CASE 
            WHEN p.abha_id LIKE '91-2345%' THEN 'Diabetes'
            WHEN p.abha_id LIKE '91-3456%' THEN 'Hypertension'
            WHEN p.abha_id LIKE '91-4567%' THEN 'Cardiovascular'
            WHEN p.abha_id LIKE '91-5678%' THEN 'Respiratory'
            WHEN p.abha_id LIKE '91-6789%' THEN 'Cancer'
        END as category
    FROM patients p
)
SELECT 
    cp.category,
    COUNT(DISTINCT cp.id) as patients,
    COUNT(DISTINCT e.id) as encounters,
    COUNT(DISTINCT o.id) as observations,
    COUNT(DISTINCT d.id) as diagnoses,
    COUNT(DISTINCT m.id) as medications
FROM categorized_patients cp
LEFT JOIN encounters e ON cp.id = e.patient_id
LEFT JOIN observations o ON cp.id = o.patient_id
LEFT JOIN diagnoses d ON cp.id = d.patient_id
LEFT JOIN medications m ON cp.id = m.patient_id
GROUP BY cp.category
ORDER BY cp.category;

-- Organization Distribution
SELECT 
    '' as blank_line;

SELECT 
    '=== ORGANIZATION TYPES ===' as section;

SELECT 
    org_type,
    COUNT(*) as count
FROM organizations
GROUP BY org_type
ORDER BY org_type;

-- User Role Distribution
SELECT 
    '' as blank_line;

SELECT 
    '=== USER ROLES ===' as section;

SELECT 
    role,
    COUNT(*) as count
FROM users
GROUP BY role
ORDER BY role;

-- Sample Data Check
SELECT 
    '' as blank_line;

SELECT 
    '=== SAMPLE RECORDS ===' as section;

-- Sample patients
SELECT 
    'Sample Diabetes Patient:' as info,
    abha_id,
    id
FROM patients 
WHERE abha_id LIKE '91-2345%' 
LIMIT 1;

SELECT 
    'Sample Encounter:' as info,
    encounter_type,
    reason
FROM encounters 
LIMIT 1;

SELECT 
    'Sample Observation:' as info,
    category,
    code,
    value,
    unit
FROM observations 
LIMIT 1;

SELECT 
    'Sample Diagnosis:' as info,
    code,
    description
FROM diagnoses 
LIMIT 1;

SELECT 
    'Sample Medication:' as info,
    name,
    dose,
    unit,
    frequency
FROM medications 
LIMIT 1;

EOF

echo ""
echo "======================================================================"
echo -e "${GREEN}Verification Complete!${NC}"
echo "======================================================================"
echo ""
echo "Expected counts:"
echo "  - Organizations: 11"
echo "  - Users: 31"
echo "  - Patients: 625 (125 per category)"
echo "  - Encounters: ~1,875"
echo "  - Observations: ~11,250"
echo "  - Diagnoses: ~1,000"
echo "  - Medications: ~1,500"
echo ""
echo "If any counts are significantly different, review the seeding logs."
echo "======================================================================"
