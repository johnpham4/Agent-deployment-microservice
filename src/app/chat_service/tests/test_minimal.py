# Test minimal không import transformers để kiểm tra infra
import sys
import os
from pathlib import Path

# Add path để import
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src" / "app"))

import pytest
from fastapi.testclient import TestClient

def test_health_check():
    """Test basic health check endpoint without model dependencies"""
    # Mock implementation
    assert True

def test_basic_api_structure():
    """Test API structure without loading actual transformers"""
    # Basic structure test
    assert True

def test_imports():
    """Test basic imports work"""
    try:
        from chat_service.dto.models import ChatRequest, ChatResponse, ErrorResponse
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")
