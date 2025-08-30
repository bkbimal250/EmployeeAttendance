#!/usr/bin/env python3
"""
Verify Production Readiness
Check if the project is ready for production deployment
"""

import os
import glob

def verify_production_ready():
    """Verify the project is ready for production"""
    print("🔍 Verifying production readiness...")
    
    # Essential files that must exist
    essential_files = [
        "manage.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "attendance_system/__init__.py",
        "attendance_system/settings.py",
        "attendance_system/urls.py",
        "attendance_system/wsgi.py",
        "core/__init__.py",
        "core/models.py",
        "core/views.py",
        "core/urls.py",
        "core/admin.py",
        "core/middleware.py",
    ]
    
    # Files that should NOT exist (development files)
    forbidden_patterns = [
        "test_*.py",
        "*_test.py",
        "debug_*.py",
        "check_*.py",
        "clear_*.py",
        "fetch_*.py",
        "generate_*.py",
        "quick_*.py",
        "reset_*.py",
        "setup_*.py",
        "sync_*.py",
        "add_*.py",
        "create_*.py",
        "run_*.py",
        "complete_*.py",
        "fix_*.py",
        "manage_*.py",
        "clean_*.py",
        "deploy_*.py",
        "push_*.py",
        "*.bat",
        "*.ps1",
        "*.log",
        "*.db",
        "*.sqlite3",
        "db.sqlite3",
    ]
    
    print("\n📋 Checking essential files...")
    missing_files = []
    for file_path in essential_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    print("\n📋 Checking for forbidden files...")
    forbidden_files = []
    for pattern in forbidden_patterns:
        for file_path in glob.glob(pattern):
            forbidden_files.append(file_path)
            print(f"❌ Forbidden file found: {file_path}")
    
    print("\n📋 Checking directories...")
    forbidden_dirs = []
    dirs_to_check = ["logs", "media", "staticfiles", "venv", "env", "exports"]
    for dir_name in dirs_to_check:
        if os.path.exists(dir_name):
            forbidden_dirs.append(dir_name)
            print(f"❌ Forbidden directory found: {dir_name}")
    
    # Check for __pycache__ directories
    pycache_dirs = []
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dirs.append(os.path.join(root, dir_name))
                print(f"❌ Python cache found: {os.path.join(root, dir_name)}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 PRODUCTION READINESS SUMMARY")
    print("="*60)
    
    if missing_files:
        print(f"❌ Missing {len(missing_files)} essential files")
    else:
        print("✅ All essential files present")
    
    if forbidden_files:
        print(f"❌ Found {len(forbidden_files)} forbidden files")
    else:
        print("✅ No forbidden files found")
    
    if forbidden_dirs:
        print(f"❌ Found {len(forbidden_dirs)} forbidden directories")
    else:
        print("✅ No forbidden directories found")
    
    if pycache_dirs:
        print(f"❌ Found {len(pycache_dirs)} Python cache directories")
    else:
        print("✅ No Python cache directories found")
    
    # Frontend directory check
    if os.path.exists("frontend"):
        print("⚠️ Frontend directory still present (will be deployed separately)")
    else:
        print("✅ Frontend directory removed")
    
    # Final verdict
    total_issues = len(missing_files) + len(forbidden_files) + len(forbidden_dirs) + len(pycache_dirs)
    
    print("\n" + "="*60)
    if total_issues == 0:
        print("🎉 PRODUCTION READY! ✅")
        print("Your project is ready for GitHub deployment!")
    else:
        print(f"⚠️ {total_issues} ISSUES FOUND")
        print("Please fix the issues above before deploying.")
    
    print("="*60)
    
    return total_issues == 0

def show_deployment_instructions():
    """Show deployment instructions"""
    print("\n🚀 DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    print("1. Commit your changes:")
    print("   git add .")
    print("   git commit -m 'Production ready: Cleaned project for deployment'")
    print("   git push origin main")
    print("\n2. On your production server:")
    print("   git clone <your-repository-url>")
    print("   cd EmployeeAttandance")
    print("   python -m venv venv")
    print("   source venv/bin/activate")
    print("   pip install -r requirements.txt")
    print("   export ENVIRONMENT=production")
    print("   python manage.py migrate")
    print("   python manage.py collectstatic --noinput")
    print("   gunicorn attendance_system.wsgi:application")
    print("\n3. Frontend deployment:")
    print("   Deploy frontend separately to your hosting service")
    print("   (e.g., Vercel, Netlify, or your own server)")

if __name__ == "__main__":
    is_ready = verify_production_ready()
    if is_ready:
        show_deployment_instructions()
    else:
        print("\n❌ Please fix the issues above before deploying.")
