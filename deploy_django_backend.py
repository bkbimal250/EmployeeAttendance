#!/usr/bin/env python3
"""
Django Backend Deployment Script
This script deploys only the Django backend to your server.
Frontend will be hosted separately.
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
    env_content = """# Production Environment Variables for Django Backend
ENVIRONMENT=production
DEBUG=False

# Django Secret Key (Generate a new one!)
SECRET_KEY=your-production-secret-key-here-change-this-immediately

# Database settings (already configured in settings.py)
# DATABASE_URL=mysql://u434975676_bimal:DishaSolution@8989@193.203.184.215:3306/u434975676_DOS

# CORS settings for your frontend domains
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
    print("🚀 Starting Django Backend Deployment...")
    print("📝 Note: Frontend will be hosted separately")
    
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
# Django Backend Production Startup Script
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
    
    with open('start_django_backend.sh', 'w') as f:
        f.write(startup_script)
    
    # Make the script executable
    os.chmod('start_django_backend.sh', 0o755)
    print("✅ Created Django backend startup script: start_django_backend.sh")
    
    # Create nginx configuration for API only
    nginx_config = """# Nginx configuration for Django Backend API
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
    
    # Static files (for admin interface)
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
        
        # CORS headers for frontend
        add_header Access-Control-Allow-Origin $http_origin always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization, X-Requested-With" always;
        add_header Access-Control-Allow-Credentials true always;
        
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin $http_origin;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "Content-Type, Authorization, X-Requested-With";
            add_header Access-Control-Allow-Credentials true;
            add_header Content-Length 0;
            add_header Content-Type text/plain;
            return 204;
        }
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
    
    # JWT token endpoints
    location /api/token/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header Access-Control-Allow-Origin $http_origin always;
        add_header Access-Control-Allow-Methods "POST, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
        add_header Access-Control-Allow-Credentials true always;
    }
    
    # Redirect root to frontend (if needed)
    location / {
        return 301 https://your-frontend-domain.com;
    }
}
"""
    
    with open('nginx_django_backend.conf', 'w') as f:
        f.write(nginx_config)
    print("✅ Created nginx configuration for Django backend: nginx_django_backend.conf")
    
    # Create systemd service file
    systemd_service = """[Unit]
Description=Django Backend API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment=ENVIRONMENT=production
Environment=DJANGO_SETTINGS_MODULE=attendance_system.settings
ExecStart=/path/to/your/venv/bin/gunicorn attendance_system.wsgi:application --bind 127.0.0.1:8000 --workers 4 --worker-class gunicorn.workers.sync --worker-connections 1000 --max-requests 1000 --max-requests-jitter 100 --timeout 30 --keep-alive 2 --access-logfile logs/gunicorn-access.log --error-logfile logs/gunicorn-error.log --log-level info
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
    
    with open('django-backend.service', 'w') as f:
        f.write(systemd_service)
    print("✅ Created systemd service file: django-backend.service")
    
    print("\n🎉 Django Backend deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the .env file with your production secret key")
    print("2. Copy nginx_django_backend.conf to /etc/nginx/sites-available/")
    print("3. Copy django-backend.service to /etc/systemd/system/")
    print("4. Set up SSL certificates")
    print("5. Start the service with: ./start_django_backend.sh")
    print("6. Monitor logs in the logs/ directory")
    print("\n🔧 For troubleshooting, check:")
    print("- logs/django.log for Django errors")
    print("- logs/gunicorn-access.log and logs/gunicorn-error.log for server errors")
    print("- Run 'python manage.py check --deploy' for deployment validation")
    print("\n🌐 API Endpoints:")
    print("- Health Check: https://company.d0s369.co.in/health/")
    print("- API Base: https://company.d0s369.co.in/api/")
    print("- Admin: https://company.d0s369.co.in/admin/")
    print("- JWT Token: https://company.d0s369.co.in/api/token/")

if __name__ == "__main__":
    main()
