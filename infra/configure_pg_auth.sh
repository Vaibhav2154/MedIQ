#!/bin/bash
# Configure PostgreSQL to allow password authentication
# This script updates pg_hba.conf to enable md5 authentication

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================================================"
echo "Configure PostgreSQL Authentication"
echo "======================================================================"
echo ""

# Find pg_hba.conf location
PG_HBA=$(sudo -u postgres psql -t -P format=unaligned -c 'SHOW hba_file')

echo -e "${YELLOW}PostgreSQL configuration file: $PG_HBA${NC}"
echo ""

# Backup original file
echo "Creating backup..."
sudo cp "$PG_HBA" "${PG_HBA}.backup.$(date +%Y%m%d_%H%M%S)"
echo -e "${GREEN}✓ Backup created${NC}"
echo ""

# Add md5 authentication for local connections
echo "Configuring authentication..."
sudo bash -c "cat > $PG_HBA" <<'EOF'
# PostgreSQL Client Authentication Configuration File
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             postgres                                peer
local   all             all                                     md5

# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# Allow replication connections from localhost
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
EOF

echo -e "${GREEN}✓ Configuration updated${NC}"
echo ""

# Reload PostgreSQL
echo "Reloading PostgreSQL..."
sudo systemctl reload postgresql
echo -e "${GREEN}✓ PostgreSQL reloaded${NC}"
echo ""

echo "======================================================================"
echo -e "${GREEN}Configuration Complete!${NC}"
echo "======================================================================"
echo ""
echo "You can now connect using:"
echo "  psql -h localhost -U mediq_user -d identity_db"
echo ""
