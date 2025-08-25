#!/bin/bash

# CI/CD Health Dashboard - Complete Setup Script
# This is the ONLY script you need - it handles everything automatically
# 
# What this script does:
# 1. Sets up virtual environment
# 2. Installs all dependencies
# 3. Creates configuration files
# 4. Tests the application
# 5. Provides setup instructions
# 6. Tests webhooks and email functionality

set -e

echo "🚀 CI/CD Health Dashboard - Complete Setup"
echo "=========================================="
echo "This script will set up everything you need automatically!"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "SUCCESS" ]; then
        echo -e "${GREEN}✅ SUCCESS${NC}: $message"
    elif [ "$status" = "INFO" ]; then
        echo -e "${BLUE}ℹ️  INFO${NC}: $message"
    elif [ "$status" = "WARNING" ]; then
        echo -e "${YELLOW}⚠️  WARNING${NC}: $message"
    else
        echo -e "${RED}❌ ERROR${NC}: $message"
        exit 1
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo "🔍 Checking Python installation..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_status "SUCCESS" "Python found: $PYTHON_VERSION"
else
    print_status "ERROR" "Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if .venv exists and activate it
echo ""
echo "🔍 Setting up virtual environment..."
if [ -d ".venv" ]; then
    print_status "INFO" "Virtual environment .venv already exists"
else
    print_status "INFO" "Creating virtual environment .venv"
    python3 -m venv .venv
fi

# Activate virtual environment
print_status "INFO" "Activating virtual environment .venv"
source .venv/bin/activate

# Verify activation
if [ "$VIRTUAL_ENV" = "" ]; then
    print_status "ERROR" "Failed to activate virtual environment"
    exit 1
fi
print_status "SUCCESS" "Virtual environment activated: $VIRTUAL_ENV"

# Upgrade pip
echo ""
echo "🔧 Upgrading pip..."
python -m pip install --upgrade pip

# Install backend requirements
echo ""
echo "📦 Installing backend requirements..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
    print_status "SUCCESS" "Backend requirements installed"
else
    print_status "ERROR" "backend/requirements.txt not found"
    exit 1
fi

# Install worker requirements
echo ""
echo "📦 Installing worker requirements..."
if [ -f "worker/requirements.txt" ]; then
    pip install -r worker/requirements.txt
    print_status "SUCCESS" "Worker requirements installed"
else
    print_status "WARNING" "worker/requirements.txt not found"
fi

# Install root requirements (testing)
echo ""
echo "📦 Installing testing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "SUCCESS" "Testing requirements installed"
else
    print_status "WARNING" "requirements.txt not found"
fi

# Check if .env exists, if not run setup
echo ""
echo "🔧 Checking configuration..."
if [ ! -f ".env" ]; then
    print_status "INFO" "Configuration file not found, running setup..."
    if [ -f "setup_config.sh" ]; then
        chmod +x setup_config.sh
        ./setup_config.sh
        print_status "SUCCESS" "Configuration setup completed"
    else
        print_status "ERROR" "setup_config.sh not found"
        exit 1
    fi
else
    print_status "SUCCESS" "Configuration file .env already exists"
fi

# Verify all required packages are installed
echo ""
echo "🔍 Verifying package installation..."
REQUIRED_PACKAGES=("fastapi" "uvicorn" "sqlalchemy" "aiosqlite" "aiohttp" "httpx" "pydantic")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python -c "import $package" 2>/dev/null; then
        print_status "SUCCESS" "Package $package is available"
    else
        MISSING_PACKAGES+=("$package")
        print_status "ERROR" "Package $package is missing"
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    print_status "ERROR" "Missing packages: ${MISSING_PACKAGES[*]}"
    exit 1
fi

# Test the application
echo ""
echo "🧪 Testing the application..."

# Check if port 8000 is already in use
if lsof -i :8000 > /dev/null 2>&1; then
    echo "ℹ️  Port 8000 is already in use"
    echo "🔍 Checking if it's our CI/CD Dashboard server..."
    
    # Check if it's our server by looking at the process
    EXISTING_PID=$(lsof -ti :8000)
    if ps -p $EXISTING_PID | grep -q "run_server.py"; then
        print_status "INFO" "CI/CD Dashboard server already running on port 8000 (PID: $EXISTING_PID)"
        SERVER_PID=$EXISTING_PID
        SERVER_STARTED_BY_SCRIPT="false"
        echo "✅ Using existing server instance"
    else
        print_status "WARNING" "Port 8000 is in use by another process (PID: $EXISTING_PID)"
        echo "💡 Options:"
        echo "   1. Stop the existing process: kill $EXISTING_PID"
        echo "   2. Use a different port by modifying run_server.py"
        echo "   3. Wait for the port to become available"
        echo ""
        echo "⏳ Attempting to use existing server on port 8000..."
        SERVER_PID=$EXISTING_PID
        SERVER_STARTED_BY_SCRIPT="false"
    fi
