#!/usr/bin/env python3
"""Simple verification script"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set deployment environment
os.environ["PORT"] = "8000"

try:
    print("Testing basic imports...")
    from app.main import app
    print("OK: Main app imported")

    from fastapi.testclient import TestClient
    client = TestClient(app)
    print("OK: Test client created")

    response = client.get("/health")
    print(f"Health check: {response.status_code} - {response.json()}")

    if response.status_code == 200:
        print("SUCCESS: App is ready for deployment!")
    else:
        print("FAIL: Health check failed")
        sys.exit(1)

except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)