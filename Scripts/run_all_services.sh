#!/bin/bash
# Run All MedIQ Backend Microservices
# This script starts all backend microservices concurrently with proper port assignments

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Change to the MedIQ root directory (parent of Scripts)
cd "$SCRIPT_DIR/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Log directory for service outputs
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

# PID file to track running services
PID_FILE="$LOG_DIR/services.pid"

echo "======================================================================"
echo -e "${CYAN}MedIQ Backend Microservices Launcher${NC}"
echo "======================================================================"
echo ""

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on a port
kill_port() {
    local port=$1
    local service_name=$2
    if check_port $port; then
        echo -e "${YELLOW}⚠ Port $port is already in use by another process${NC}"
        read -p "Kill the process on port $port? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            lsof -ti:$port | xargs kill -9 2>/dev/null || true
            echo -e "${GREEN}✓ Killed process on port $port${NC}"
            sleep 1
        else
            echo -e "${RED}✗ Cannot start $service_name - port $port is occupied${NC}"
            return 1
        fi
    fi
    return 0
}

# Function to start a service
start_service() {
    local service_name=$1
    local service_dir=$2
    local port=$3
    local start_command=$4
    local color=$5
    
    echo ""
    echo -e "${color}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${color}Starting: $service_name (Port: $port)${NC}"
    echo -e "${color}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Check and handle port conflicts
    if ! kill_port $port "$service_name"; then
        return 1
    fi
    
    # Navigate to service directory
    cd "$service_dir"
    
    # Start the service in background
    LOG_FILE="$LOG_DIR/${service_name}.log"
    echo -e "${BLUE}Command: $start_command${NC}"
    echo -e "${BLUE}Log file: $LOG_FILE${NC}"
    
    # Execute the start command
    eval "$start_command > $LOG_FILE 2>&1 &"
    local pid=$!
    
    # Save PID
    echo "$service_name:$pid:$port" >> "$PID_FILE"
    
    # Wait a moment and check if process is still running
    sleep 2
    if ps -p $pid > /dev/null; then
        echo -e "${GREEN}✓ $service_name started successfully (PID: $pid)${NC}"
        echo -e "${GREEN}  Access at: http://localhost:$port${NC}"
        return 0
    else
        echo -e "${RED}✗ $service_name failed to start${NC}"
        echo -e "${RED}  Check log: $LOG_FILE${NC}"
        return 1
    fi
}

# Clean up previous PID file
rm -f "$PID_FILE"

echo -e "${CYAN}Checking prerequisites...${NC}"
echo ""

# Check if required commands exist
for cmd in python3 uvicorn lsof; do
    if ! command -v $cmd &> /dev/null; then
        echo -e "${RED}✗ Required command '$cmd' not found${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✓ All prerequisites met${NC}"

# Start all services
echo ""
echo "======================================================================"
echo -e "${CYAN}Starting Microservices...${NC}"
echo "======================================================================"

# 1. Identity Service (Port 8000)
start_service \
    "Identity Service" \
    "apps/backend/identity-service" \
    "8000" \
    "uv run uvicorn main:app --host 0.0.0.0 --port 8000" \
    "$GREEN"

# 2. Consent Intelligence (Port 8001)
start_service \
    "Consent Intelligence" \
    "apps/backend/consent-intelligence" \
    "8001" \
    "uvicorn app.main:app --host 0.0.0.0 --port 8001" \
    "$BLUE"

# 3. Consent Ingestion (Port 8002)
start_service \
    "Consent Ingestion" \
    "apps/backend/consent-ingestion" \
    "8002" \
    "uvicorn app.main:app --host 0.0.0.0 --port 8002" \
    "$MAGENTA"

# 4. Policy Engine (Port 8003)
start_service \
    "Policy Engine" \
    "apps/backend/policy-engine" \
    "8003" \
    "uvicorn app.main:app --host 0.0.0.0 --port 8003" \
    "$YELLOW"

# 5. Researcher Service (Port 8004)
start_service \
    "Researcher Service" \
    "apps/backend/researcher-service" \
    "8004" \
    "uvicorn app.main:app --host 0.0.0.0 --port 8004" \
    "$CYAN"

# Return to original directory
cd "$SCRIPT_DIR/.."

echo ""
echo "======================================================================"
echo -e "${GREEN}All Services Started!${NC}"
echo "======================================================================"
echo ""
echo -e "${CYAN}Service Status:${NC}"
echo ""

# Display service URLs
if [ -f "$PID_FILE" ]; then
    while IFS=: read -r name pid port; do
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $name"
            echo -e "  ${BLUE}URL:${NC} http://localhost:$port"
            echo -e "  ${BLUE}Docs:${NC} http://localhost:$port/docs"
            echo -e "  ${BLUE}PID:${NC} $pid"
            echo ""
        else
            echo -e "${RED}✗${NC} $name (failed to start)"
            echo ""
        fi
    done < "$PID_FILE"
fi

echo "======================================================================"
echo -e "${CYAN}Useful Commands:${NC}"
echo "======================================================================"
echo ""
echo -e "${YELLOW}View logs:${NC}"
echo "  tail -f $LOG_DIR/<service-name>.log"
echo ""
echo -e "${YELLOW}Stop all services:${NC}"
echo "  $SCRIPT_DIR/stop_all_services.sh"
echo ""
echo -e "${YELLOW}Check service health:${NC}"
echo "  curl http://localhost:8000/health  # Identity Service"
echo "  curl http://localhost:8001/        # Consent Intelligence"
echo "  curl http://localhost:8002/        # Consent Ingestion"
echo "  curl http://localhost:8003/        # Policy Engine"
echo "  curl http://localhost:8004/        # Researcher Service"
echo ""
echo "======================================================================"
echo -e "${GREEN}Services are running in the background${NC}"
echo -e "${YELLOW}Press Ctrl+C to exit this script (services will continue running)${NC}"
echo "======================================================================"
