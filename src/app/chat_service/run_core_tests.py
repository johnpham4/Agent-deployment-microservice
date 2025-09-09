#!/usr/bin/env python3
"""
Test script chạy tất cả test với mocking để tránh dependency issues
"""

import sys
import os
from pathlib import Path
import pytest

def main():
    """Main test runner"""
    print("🧪 Running QA Chatbot Tests with Mocking...")

    # Setup paths
    project_root = Path(__file__).parent
    app_dir = project_root / "src" / "app"

    print(f"Project root: {project_root}")
    print(f"App directory: {app_dir}")

    # Change to app directory
    os.chdir(app_dir)

    # Add to Python path
    sys.path.insert(0, str(app_dir))

    # Run pytest with specific test files
    test_files = [
        "chat_service/tests/test_integration.py::TestChatModels",
        "chat_service/tests/test_integration.py::TestChatService",
    ]

    pytest_args = [
        "--tb=short",
        "-x",
        *test_files
    ]

    # Run tests
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        print("All tests passed!")
    else:
        print("Some tests failed!")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())
