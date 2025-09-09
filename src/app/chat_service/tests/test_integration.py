import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add path để import
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src" / "app"))

import pytest
from fastapi.testclient import TestClient

# Mock transformers trước khi import
transformers_mock = MagicMock()
transformers_mock.AutoModelForCausalLM = Mock()
transformers_mock.AutoTokenizer = Mock()
transformers_mock.pipeline = Mock()

sys.modules['transformers'] = transformers_mock

# Import sau khi mock
from chat_service.dto.models import ChatRequest, ChatResponse, ErrorResponse


class TestChatModels:
    """Test Pydantic models"""

    def test_chat_request_valid(self):
        """Test valid chat request creation"""
        request = ChatRequest(
            message="What is SQL?",
            max_tokens=100,
            temperature=0.5
        )
        assert request.message == "What is SQL?"
        assert request.max_tokens == 100
        assert request.temperature == 0.5
        assert request.session_id is not None

    def test_chat_request_validation(self):
        """Test chat request validation"""
        # Test empty message
        with pytest.raises(ValueError):
            ChatRequest(message="   ")

    def test_chat_response_creation(self):
        """Test chat response creation"""
        response = ChatResponse(
            response="SQL is a programming language...",
            session_id="test-123"
        )
        assert response.response == "SQL is a programming language..."
        assert response.session_id == "test-123"
        assert response.timestamp is not None

    def test_error_response_creation(self):
        """Test error response creation"""
        error = ErrorResponse(
            error="Model not loaded",
            detail="Please wait for model to load"
        )
        assert error.error == "Model not loaded"
        assert error.detail == "Please wait for model to load"


@patch('chat_service.services.chat_service.AutoModelForCausalLM')
@patch('chat_service.services.chat_service.AutoTokenizer')
@patch('chat_service.services.chat_service.pipeline')
class TestChatService:
    """Test chat service với mock transformers"""

    def test_chat_service_creation(self, mock_pipeline, mock_tokenizer, mock_model):
        """Test tạo chat service"""
        from chat_service.services.chat_service import ChatService

        service = ChatService()
        assert service.model is None
        assert service.tokenizer is None
        assert not service.is_model_loaded()

    def test_load_model_mock(self, mock_pipeline, mock_tokenizer, mock_model):
        """Test load model với mock"""
        from chat_service.services.chat_service import ChatService

        # Setup mocks
        mock_model.from_pretrained.return_value = Mock()
        mock_tokenizer.from_pretrained.return_value = Mock()
        mock_pipeline.return_value = Mock()

        service = ChatService()

        # Mock attributes
        service.model = Mock()
        service.tokenizer = Mock()
        service.model_loaded = True  # Set directly

        assert service.is_model_loaded()

    def test_generate_response_mock(self, mock_pipeline, mock_tokenizer, mock_model):
        """Test generate response với mock"""
        from chat_service.services.chat_service import ChatService

        service = ChatService()

        # Setup mock attributes
        mock_tokenizer_instance = Mock()
        mock_tokenizer_instance.apply_chat_template.return_value = "mocked prompt"
        mock_tokenizer_instance.eos_token_id = 2

        mock_pipe = Mock()
        mock_pipe.return_value = [{"generated_text": "mocked prompt assistant SELECT * FROM users;"}]

        service.model = Mock()
        service.tokenizer = mock_tokenizer_instance
        service.pipe = mock_pipe
        service.model_loaded = True

        response = service.generate_response("Show all users")

        # Verify response
        assert isinstance(response, str)
        assert "SELECT * FROM users;" in response


@patch('chat_service.services.chat_service.AutoModelForCausalLM')
@patch('chat_service.services.chat_service.AutoTokenizer')
@patch('chat_service.services.chat_service.pipeline')
class TestAPIEndpoints:
    """Test API endpoints với mock"""

    def setup_method(self):
        """Setup cho mỗi test"""
        # Import main sau khi mock transformers
        from main import app
        self.client = TestClient(app)

    def test_health_endpoint(self, mock_pipeline, mock_tokenizer, mock_model):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data

    def test_model_status_endpoint(self, mock_pipeline, mock_tokenizer, mock_model):
        """Test model status endpoint"""
        response = self.client.get("/model/status")
        assert response.status_code == 200
        data = response.json()
        assert "model_loaded" in data

    @patch('chat_service.api.api.chatService')
    def test_generate_endpoint_with_mock(self, mock_chat_service, mock_pipeline, mock_tokenizer, mock_model):
        """Test generate endpoint với mock service"""
        # Setup mock service
        mock_chat_service.is_model_loaded.return_value = True
        mock_chat_service.generate_response.return_value = "SELECT * FROM users WHERE id = 1;"

        request_data = {
            "message": "Show user with ID 1",
            "max_tokens": 100,
            "temperature": 0.7
        }

        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert "timestamp" in data

    @patch('chat_service.api.api.chatService')
    def test_generate_endpoint_model_not_loaded(self, mock_chat_service, mock_pipeline, mock_tokenizer, mock_model):
        """Test generate endpoint khi model chưa load"""
        # Setup mock service - model not loaded
        mock_chat_service.is_model_loaded.return_value = False

        request_data = {
            "message": "Show all users",
            "max_tokens": 100,
            "temperature": 0.7
        }

        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 500  # Should be 500 because load model will fail

    def test_generate_endpoint_invalid_request(self, mock_pipeline, mock_tokenizer, mock_model):
        """Test generate endpoint với invalid request"""
        request_data = {
            "message": "",  # Empty message (should fail validation)
            "max_tokens": 100,
            "temperature": 0.7
        }

        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 422  # Validation error
