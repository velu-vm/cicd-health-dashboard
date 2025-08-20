import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "CI/CD Health Dashboard API"
    assert data["version"] == "1.0.0"
    assert "docs" in data

def test_metrics_summary_empty_db():
    """Test metrics summary endpoint with empty database"""
    response = client.get("/api/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["window_days"] == 7
    assert data["success_rate"] == 0.0
    assert data["failure_rate"] == 0.0
    assert data["avg_build_time_seconds"] is None
    assert data["last_build_status"] is None
    assert "last_updated" in data

def test_builds_endpoint_empty_db():
    """Test builds endpoint with empty database"""
    response = client.get("/api/builds")
    assert response.status_code == 200
    data = response.json()
    assert data["builds"] == []
    assert data["total"] == 0
    assert data["limit"] == 50
    assert data["offset"] == 0
    assert data["has_more"] == False

def test_builds_endpoint_with_pagination():
    """Test builds endpoint pagination parameters"""
    response = client.get("/api/builds?limit=10&offset=5")
    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 10
    assert data["offset"] == 5

def test_builds_endpoint_invalid_limit():
    """Test builds endpoint with invalid limit"""
    response = client.get("/api/builds?limit=0")
    assert response.status_code == 422  # Validation error

def test_builds_endpoint_invalid_offset():
    """Test builds endpoint with invalid offset"""
    response = client.get("/api/builds?offset=-1")
    assert response.status_code == 422  # Validation error

def test_build_detail_not_found():
    """Test build detail endpoint with non-existent ID"""
    response = client.get("/api/builds/999")
    assert response.status_code == 404
    assert "Build not found" in response.json()["detail"]

def test_webhook_github_actions():
    """Test GitHub Actions webhook endpoint"""
    payload = {
        "workflow_run": {
            "id": 123456789,
            "conclusion": "success",
            "status": "completed",
            "head_branch": "main",
            "head_sha": "abc123",
            "actor": {"login": "testuser"},
            "html_url": "https://github.com/test/repo/actions/runs/123456789",
            "run_started_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:33:00Z"
        },
        "workflow": {"name": "CI Pipeline"},
        "repository": {"full_name": "test/repo"},
        "sender": {"login": "testuser"}
    }
    
    response = client.post("/api/webhook/github-actions", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "processed"

def test_alert_test_without_key():
    """Test alert test endpoint without API key"""
    payload = {
        "message": "Test message",
        "severity": "info"
    }
    
    response = client.post("/api/alert/test", json=payload)
    assert response.status_code == 401
    assert "X-API-KEY header required" in response.json()["detail"]

def test_seed_without_key():
    """Test seed endpoint without API key"""
    payload = {
        "providers": [{"name": "test-provider", "kind": "github_actions"}]
    }
    
    response = client.post("/api/seed", json=payload)
    assert response.status_code == 401
    assert "X-API-KEY header required" in response.json()["detail"]

def test_docs_endpoint():
    """Test that docs endpoint is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_endpoint():
    """Test that OpenAPI schema is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "CI/CD Health Dashboard API"
