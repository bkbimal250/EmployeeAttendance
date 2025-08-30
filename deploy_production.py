#!/usr/bin/env python3
"""
Production Deployment Script for Employee Attendance System
This script prepares the Django application for production deployment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def create_env_file():
    """Create .env file for production"""
    env_content = """# Production Environment Variables
ENVIRONMENT=production
SECRET_KEY=your-production-secret-key-here
DEBUG=False

# Database settings (already configured in settings.py)
# DATABASE_URL=mysql://u434975676_bimal:DishaSolution@8989@193.203.184.215:3306/u434975676_DOS

# CORS settings
CORS_ALLOWED_ORIGINS=https://company.d0s369.co.in,https://www.company.d0s369.co.in

# Security settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file for production")
    else:
        print("ℹ️  .env file already exists")

def main():
    """Main deployment function"""
    print("🚀 Starting Production Deployment...")
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Set environment variables
    os.environ['ENVIRONMENT'] = 'production'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'attendance_system.settings'
    
    # Install/upgrade dependencies
    if not run_command("pip install -r requirements.txt --upgrade", "Installing/upgrading dependencies"):
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    # Run database migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        sys.exit(1)
    
    # Create superuser if needed (optional)
    print("\n🤔 Do you want to create a superuser? (y/n): ", end="")
    create_superuser = input().lower().strip()
    if create_superuser == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Test the application
    print("\n🧪 Testing the application...")
    if not run_command("python manage.py check --deploy", "Running deployment checks"):
        print("⚠️  Deployment checks failed, but continuing...")
    
    # Create production startup script
    startup_script = """#!/bin/bash
# Production Startup Script
export ENVIRONMENT=production
export DJANGO_SETTINGS_MODULE=attendance_system.settings

# Start Gunicorn server
gunicorn attendance_system.wsgi:application \\
    --bind 0.0.0.0:8000 \\
    --workers 4 \\
    --worker-class gunicorn.workers.sync \\
    --worker-connections 1000 \\
    --max-requests 1000 \\
    --max-requests-jitter 100 \\
    --timeout 30 \\
    --keep-alive 2 \\
    --access-logfile logs/gunicorn-access.log \\
    --error-logfile logs/gunicorn-error.log \\
    --log-level info
"""
    
    with open('start_production.sh', 'w') as f:
        f.write(startup_script)
    
    # Make the script executable
    os.chmod('start_production.sh', 0o755)
    print("✅ Created production startup script: start_production.sh")
    
    # Create nginx configuration template
    nginx_config = """# Nginx configuration for Employee Attendance System
server {
    listen 80;
    server_name company.d0s369.co.in www.company.d0s369.co.in;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name company.d0s369.co.in www.company.d0s369.co.in;
    
    # SSL configuration
    ssl_certificate /path/to/your/ssl/certificate.crt;
    ssl_certificate_key /path/to/your/ssl/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Admin interface
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check
    location /health/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Frontend (if serving from Django)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
    
    with open('nginx_config.conf', 'w') as f:
        f.write(nginx_config)
    print("✅ Created nginx configuration template: nginx_config.conf")
    
    print("\n🎉 Production deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your production secret key")
    print("2. Configure your web server (nginx/apache) using nginx_config.conf")
    print("3. Set up SSL certificates")
    print("4. Start the application with: ./start_production.sh")
    print("5. Monitor logs in the logs/ directory")
    print("\n🔧 For troubleshooting, check:")
    print("- logs/django.log for Django errors")
    print("- logs/gunicorn-access.log and logs/gunicorn-error.log for server errors")
    print("- Run 'python manage.py check --deploy' for deployment validation")

if __name__ == "__main__":
    main()
