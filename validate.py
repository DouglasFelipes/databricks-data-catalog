#!/usr/bin/env python3
"""
Validation script for Data Governance Portal
Checks environment and dependencies before deployment
"""
import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not Path('.env').exists():
        print("❌ .env file not found")
        print("   Create it from .env.example: cp .env.example .env")
        return False
    
    required_vars = [
        'DATABRICKS_SERVER_HOSTNAME',
        'DATABRICKS_HTTP_PATH',
        'DATABRICKS_TOKEN'
    ]
    
    from dotenv import load_dotenv
    load_dotenv()
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_frontend_build():
    """Check if frontend is built"""
    build_path = Path('frontend/build')
    if not build_path.exists():
        print("❌ Frontend not built")
        print("   Run: cd frontend && npm install && npm run build")
        return False
    
    print("✅ Frontend build found")
    return True

def check_python_deps():
    """Check if Python dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        from databricks import sql
        import pydantic
        print("✅ Python dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e.name}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_databricks_connection():
    """Test Databricks connection"""
    try:
        from databricks import sql
        from dotenv import load_dotenv
        load_dotenv()
        
        connection = sql.connect(
            server_hostname=os.getenv('DATABRICKS_SERVER_HOSTNAME'),
            http_path=os.getenv('DATABRICKS_HTTP_PATH'),
            access_token=os.getenv('DATABRICKS_TOKEN')
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()
        cursor.close()
        connection.close()
        
        print("✅ Databricks connection successful")
        return True
    except Exception as e:
        print(f"❌ Databricks connection failed: {str(e)}")
        return False

def main():
    print("🔍 Validating Data Governance Portal setup...\n")
    
    checks = [
        ("Environment", check_env_file),
        ("Frontend Build", check_frontend_build),
        ("Python Dependencies", check_python_deps),
        ("Databricks Connection", check_databricks_connection)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append(check_func())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! Ready to deploy.")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
