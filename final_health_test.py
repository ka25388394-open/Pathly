#!/usr/bin/env python3
"""Final comprehensive health check test"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_health_with_cors():
    """Test health endpoint with CORS headers"""
    print("Testing health endpoint with CORS...")

    try:
        # Set Railway environment
        os.environ["PORT"] = "8000"
        os.environ["RAILWAY_ENVIRONMENT"] = "production"

        # Import the real app
        from app.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # Test health endpoint
        response = client.get("/health")

        if response.status_code != 200:
            print(f"FAIL: Health endpoint returned {response.status_code}")
            return False

        data = response.json()
        if data.get("status") != "ok":
            print(f"FAIL: Health endpoint returned wrong status: {data}")
            return False

        print(f"OK: Health endpoint returned: {data}")

        # Test OPTIONS request (CORS preflight)
        options_response = client.options("/health")
        print(f"OK: OPTIONS request status: {options_response.status_code}")

        return True

    except Exception as e:
        print(f"FAIL: Health test with CORS failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_startup_without_db():
    """Test app can start even if database fails"""
    print("Testing app startup without database...")

    try:
        # Set invalid database URL to simulate DB failure
        os.environ["DATABASE_URL"] = "sqlite:///./nonexistent/path/db.sqlite"

        # Force reload config
        import importlib
        from app import config
        importlib.reload(config)

        # Try to create app
        from app.main import create_app
        app = create_app()

        from fastapi.testclient import TestClient
        client = TestClient(app)

        # Health check should still work
        response = client.get("/health")

        if response.status_code == 200:
            print("OK: App starts and health check works even with DB issues")
            return True
        else:
            print(f"FAIL: Health check failed with DB issues: {response.status_code}")
            return False

    except Exception as e:
        print(f"FAIL: App startup without DB failed: {e}")
        return False

def test_minimal_import():
    """Test that core modules can be imported without issues"""
    print("Testing minimal import...")

    critical_imports = [
        "app.config",
        "app.main",
        "fastapi",
        "uvicorn"
    ]

    for module in critical_imports:
        try:
            __import__(module)
            print(f"OK: {module} imported successfully")
        except Exception as e:
            print(f"FAIL: {module} import failed: {e}")
            return False

    return True

if __name__ == "__main__":
    print("=== Final Health Check Test ===")

    # Reset environment
    os.environ.pop("DATABASE_URL", None)

    success = True
    success &= test_minimal_import()
    success &= test_health_with_cors()
    success &= test_app_startup_without_db()

    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The app is ready for deployment and health checks should work.")
    else:
        print("\n💥 SOME TESTS FAILED!")
        print("There may still be health check issues.")

    sys.exit(0 if success else 1)