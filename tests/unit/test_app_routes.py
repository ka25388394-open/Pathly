#!/usr/bin/env python3
"""Test FastAPI app routes"""

try:
    print("Loading FastAPI app...")
    from app.main import app
    print("OK: App loaded successfully")

    print("\nChecking routes...")
    route_count = 0
    for route in app.routes:
        print(f"Route: {route}")
        if hasattr(route, 'path'):
            print(f"  Path: {route.path}")
        if hasattr(route, 'methods'):
            print(f"  Methods: {route.methods}")
        if hasattr(route, 'path_regex'):
            print(f"  Path regex: {route.path_regex.pattern}")
        route_count += 1
        print()

    print(f"Total routes found: {route_count}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()