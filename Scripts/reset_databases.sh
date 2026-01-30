#!/bin/bash
# Reset Databases Script
# WARNING: This will DELETE ALL DATA in the specified tables

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "MedIQ Database Reset Script"
echo "======================================================================"
echo ""
echo -e "${RED}WARNING: This will DELETE ALL DATA from the following tables:${NC}"
echo "  - medications"
echo "  - diagnoses"
echo "  - observations"
echo "  - encounters"
echo "  - patients"
echo "  - users"
echo "  - organizations"
echo ""
echo -e "${YELLOW}This action CANNOT be undone!${NC}"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}Error: DATABASE_URL environment variable is not set${NC}"
    echo "Please set it to your PostgreSQL connection string, e.g.:"
    echo "export DATABASE_URL='postgresql://user:password@localhost:5432/identity_db'"
    exit 1
fi

echo -e "Database: ${DATABASE_URL}"
echo ""

# Triple confirmation
read -p "Are you ABSOLUTELY SURE you want to delete all data? (yes/NO) " -r
echo
if [[ ! $REPLY == "yes" ]]; then
    echo "Aborted. No changes made."
    exit 0
fi

read -p "Type 'DELETE ALL DATA' to confirm: " -r
echo
if [[ ! $REPLY == "DELETE ALL DATA" ]]; then
    echo "Aborted. No changes made."
    exit 0
fi

echo ""
echo "======================================================================"
echo "Truncating tables..."
echo "======================================================================"

# Truncate tables in reverse dependency order
psql "$DATABASE_URL" <<EOF
-- Truncate medical data tables
TRUNCATE TABLE medications CASCADE;
TRUNCATE TABLE diagnoses CASCADE;
TRUNCATE TABLE observations CASCADE;
TRUNCATE TABLE encounters CASCADE;

-- Truncate patient and user tables
TRUNCATE TABLE patients CASCADE;
TRUNCATE TABLE users CASCADE;

-- Truncate organizations
TRUNCATE TABLE organizations CASCADE;

-- Display counts to confirm
SELECT 'organizations' as table_name, COUNT(*) as count FROM organizations
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'patients', COUNT(*) FROM patients
UNION ALL
SELECT 'encounters', COUNT(*) FROM encounters
UNION ALL
SELECT 'observations', COUNT(*) FROM observations
UNION ALL
SELECT 'diagnoses', COUNT(*) FROM diagnoses
UNION ALL
SELECT 'medications', COUNT(*) FROM medications;
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ All tables truncated successfully${NC}"
    echo ""
    echo "The database is now empty and ready for fresh seeding."
    echo "Run './run_all_seeds.sh' to populate with sample data."
else
    echo ""
    echo -e "${RED}✗ Failed to truncate tables${NC}"
    exit 1
fi

echo "======================================================================"
