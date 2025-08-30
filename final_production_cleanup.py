#!/usr/bin/env python3
"""
Final Production Cleanup
Clean up the project for production deployment
"""

import os
import shutil
import glob

def cleanup_for_production():
    """Clean up the project for production deployment"""
    print("🧹 Final Production Cleanup...")
    
    # Files to remove
    files_to_remove = [
        "verify_production_ready.py",
        "final_production_cleanup.py",
        "db.sqlite3",  # Remove local database
    ]
    
    # Directories to remove
    dirs_to_remove = [
        "frontend",  # Frontend will be deployed separately
        "exports",
        "media",
        "logs",
        "venv",
        "__pycache__",
    ]
    
    # Remove files
    print("📁 Removing development files...")
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"   ✅ Removed: {file_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
    
    # Remove directories
    print("📁 Removing development directories...")
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"   ✅ Removed: {dir_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {dir_path}: {e}")
    
    # Remove __pycache__ directories recursively
    print("📁 Removing Python cache directories...")
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(cache_path)
                    print(f"   ✅ Removed: {cache_path}")
                except Exception as e:
                    print(f"   ❌ Failed to remove {cache_path}: {e}")
    
    # Remove test files
    print("📁 Removing test files...")
    test_patterns = [
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
    ]
    
    for pattern in test_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                print(f"   ✅ Removed: {file_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
    
    # Remove batch and PowerShell files
    print("📁 Removing batch and PowerShell files...")
    for ext in ["*.bat", "*.ps1"]:
        for file_path in glob.glob(ext):
            try:
                os.remove(file_path)
                print(f"   ✅ Removed: {file_path}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
    
    print("\n✅ Production cleanup completed!")
    print("🚀 Your project is ready for GitHub deployment!")

def verify_production_ready():
    """Verify the project is ready for production"""
    print("\n🔍 Verifying production readiness...")
    
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
    
    print("📋 Checking essential files...")
    missing_files = []
    for file_path in essential_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"   ❌ Missing: {file_path}")
        else:
            print(f"   ✅ Found: {file_path}")
    
    # Check for forbidden files
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
    
    print("\n📋 Checking for forbidden files...")
    forbidden_files = []
    for pattern in forbidden_patterns:
        for file_path in glob.glob(pattern):
            forbidden_files.append(file_path)
            print(f"   ❌ Forbidden file found: {file_path}")
    
    # Check for forbidden directories
    forbidden_dirs = []
    dirs_to_check = ["logs", "media", "staticfiles", "venv", "env", "exports", "frontend"]
    for dir_name in dirs_to_check:
        if os.path.exists(dir_name):
            forbidden_dirs.append(dir_name)
            print(f"   ❌ Forbidden directory found: {dir_name}")
    
    # Check for __pycache__ directories
    pycache_dirs = []
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_dirs.append(os.path.join(root, dir_name))
                print(f"   ❌ Python cache found: {os.path.join(root, dir_name)}")
    
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
    
    # Final verdict
    total_issues = len(missing_files) + len(forbidden_files) + len(forbidden_dirs) + len(pycache_dirs)
    
    print("\n" + "="*60)
    if total_issues == 0:
        print("🎉 PRODUCTION READY! ✅")
        print("Your project is ready for GitHub deployment!")
        return True
    else:
        print(f"⚠️ {total_issues} ISSUES FOUND")
        print("Please fix the issues above before deploying.")
        return False

if __name__ == "__main__":
    cleanup_for_production()
    is_ready = verify_production_ready()
    
    if is_ready:
        print("\n🚀 DEPLOYMENT INSTRUCTIONS")
        print("="*60)
        print("1. Commit your changes:")
        print("   git add .")
        print("   git commit -m 'Production ready: JWT authentication fix and cleanup'")
        print("   git push origin main")
        print("\n2. The production server will automatically deploy from GitHub")
        print("\n3. After deployment, test the authentication:")
        print("   - Login to the manager dashboard")
        print("   - Verify API calls work without 401 errors")
        print("   - Check that data is loading properly")
    else:
        print("\n❌ Please fix the issues above before deploying.")
