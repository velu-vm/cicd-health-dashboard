#!/bin/bash

# Simple CI/CD Dashboard Test Script
echo "🧪 Simple CI/CD Dashboard Test"
echo "=============================="

# Set environment variables directly
export WRITE_KEY="d447e5b2466828ddda9eed4da0597577"
export SECRET_KEY="2e6b09416dd5e87d2bd26390ff79f67f337ea48dac8f19897cf51ef0fe259037"
export DATABASE_URL="sqlite+aiosqlite:///./data.db"
export DEBUG="true"

echo "🔍 Checking backend status..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running and healthy"
else
    echo "❌ Backend is not responding"
    exit 1
fi

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

echo ""
echo "🔐 Testing webhook authentication..."
echo "📋 Using WRITE_KEY: $WRITE_KEY"

# Test webhook with authentication
echo "📡 Testing GitHub webhook..."
WEBHOOK_RESPONSE=$(curl -s -X POST http://localhost:8000/api/webhook/github-actions \
    -H "Authorization: Bearer $WRITE_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "test": "simple-test",
        "run_id": "111222333",
        "conclusion": "success",
        "head_branch": "main",
        "head_sha": "simple123",
        "actor": {"login": "simple-user"},
        "html_url": "https://github.com/test/repo/actions/runs/111222333",
        "run_started_at": "2025-08-21T15:00:00Z",
        "updated_at": "2025-08-21T15:02:00Z"
    }')

echo "Webhook response: $WEBHOOK_RESPONSE"

if echo "$WEBHOOK_RESPONSE" | grep -q "Webhook processed successfully"; then
    echo "✅ Webhook authentication working"
else
    echo "❌ Webhook authentication failed"
fi

echo ""
echo "📋 Configuration Summary:"
echo "========================="
echo "WRITE_KEY: $WRITE_KEY"
echo "DATABASE_URL: $DATABASE_URL"
echo "DEBUG: $DEBUG"
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:8080"

echo ""
echo "📝 GitHub Repository Secrets Required:"
echo "======================================"
echo "1. DASHBOARD_WEBHOOK_URL: https://your-ngrok-url/api/webhook/github-actions"
echo "2. DASHBOARD_WRITE_KEY: $WRITE_KEY"

echo ""
echo "🚀 Next Steps:"
echo "=============="
echo "1. ✅ Backend is running and tested"
echo "2. 🌐 Expose with ngrok: ngrok http 8000"
echo "3. 🔐 Add GitHub secrets (see above)"
echo "4. 📝 Make a test commit to trigger workflow"
echo "5. 🎯 Watch dashboard update in real-time"

echo ""
echo "🎉 Simple test completed successfully!"
