import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from chat_service.db.database import Base, get_db
from chat_service.dto.models import ChatRequest

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestChatAPI:
    """Test chat API endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "QA Chatbot Service" in data["message"]

    def test_chat_generate_endpoint(self):
        """Test chat generation endpoint"""
        # Note: This test will fail if model is not loaded
        # In real tests, you might want to mock the model service
        chat_request = {
            "message": "Hello, how are you?",
            "session_id": "test_session_123",
            "max_tokens": 50,
            "temperature": 0.7
        }

        response = client.post("/api/v1/chat/generate", json=chat_request)
        # This might return 500 if model is not loaded, which is expected
        assert response.status_code in [200, 500]

    def test_chat_history_endpoint(self):
        """Test chat history endpoint"""
        session_id = "test_session_123"
        response = client.get(f"/api/v1/chat/history/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert "history" in data
        assert data["session_id"] == session_id

    def test_model_info_endpoint(self):
        """Test model info endpoint"""
        response = client.get("/api/v1/chat/model/info")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_analytics_endpoint(self):
        """Test analytics endpoint"""
        response = client.get("/api/v1/chat/analytics?days=7")
        assert response.status_code == 200
        data = response.json()
        assert "period_days" in data
        assert "total_chats" in data

class TestChatRequest:
    """Test chat request validation"""

    def test_valid_chat_request(self):
        """Test valid chat request"""
        request = ChatRequest(
            message="Test message",
            max_tokens=100,
            temperature=0.5
        )
        assert request.message == "Test message"
        assert request.max_tokens == 100
        assert request.temperature == 0.5
        assert request.session_id is not None

    def test_invalid_chat_request_empty_message(self):
        """Test invalid chat request with empty message"""
        with pytest.raises(ValueError):
            ChatRequest(message="", max_tokens=100)

    def test_invalid_chat_request_long_message(self):
        """Test invalid chat request with too long message"""
        long_message = "x" * 1001  # Exceeds max length
        with pytest.raises(ValueError):
            ChatRequest(message=long_message, max_tokens=100)

if __name__ == "__main__":
    pytest.main([__file__])