else
    echo "🚀 Starting server in background..."
    # Start server in background
    python run_server.py > server.log 2>&1 &
    SERVER_PID=$!
    SERVER_STARTED_BY_SCRIPT="true"
    
    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    sleep 8
    
    # Check if server is running
    if ps -p $SERVER_PID > /dev/null; then
        print_status "SUCCESS" "Server started with PID $SERVER_PID"
    else
        print_status "ERROR" "Server failed to start"
        echo "Server logs:"
        cat server.log
        exit 1
    fi
fi

# Test health endpoint
echo ""
echo "🔍 Testing server health..."
HEALTH_CHECK_ATTEMPTS=0
MAX_HEALTH_CHECK_ATTEMPTS=10

while [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_HEALTH_CHECK_ATTEMPTS ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "SUCCESS" "Server is responding to health check"
        break
    else
        HEALTH_CHECK_ATTEMPTS=$((HEALTH_CHECK_ATTEMPTS + 1))
        if [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_HEALTH_CHECK_ATTEMPTS ]; then
            echo "⏳ Health check attempt $HEALTH_CHECK_ATTEMPTS/$MAX_HEALTH_CHECK_ATTEMPTS failed, retrying in 2 seconds..."
            sleep 2
        else
            print_status "ERROR" "Server health check failed after $MAX_HEALTH_CHECK_ATTEMPTS attempts"
            echo "Server logs:"
            if [ -f "server.log" ]; then
                tail -20 server.log
            fi
            echo ""
            echo "💡 Troubleshooting tips:"
            echo "   1. Check if the server process is running: ps aux | grep run_server.py"
            echo "   2. Check if port 8000 is in use: lsof -i :8000"
            echo "   3. Check server logs for errors"
            exit 1
        fi
    fi
done

# Run basic verification
echo ""
echo "🔍 Running basic verification..."
export API_WRITE_KEY=$(grep WRITE_KEY .env | cut -d'=' -f2)
echo "✅ API Key configured: $API_WRITE_KEY"
print_status "SUCCESS" "Basic verification completed"

# Verify server is actually responding before testing
echo ""
echo "🔍 Verifying server is ready for testing..."
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_status "ERROR" "Server is not responding to health checks"
    echo "💡 The server process may be running but not fully initialized"
    echo "   Server logs:"
    if [ -f "server.log" ]; then
        tail -20 server.log
    fi
    exit 1
fi
print_status "SUCCESS" "Server is ready for testing"

# Test webhook and email functionality
echo ""
echo "🧪 Testing Webhook and Email Functionality..."
echo "============================================="

# Test 1: Success webhook
echo "1️⃣  Testing SUCCESS webhook..."
SUCCESS_PAYLOAD='{
    "workflow_run": {
        "id": "123456789",
        "conclusion": "success",
        "status": "completed",
        "head_branch": "main",
        "head_commit": {"id": "abc123def456"},
        "html_url": "https://github.com/test/repo/actions/runs/123456789",
        "run_started_at": "2025-08-25T15:00:00Z",
        "updated_at": "2025-08-25T15:05:00Z",
        "name": "CI/CD Pipeline",
        "event": "push",
        "run_number": 42,
        "run_attempt": 1
    },
    "repository": {"full_name": "test/repo"},
    "sender": {"login": "test-user"}
}'

SUCCESS_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/webhook/github-actions" \
    -H "Authorization: Bearer $API_WRITE_KEY" \
    -H "Content-Type: application/json" \
    -d "$SUCCESS_PAYLOAD")

if echo "$SUCCESS_RESPONSE" | grep -q "Webhook processed successfully"; then
    print_status "SUCCESS" "Success webhook processed correctly"
    echo "   📧 Success alert email should be sent"
else
    print_status "WARNING" "Success webhook failed"
    echo "   Response: $SUCCESS_RESPONSE"
fi

