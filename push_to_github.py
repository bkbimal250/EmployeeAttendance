#!/usr/bin/env python3
"""
Push Django Backend to GitHub
This script helps push only the Django backend code to GitHub.
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def push_to_github():
    """Push Django backend to GitHub"""
    
    print("🚀 Preparing to push Django backend to GitHub...")
    print("=" * 50)
    
    # Step 1: Clean repository
    if not run_command("python clean_for_github.py", "Cleaning repository"):
        print("❌ Failed to clean repository. Exiting.")
        return False
    
    # Step 2: Check git status
    if not run_command("git status", "Checking git status"):
        print("❌ Git not initialized or repository not found. Exiting.")
        return False
    
    # Step 3: Add all files
    if not run_command("git add .", "Adding files to git"):
        print("❌ Failed to add files. Exiting.")
        return False
    
    # Step 4: Commit changes
    commit_message = input("Enter commit message (or press Enter for default): ").strip()
    if not commit_message:
        commit_message = "Add Django backend code only - ready for VPS deployment"
    
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        print("❌ Failed to commit changes. Exiting.")
        return False
    
    # Step 5: Push to GitHub
    print("🔄 Pushing to GitHub...")
    print("Note: Make sure you have set up your GitHub repository and remote origin.")
    
    if not run_command("git push origin main", "Pushing to GitHub"):
        print("❌ Failed to push to GitHub.")
        print("Possible issues:")
        print("1. GitHub repository not set up")
        print("2. Remote origin not configured")
        print("3. Authentication issues")
        print("4. Branch name might be different (try 'master' instead of 'main')")
        return False
    
    print("=" * 50)
    print("🎉 Successfully pushed Django backend to GitHub!")
    print("\n📋 Next steps:")
    print("1. Clone the repository on your VPS")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run migrations: python manage.py migrate")
    print("4. Start the server: python manage.py runserver 0.0.0.0:8000")
    print("5. Start attendance service: python manage.py auto_fetch_attendance --daemon")
    
    return True

def check_git_setup():
    """Check if git is properly set up"""
    print("🔍 Checking git setup...")
    
    # Check if git is installed
    if not run_command("git --version", "Checking git installation"):
        print("❌ Git is not installed. Please install git first.")
        return False
    
    # Check if this is a git repository
    if not os.path.exists(".git"):
        print("❌ This is not a git repository.")
        print("Run these commands first:")
        print("git init")
        print("git remote add origin <your-github-repo-url>")
        return False
    
    # Check if remote origin is set
    try:
        result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
        if "origin" not in result.stdout:
            print("❌ Remote origin not configured.")
            print("Run: git remote add origin <your-github-repo-url>")
            return False
    except:
        print("❌ Could not check remote configuration.")
        return False
    
    print("✅ Git setup looks good!")
    return True

if __name__ == "__main__":
    print("🚀 Django Backend GitHub Push Tool")
    print("=" * 50)
    
    # Check git setup first
    if not check_git_setup():
        sys.exit(1)
    
    # Ask for confirmation
    print("\n⚠️  This will:")
    print("1. Remove all frontend files")
    print("2. Remove all test scripts and data files")
    print("3. Keep only Django backend code")
    print("4. Push to GitHub")
    
    confirm = input("\nDo you want to continue? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    # Push to GitHub
    success = push_to_github()
    
    if success:
        print("\n🎉 All done! Your Django backend is now on GitHub.")
    else:
        print("\n❌ Failed to push to GitHub. Please check the errors above.")
        sys.exit(1)
