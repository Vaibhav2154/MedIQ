#!/bin/bash
# Stop All MedIQ Backend Microservices
# This script stops all running microservices started by run_all_services.sh

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Log directory
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$LOG_DIR/services.pid"

echo "======================================================================"
echo -e "${CYAN}Stopping MedIQ Backend Microservices${NC}"
echo "======================================================================"
echo ""

if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}⚠ No PID file found. Services may not be running.${NC}"
    echo ""
    echo -e "${YELLOW}Attempting to kill processes on known ports...${NC}"
    
    # Try to kill processes on known ports
    for port in 8000 8001 8002 8003 8004; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${BLUE}Killing process on port $port...${NC}"
            lsof -ti:$port | xargs kill -9 2>/dev/null || true
            echo -e "${GREEN}✓ Killed process on port $port${NC}"
        fi
    done
    
    exit 0
fi

# Read PID file and stop services
while IFS=: read -r name pid port; do
    echo -e "${BLUE}Stopping: $name (PID: $pid, Port: $port)${NC}"
    
    if ps -p $pid > /dev/null 2>&1; then
        kill $pid 2>/dev/null || true
        
        # Wait for process to terminate
        for i in {1..5}; do
            if ! ps -p $pid > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${YELLOW}  Process still running, force killing...${NC}"
            kill -9 $pid 2>/dev/null || true
        fi
        
        echo -e "${GREEN}✓ $name stopped${NC}"
    else
        echo -e "${YELLOW}⚠ $name was not running (PID: $pid)${NC}"
    fi
    
    # Also try to kill any process on the port
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}  Cleaning up port $port...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
    fi
    
    echo ""
done < "$PID_FILE"

# Remove PID file
rm -f "$PID_FILE"

echo "======================================================================"
echo -e "${GREEN}All services stopped successfully${NC}"
echo "======================================================================"
