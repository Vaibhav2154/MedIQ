#!/bin/bash
# Run All Seeding Scripts
# This script executes all database seeding scripts in the correct order

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Change to the MedIQ root directory (parent of Scripts)
cd "$SCRIPT_DIR/.."

# Disable psql pager to prevent --more-- prompts
export PAGER=cat

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "MedIQ Database Seeding Script"
echo "======================================================================"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}Error: DATABASE_URL environment variable is not set${NC}"
    echo "Please set it to your PostgreSQL connection string, e.g.:"
    echo "export DATABASE_URL='postgresql://user:password@localhost:5432/identity_db'"
    exit 1
fi

echo -e "${GREEN}Using DATABASE_URL: ${DATABASE_URL}${NC}"
echo ""

# Confirm before proceeding
read -p "This will seed the database with sample data. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "======================================================================"
echo "Step 1: Seeding Organizations"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/01_seed_organizations.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Organizations seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed organizations${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 2: Seeding Users"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/02_seed_users.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Users seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed users${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 3: Seeding Patients"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/03_seed_patients.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Patients seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed patients${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 4: Seeding Diabetes Medical Data"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/04_seed_diabetes_data.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Diabetes data seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed diabetes data${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 5: Seeding Hypertension Medical Data"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/05_seed_hypertension_data.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Hypertension data seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed hypertension data${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 6: Seeding Cardiovascular Medical Data"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/06_seed_cardiovascular_data.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cardiovascular data seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed cardiovascular data${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 7: Seeding Respiratory Medical Data"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/07_seed_respiratory_data.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Respiratory data seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed respiratory data${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 8: Seeding Cancer Medical Data"
echo "======================================================================"
psql "$DATABASE_URL" -f Scripts/identity-service/08_seed_cancer_data.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cancer data seeded successfully${NC}"
else
    echo -e "${RED}✗ Failed to seed cancer data${NC}"
    exit 1
fi

echo ""
echo "======================================================================"
echo "Step 9: Seeding Consents"
echo "======================================================================"
echo "Note: This requires Identity Service and Consent Ingestion to be running"
echo ""

# Check if services are running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Warning: Identity Service (port 8000) is not responding${NC}"
    echo "Please start the Identity Service before running consent seeding"
    echo "Skipping consent seeding..."
else
    if ! curl -s http://localhost:8002/health > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Warning: Consent Ingestion (port 8002) is not responding${NC}"
        echo "Please start the Consent Ingestion service before running consent seeding"
        echo "Skipping consent seeding..."
    else
        cd Scripts/consent-ingestion
        python3 seed_consents.py
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Consents seeded successfully${NC}"
        else
            echo -e "${RED}✗ Failed to seed consents${NC}"
            echo "You can run consent seeding manually later with:"
            echo "  cd Scripts/consent-ingestion && python3 seed_consents.py"
        fi
        cd ../..
    fi
fi

echo ""
echo "======================================================================"
echo "SEEDING COMPLETE"
echo "======================================================================"
echo -e "${GREEN}All database seeding operations completed successfully!${NC}"
echo ""
echo "Summary:"
echo "  - Organizations: 11"
echo "  - Users: 31"
echo "  - Patients: 625 (125 per disease category)"
echo "  - Encounters: ~1,875 (3 per patient)"
echo "  - Observations: ~11,250"
echo "  - Diagnoses: ~1,000"
echo "  - Medications: ~1,500"
echo "  - Consents: ~625 (if services were running)"
echo ""
echo "You can now use the seeded data for testing and development."
echo "======================================================================"
