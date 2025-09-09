#!/usr/bin/env python3
"""
Test runner script for QA Chatbot API
Run this from the project root directory
"""

import sys
import os
from pathlib import Path

# Add src/app to Python path
project_root = Path(__file__).parent
app_dir = project_root / "src" / "app"
sys.path.insert(0, str(app_dir))

import pytest

def main():
    """Run tests with proper path configuration"""
    print("🧪 Running QA Chatbot API Tests...")
    print(f"Project root: {project_root}")
    print(f"App directory: {app_dir}")

    # Change to app directory
    os.chdir(app_dir)

    # Run tests
    test_file = "chat_service/tests/test_api.py"

    # Run pytest with verbose output
    exit_code = pytest.main([
        test_file,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--no-header",  # No pytest header
    ])

    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())
