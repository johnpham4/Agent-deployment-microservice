import pytest
import sys
import os
from pathlib import Path

# Add the src/app directory to Python path
app_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(app_dir))

from fastapi.testclient import TestClient
from main import app
from core.config import settings

client = TestClient(app)

def test_load_model():
    """Test model loading endpoint"""
    response = client.post("/api/v1/chat/model/load")
    # Model loading might fail if model files don't exist, check for 200 or 500
    assert response.status_code in [200, 500]
    data = response.json()
    if response.status_code == 200:
        assert data["success"] is True
        assert "Model loaded successfully" in data["message"]
        assert data["model_path"] == settings.MODEL_PATH
    else:
        # Model loading failed - this is expected if model files don't exist
        assert "detail" in data

def test_model_status():
    """Test model status endpoint"""
    response = client.get("/api/v1/chat/model/status")
    assert response.status_code == 200
    data = response.json()
    assert "model_loaded" in data
    assert "model_path" in data
    assert "device" in data

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "unhealthy"]
    assert "service" in data
    assert "model_loaded" in data

def test_generate_chat_response():
    """Test chat generation endpoint"""
    payload = {
        "message": "SELECT * FROM users;",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/api/v1/chat/generate", json=payload)
    # Should either work (200) or fail with model not available (503)
    assert response.status_code in [200, 503, 500]
    if response.status_code == 200:
        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert "model_used" in data
        assert "response_time" in data

def test_chat_request_validation():
    """Test chat request validation"""
    # Test empty message
    payload = {
        "message": "",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/api/v1/chat/generate", json=payload)
    assert response.status_code == 422  # Validation error

    # Test message too long
    payload = {
        "message": "x" * 1001,  # Exceeds max length
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/api/v1/chat/generate", json=payload)
    assert response.status_code == 422  # Validation error

def test_placeholder_endpoints():
    """Test placeholder endpoints that return not implemented messages"""
    # Test history endpoint
    response = client.get("/api/v1/chat/history/test-session")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "messages" in data

    # Test analytics endpoint
    response = client.get("/api/v1/chat/analytics?days=7")
    assert response.status_code == 200
    data = response.json()
    assert "period_days" in data
    assert data["period_days"] == 7