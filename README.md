# 🚀 Attendance Management System - Production Backend

## Overview
This is the Django backend for the Attendance Management System, designed for production deployment.

## 🏗️ Architecture
- **Framework**: Django 5.2.4 with Django REST Framework
- **Database**: MySQL (Production)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API**: RESTful API with role-based access control

## 🚀 Quick Deployment

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Production Settings
- Set `ENVIRONMENT=production` in environment variables
- Configure database credentials
- Set up static file serving
- Configure CORS settings

### 4. Start Server
```bash
# Development
python manage.py runserver

# Production (with Gunicorn)
gunicorn attendance_system.wsgi:application
```

## 📁 Project Structure
```
├── attendance_system/     # Django project settings
├── core/                 # Main application
├── templates/            # Django templates
├── static/              # Static files
├── requirements.txt     # Python dependencies
└── manage.py           # Django management
```

## 🔌 API Endpoints
- Authentication: `/api/auth/`
- Users: `/api/users/`
- Attendance: `/api/attendance/`
- Offices: `/api/offices/`
- Dashboard: `/api/dashboard/`

## 🔐 Security Features
- JWT Authentication
- Role-based permissions
- CORS protection
- Input validation
- SQL injection protection

## 📊 Features
- Multi-office support
- Role-based access control
- Attendance tracking
- Leave management
- Document management
- Real-time notifications

## 🛠️ Maintenance
- Check logs in `/logs/` directory
- Monitor database connections
- Regular backups
- Security updates

---
**Built with Django & DRF** | **Production Ready** 🚀
