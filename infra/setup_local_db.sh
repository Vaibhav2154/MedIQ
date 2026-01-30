#!/bin/bash
# Setup Local PostgreSQL Databases for MedIQ
# This script creates databases, users, and initializes schemas

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "======================================================================"
echo "MedIQ Local PostgreSQL Setup"
echo "======================================================================"
echo ""

# Configuration
DB_USER="mediq_user"
DB_PASSWORD="password"
IDENTITY_DB="identity_db"
CONSENT_DB="consent_db"

echo -e "${BLUE}Configuration:${NC}"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo "  Identity Database: $IDENTITY_DB"
echo "  Consent Database: $CONSENT_DB"
echo ""

# Check if PostgreSQL is running
if ! sudo systemctl is-active --quiet postgresql; then
    echo -e "${YELLOW}PostgreSQL is not running. Starting...${NC}"
    sudo systemctl start postgresql
    sleep 2
fi

echo -e "${GREEN}✓ PostgreSQL is running${NC}"
echo ""

# Create databases and user
echo -e "${BLUE}Creating databases and user...${NC}"
sudo -u postgres psql <<EOF
-- Create user if not exists
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Create databases
DROP DATABASE IF EXISTS $IDENTITY_DB;
DROP DATABASE IF EXISTS $CONSENT_DB;

CREATE DATABASE $IDENTITY_DB OWNER $DB_USER;
CREATE DATABASE $CONSENT_DB OWNER $DB_USER;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $IDENTITY_DB TO $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $CONSENT_DB TO $DB_USER;

\echo '✓ Databases and user created'
EOF

echo -e "${GREEN}✓ Databases created${NC}"
echo ""

# Grant schema privileges
echo -e "${BLUE}Granting schema privileges...${NC}"
PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $IDENTITY_DB <<EOF
GRANT ALL ON SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
EOF

PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $CONSENT_DB <<EOF
GRANT ALL ON SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
EOF

echo -e "${GREEN}✓ Privileges granted${NC}"
echo ""

# Initialize Identity Service schema
echo -e "${BLUE}Initializing Identity Service schema...${NC}"
PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $IDENTITY_DB -f "$(dirname "$0")/identity_schema.sql"
echo -e "${GREEN}✓ Identity Service schema initialized${NC}"
echo ""

# Initialize Consent Ingestion schema
echo -e "${BLUE}Initializing Consent Ingestion schema...${NC}"
PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $CONSENT_DB -f "$(dirname "$0")/consent_schema.sql"
echo -e "${GREEN}✓ Consent Ingestion schema initialized${NC}"
echo ""

# Display connection strings
echo "======================================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "======================================================================"
echo ""
echo "Connection strings for .env files:"
echo ""
echo -e "${YELLOW}Identity Service (.env):${NC}"
echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$IDENTITY_DB"
echo ""
echo -e "${YELLOW}Consent Ingestion (.env):${NC}"
echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$CONSENT_DB"
echo ""
echo "To connect manually:"
echo "  psql postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$IDENTITY_DB"
echo "  psql postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$CONSENT_DB"
echo ""
echo "======================================================================"