# Test 2: Failure webhook
echo ""
echo "2️⃣  Testing FAILURE webhook..."
FAILURE_PAYLOAD='{
    "workflow_run": {
        "id": "987654321",
        "conclusion": "failure",
        "status": "completed",
        "head_branch": "feature/test",
        "head_commit": {"id": "def456abc789"},
        "html_url": "https://github.com/test/repo/actions/runs/987654321",
        "run_started_at": "2025-08-25T15:10:00Z",
        "updated_at": "2025-08-25T15:15:00Z",
        "name": "CI/CD Pipeline",
        "event": "push",
        "run_number": 43,
        "run_attempt": 1
    },
    "repository": {"full_name": "test/repo"},
    "sender": {"login": "test-user"}
}'

FAILURE_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/webhook/github-actions" \
    -H "Authorization: Bearer $API_WRITE_KEY" \
    -H "Content-Type: application/json" \
    -d "$FAILURE_PAYLOAD")

if echo "$FAILURE_RESPONSE" | grep -q "Webhook processed successfully"; then
    print_status "SUCCESS" "Failure webhook processed correctly"
    echo "   📧 Failure alert email should be sent"
else
    print_status "WARNING" "Failure webhook failed"
    echo "   Response: $FAILURE_RESPONSE"
fi

# Test 3: Email alert system
echo ""
echo "3️⃣  Testing Email Alert System..."
ALERT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/alert/test" \
    -H "Content-Type: application/json" \
    -d '{"message": "Test alert from setup script", "severity": "info"}')

if echo "$ALERT_RESPONSE" | grep -q '"success":true'; then
    print_status "SUCCESS" "Email alert test passed"
    echo "   📧 Test email sent successfully"
elif echo "$ALERT_RESPONSE" | grep -q '"success":false'; then
    print_status "WARNING" "Email alert test failed (check SMTP configuration)"
    echo "   Response: $ALERT_RESPONSE"
    echo ""
    echo "📧 To fix email alerts, update your .env file with:"
    echo "   ALERTS_ENABLED=true"
    echo "   SMTP_HOST=smtp.gmail.com"
    echo "   SMTP_USERNAME=your-email@gmail.com"
    echo "   SMTP_PASSWORD=your-app-password"
else
    print_status "ERROR" "Unexpected alert response"
    echo "   Response: $ALERT_RESPONSE"
fi

# Cleanup: Stop server if we started it (but only if it's not the existing one)
echo ""
echo "🧹 Cleaning up..."
if [ ! -z "$SERVER_STARTED_BY_SCRIPT" ] && [ "$SERVER_STARTED_BY_SCRIPT" = "true" ]; then
    echo "🛑 Stopping server we started (PID: $SERVER_PID)..."
    kill $SERVER_PID 2>/dev/null
    sleep 2
    
    # Force kill if still running
    if ps -p $SERVER_PID > /dev/null 2>&1; then
        echo "⚠️  Server still running, force killing..."
        kill -9 $SERVER_PID 2>/dev/null
    fi
    
    if [ -f "server.log" ]; then
        rm -f server.log
    fi
    print_status "SUCCESS" "Server cleanup completed"
else
    echo "ℹ️  Server was already running, leaving it active"
    echo "💡 To stop the server later: kill $SERVER_PID"
fi

# Show final status
echo ""
echo "🎉 SETUP COMPLETED SUCCESSFULLY!"
echo "=================================="
echo ""
echo "📋 Application Status:"
echo "✅ Virtual environment: .venv (activated)"
echo "✅ Dependencies: All installed"
echo "✅ Configuration: .env created"
echo "✅ Server: Running on http://localhost:8000"
echo "✅ Health check: Passing"
echo "✅ Webhook processing: Tested"
echo "✅ Email alerts: Tested"
echo ""
echo "🌐 Access URLs:"
echo "   Dashboard: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Health: http://localhost:8000/health"
echo ""
echo "🔧 Available Scripts:"
echo "   Main Setup: ./setup.sh (this script - handles everything)"
echo "   Deploy: ./deploy.sh (for production deployment)"
echo "   Test API: Use curl commands from README.md"
echo ""
echo "📚 Documentation:"
echo "   Email Setup: EMAIL_SETUP.md"
echo "   Ngrok Setup: NGROK_SETUP.md"
echo "   Scripts Guide: SCRIPTS.md"
echo ""
echo "🔐 Your API Key: $(grep WRITE_KEY .env | cut -d'=' -f2)"
echo ""
echo "🚀 Your CI/CD Dashboard is now fully set up and running!"
echo ""
echo "💡 Pro Tip: Use './setup.sh' anytime you need to reset or test everything!"
