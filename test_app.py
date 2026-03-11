"""
Quick test to verify app structure
"""
import sys
print("Python version:", sys.version)

try:
    from fastapi import FastAPI
    print("✅ FastAPI installed")
except ImportError:
    print("❌ FastAPI not installed - run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from backend.main import health_check, get_inventory, get_lineage
    print("✅ Backend functions imported")
except ImportError as e:
    print(f"❌ Backend import error: {e}")
    sys.exit(1)

try:
    from app import app
    print("✅ Main app imported")
    print(f"✅ App has {len(app.routes)} routes")
    
    # List routes
    print("\nAvailable routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  {route.methods if hasattr(route, 'methods') else 'GET'} {route.path}")
    
    print("\n✅ All checks passed!")
except Exception as e:
    print(f"❌ App import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
