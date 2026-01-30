#!/bin/bash
# Clear Consent Data Script
# Safely deletes all consents and consent versions from the database

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================================================"
echo "Clear Consent Data"
echo "======================================================================"
echo ""

# Check if CONSENT_DATABASE_URL is set
if [ -z "$CONSENT_DATABASE_URL" ]; then
    echo -e "${RED}Error: CONSENT_DATABASE_URL environment variable is not set${NC}"
    echo "Please set it to your Consent Ingestion PostgreSQL connection string"
    echo "Example: export CONSENT_DATABASE_URL='postgresql://user:password@localhost:5432/consent_db'"
    exit 1
fi

echo -e "${YELLOW}WARNING: This will delete ALL consent data!${NC}"
echo "Database: $CONSENT_DATABASE_URL"
echo ""

# Confirm before proceeding
read -p "Are you sure you want to delete all consents? (yes/NO) " -r
echo
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Second confirmation
read -p "Type 'DELETE' to confirm: " -r
echo
if [[ $REPLY != "DELETE" ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "Clearing consent data..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the SQL script
psql "$CONSENT_DATABASE_URL" -f "$SCRIPT_DIR/clear_consents.sql"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Consent data cleared successfully${NC}"
else
    echo ""
    echo -e "${RED}✗ Failed to clear consent data${NC}"
    exit 1
fi

echo "======================================================================"
