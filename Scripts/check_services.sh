#!/bin/bash
# Check Status of All MedIQ Backend Microservices
# This script checks the health and status of all running microservices

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Log directory
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$LOG_DIR/services.pid"

echo "======================================================================"
echo -e "${CYAN}MedIQ Backend Microservices Status${NC}"
echo "======================================================================"
echo ""

# Service definitions
declare -A SERVICES
SERVICES=(
    ["Identity Service"]="8000:/health"
    ["Consent Intelligence"]="8001:/"
    ["Consent Ingestion"]="8002:/"
    ["Policy Engine"]="8003:/"
    ["Researcher Service"]="8004:/"
)

# Function to check service health
check_service() {
    local name=$1
    local port=$2
    local endpoint=$3
    
    echo -e "${BLUE}Checking: $name${NC}"
    echo -e "  Port: $port"
    echo -e "  Endpoint: http://localhost:$port$endpoint"
    
    # Check if port is listening
    if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "  ${RED}✗ Not running (port not listening)${NC}"
        echo ""
        return 1
    fi
    
    # Check HTTP response
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port$endpoint 2>/dev/null || echo "000")
    
    if [ "$response" = "200" ]; then
        echo -e "  ${GREEN}✓ Running and healthy (HTTP $response)${NC}"
        
        # Get process info
        pid=$(lsof -ti:$port 2>/dev/null | head -n 1)
        if [ -n "$pid" ]; then
            echo -e "  PID: $pid"
        fi
    elif [ "$response" = "000" ]; then
        echo -e "  ${RED}✗ Not responding (connection failed)${NC}"
    else
        echo -e "  ${YELLOW}⚠ Running but returned HTTP $response${NC}"
    fi
    
    echo ""
}

# Check all services
for service_name in "${!SERVICES[@]}"; do
    IFS=':' read -r port endpoint <<< "${SERVICES[$service_name]}"
    check_service "$service_name" "$port" "$endpoint"
done

# Show PID file info if exists
if [ -f "$PID_FILE" ]; then
    echo "======================================================================"
    echo -e "${CYAN}Tracked Services (from PID file):${NC}"
    echo "======================================================================"
    echo ""
    
    while IFS=: read -r name pid port; do
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} $name (PID: $pid, Port: $port)"
        else
            echo -e "${RED}✗${NC} $name (PID: $pid - not running, Port: $port)"
        fi
    done < "$PID_FILE"
    echo ""
fi

# Show log files
if [ -d "$LOG_DIR" ] && [ "$(ls -A $LOG_DIR/*.log 2>/dev/null)" ]; then
    echo "======================================================================"
    echo -e "${CYAN}Available Log Files:${NC}"
    echo "======================================================================"
    echo ""
    
    for log_file in "$LOG_DIR"/*.log; do
        if [ -f "$log_file" ]; then
            size=$(du -h "$log_file" | cut -f1)
            modified=$(stat -c %y "$log_file" 2>/dev/null || stat -f %Sm "$log_file" 2>/dev/null)
            echo -e "${BLUE}$(basename $log_file)${NC}"
            echo "  Size: $size"
            echo "  Modified: $modified"
            echo "  Path: $log_file"
            echo ""
        fi
    done
fi

echo "======================================================================"
echo -e "${CYAN}Quick Commands:${NC}"
echo "======================================================================"
echo ""
echo -e "${YELLOW}View logs:${NC}"
echo "  tail -f $LOG_DIR/<service-name>.log"
echo ""
echo -e "${YELLOW}Test endpoints:${NC}"
echo "  curl http://localhost:8000/docs  # Identity Service API docs"
echo "  curl http://localhost:8001/docs  # Consent Intelligence API docs"
echo "  curl http://localhost:8002/docs  # Consent Ingestion API docs"
echo "  curl http://localhost:8003/docs  # Policy Engine API docs"
echo "  curl http://localhost:8004/docs  # Researcher Service API docs"
echo ""
