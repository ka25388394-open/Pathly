#!/usr/bin/env python3
"""Check if application starts correctly"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_imports():
    """Check if critical imports work"""
    try:
        print("Checking config...")
        from app.config import get_settings
        settings = get_settings()
        print(f"OK: Config loaded, port: {settings.app_port}")

        print("Checking main app...")
        from app.main import app
        print("OK: FastAPI app created successfully")

        return True
    except Exception as e:
        print(f"FAIL: Import failed: {e}")
        return False

def check_health_endpoint():
    """Check health endpoint"""
    try:
        from app.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/health")

        if response.status_code == 200:
            print(f"OK: Health endpoint works: {response.json()}")
            return True
        else:
            print(f"FAIL: Health endpoint error: {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL: Health check test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Pathly Startup Check ===")

    # Set environment variables to simulate deployment
    os.environ.setdefault("PORT", "8000")
    os.environ.setdefault("RAILWAY_ENVIRONMENT", "production")

    success = True

    success &= check_imports()
    success &= check_health_endpoint()

    if success:
        print("\nSUCCESS: All checks passed, app should deploy correctly!")
        sys.exit(0)
    else:
        print("\nFAIL: Checks failed, need more debugging")
        sys.exit(1)