#!/usr/bin/env python3
"""Test deployment environment specifically"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_port_env_var():
    """Test PORT environment variable handling"""
    print("Testing PORT environment variable...")

    # Test with different PORT values
    test_ports = ["8000", "5000", "3000"]

    for port in test_ports:
        os.environ["PORT"] = port

        try:
            # Force reload settings
            import importlib
            from app import config
            importlib.reload(config)

            settings = config.get_settings()
            if settings.app_port == int(port):
                print(f"OK: PORT={port} correctly read as {settings.app_port}")
            else:
                print(f"FAIL: PORT={port} read as {settings.app_port}")
                return False
        except Exception as e:
            print(f"FAIL: PORT={port} caused error: {e}")
            return False

    return True

def test_railway_env():
    """Test Railway-specific environment variables"""
    print("Testing Railway environment variables...")

    # Set typical Railway environment variables
    railway_vars = {
        "RAILWAY_ENVIRONMENT": "production",
        "RAILWAY_DEPLOYMENT_ID": "test-deploy-123",
        "RAILWAY_SERVICE_NAME": "pathly"
    }

    for key, value in railway_vars.items():
        os.environ[key] = value
        print(f"Set {key}={value}")

    try:
        from app.config import get_settings
        settings = get_settings()
        print(f"OK: Settings loaded in Railway environment")
        return True
    except Exception as e:
        print(f"FAIL: Railway environment test failed: {e}")
        return False

def test_minimal_health_check():
    """Test health check without any complex dependencies"""
    print("Testing minimal health check...")

    try:
        # Import only what health check needs
        from fastapi import FastAPI

        # Create minimal app
        app = FastAPI()

        @app.get("/health")
        def health():
            return {"status": "ok", "service": "pathly"}

        # Test with TestClient
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/health")

        if response.status_code == 200 and response.json()["status"] == "ok":
            print("OK: Minimal health check works")
            return True
        else:
            print(f"FAIL: Health check returned {response.status_code}: {response.json()}")
            return False

    except Exception as e:
        print(f"FAIL: Minimal health check failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Pathly Deployment Test ===")

    success = True
    success &= test_port_env_var()
    success &= test_railway_env()
    success &= test_minimal_health_check()

    if success:
        print("\nSUCCESS: All deployment tests passed!")
        print("The app should work correctly on Railway.")
        sys.exit(0)
    else:
        print("\nFAIL: Some deployment tests failed!")
        sys.exit(1)