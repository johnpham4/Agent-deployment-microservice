"""
Pytest configuration for QA Chatbot tests
"""

import sys
import os
from pathlib import Path
import pytest

# Add src/app to Python path
current_dir = Path(__file__).parent
app_dir = current_dir.parent.parent
sys.path.insert(0, str(app_dir))

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Setup test environment"""
    # Set working directory to app directory
    os.chdir(app_dir)

    # Set environment variables if needed
    os.environ.setdefault("TESTING", "true")

    yield

    # Cleanup after tests
    pass
