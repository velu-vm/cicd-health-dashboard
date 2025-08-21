#!/bin/bash

# CI/CD Dashboard Setup Test Script
set -e

echo "🧪 Testing CI/CD Dashboard Setup..."
echo "=================================="

# Check if backend is running
echo "🔍 Checking backend status..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running and healthy"
else
    echo "❌ Backend is not responding"
    echo "💡 Start the backend with: python run_server.py"
    exit 1
fi

# Test all API endpoints
echo ""
echo "🔍 Testing API endpoints..."

echo "📊 Health endpoint:"
curl -s http://localhost:8000/health | jq .

echo ""
echo "📈 Metrics summary:"
curl -s http://localhost:8000/api/metrics/summary | jq .

echo ""
echo "🏗️ Builds list:"
curl -s http://localhost:8000/api/builds | jq '.builds | length' | xargs echo "Total builds:"

# Test webhook authentication
echo ""
echo "🔐 Testing webhook authentication..."

# Load WRITE_KEY from .env
if [ -f .env ]; then
    source .env
    echo "📋 Using WRITE_KEY: $WRITE_KEY"
    
    # Test webhook with authentication
    echo "📡 Testing GitHub webhook..."
    WEBHOOK_RESPONSE=$(curl -s -X POST http://localhost:8000/api/webhook/github-actions \
        -H "Authorization: Bearer $WRITE_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "test": "setup-test",
            "run_id": "999888777",
            "conclusion": "success",
            "head_branch": "main",
            "head_sha": "setup123",
            "actor": {"login": "setup-user"},
            "html_url": "https://github.com/test/repo/actions/runs/999888777",
            "run_started_at": "2025-08-21T15:00:00Z",
            "updated_at": "2025-08-21T15:02:00Z"
        }')
    
    echo "Webhook response: $WEBHOOK_RESPONSE"
    
    # Check if webhook was successful
    if echo "$WEBHOOK_RESPONSE" | grep -q "Webhook processed successfully"; then
        echo "✅ Webhook authentication working"
    else
        echo "❌ Webhook authentication failed"
    fi
else
    echo "❌ .env file not found"
fi

# Test frontend
echo ""
echo "🌐 Testing frontend..."
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible at http://localhost:8080"
else
    echo "⚠️  Frontend not accessible (may need to be started separately)"
fi

# Show current configuration
echo ""
echo "📋 Current Configuration Summary:"
echo "=================================="

if [ -f .env ]; then
    echo "🔐 Environment variables loaded from .env"
    echo "📊 Backend API: http://localhost:8000"
    echo "🌐 Frontend: http://localhost:8080"
    echo "📚 API Docs: http://localhost:8000/docs"
    
    # Show key configuration
    source .env
    echo ""
    echo "🔑 Key Configuration:"
    echo "WRITE_KEY: $WRITE_KEY"
    echo "DATABASE_URL: $DATABASE_URL"
    echo "DEBUG: $DEBUG"
    echo "ALERTS_ENABLED: $ALERTS_ENABLED"
else
    echo "❌ .env file not found"
fi

# Show GitHub secrets needed
echo ""
echo "📝 GitHub Repository Secrets Required:"
echo "======================================"
echo "1. DASHBOARD_WEBHOOK_URL: https://your-ngrok-url/api/webhook/github-actions"
echo "2. DASHBOARD_WRITE_KEY: $WRITE_KEY"
echo ""
echo "💡 Use ngrok to expose localhost:8000:"
echo "   ngrok http 8000"

# Show next steps
echo ""
echo "🚀 Next Steps:"
echo "=============="
echo "1. ✅ Backend is running and tested"
echo "2. 🌐 Expose with ngrok: ngrok http 8000"
echo "3. 🔐 Add GitHub secrets (see above)"
echo "4. 📝 Make a test commit to trigger workflow"
echo "5. 🎯 Watch dashboard update in real-time"
echo ""
echo "📚 For detailed setup: cat SETUP_GUIDE.md"
echo "🔧 For quick start: ./quick-start.sh"

echo ""
echo "🎉 Setup test completed successfully!"
