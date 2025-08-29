#!/usr/bin/env python3
"""
Clean Repository for GitHub Push
This script helps prepare the repository for GitHub by removing frontend files
and keeping only Django backend code.
"""

import os
import shutil
import subprocess
from pathlib import Path

def clean_repository():
    """Clean repository for GitHub push - Django backend only"""
    
    print("🧹 Cleaning repository for GitHub push (Django backend only)...")
    
    # Files and folders to remove
    items_to_remove = [
        'frontend/',
        'src/',
        'public/',
        'static/',
        'exports/',
        'venv/',
        'logs/',
        'media/',
        'db.sqlite3',
        'node_modules/',
        'dist/',
        'build/',
    ]
    
    # Remove directories and files
    for item in items_to_remove:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"✅ Removed directory: {item}")
            else:
                os.remove(item)
                print(f"✅ Removed file: {item}")
        else:
            print(f"ℹ️  Not found: {item}")
    
    # Remove all CSV files
    csv_files = list(Path('.').glob('*.csv'))
    for csv_file in csv_files:
        os.remove(csv_file)
        print(f"✅ Removed CSV file: {csv_file}")
    
    # Remove all test and utility scripts
    script_patterns = [
        'test_*.py',
        '*_test.py',
        '*_credentials_*.py',
        '*_diagnostic.py',
        'export_*.py',
        'start_*.py',
        'check_*.py',
        'clear_*.py',
        'fetch_*.py',
        'generate_*.py',
        'quick_*.py',
        'reset_*.py',
        'setup_*.py',
        'sync_*.py',
        '*.bat',
        '*.ps1',
    ]
    
    for pattern in script_patterns:
        files = list(Path('.').glob(pattern))
        for file in files:
            if file.name != 'clean_for_github.py':  # Don't remove this script
                os.remove(file)
                print(f"✅ Removed script: {file}")
    
    print("\n🎉 Repository cleaned successfully!")
    print("\n📁 Remaining Django backend structure:")
    
    # Show remaining structure
    def show_structure(path, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(os.listdir(path))
            for i, item in enumerate(items):
                if item.startswith('.') or item in ['__pycache__', '.git']:
                    continue
                    
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1
                
                if os.path.isdir(item_path):
                    print(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
                    if current_depth < max_depth - 1:
                        show_structure(item_path, 
                                     prefix + ('    ' if is_last else '│   '), 
                                     max_depth, current_depth + 1)
                else:
                    print(f"{prefix}{'└── ' if is_last else '├── '}{item}")
        except PermissionError:
            pass
    
    show_structure('.')
    
    print("\n🚀 Ready for GitHub push!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Add Django backend code only'")
    print("3. git push origin main")

def restore_frontend():
    """Restore frontend files (if needed)"""
    print("⚠️  This will restore frontend files from git history")
    response = input("Are you sure? (y/N): ")
    if response.lower() == 'y':
        subprocess.run(['git', 'checkout', 'HEAD', '--', 'frontend/'])
        print("✅ Frontend files restored")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--restore':
        restore_frontend()
    else:
        clean_repository()
