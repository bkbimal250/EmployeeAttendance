# 📘 Multi-Dashboard Attendance Management System

A comprehensive **multi-office employee attendance and management platform** built with **Django REST Framework** and **React + Vite + TailwindCSS**.

## 🏗️ System Architecture

This system consists of **three separate dashboards** designed for different user roles:

- **🔧 Admin Dashboard** → `admin.company.com` (System-wide management)
- **👨‍💼 Manager Dashboard** → `manager.company.com` (Office-specific management)
- **👤 Employee Dashboard** → `employee.company.com` (Personal dashboard)

## 🎯 Features

### 🔹 Admin (Superuser)
- ✅ Manage multiple offices (create, edit, delete)
- ✅ Assign managers to offices
- ✅ Configure system-wide settings
- ✅ View global reports and analytics
- ✅ Audit logs & security management
- ✅ Device management across all offices

### 🔹 Manager (Per Office)
- ✅ Access only their assigned office
- ✅ Add/Edit employees within their office
- ✅ Monitor attendance of all employees
- ✅ Approve/Reject leave requests
- ✅ Generate monthly attendance reports
- ✅ Manage biometric devices for their office
- ✅ Modify office details

### 🔹 Employee
- ✅ Login to personal dashboard
- ✅ View daily attendance and monthly summary
- ✅ Apply for leave requests
- ✅ Upload/view documents
- ✅ Update profile information
- ✅ View notifications

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.4
- **API**: Django REST Framework 3.15.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **CORS**: django-cors-headers
- **Admin**: django-jazzmin
- **Background Tasks**: Celery + Redis

### Frontend (Planned)
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: React Context / Redux
- **HTTP Client**: Axios
- **Routing**: React Router

## 📁 Project Structure

```
EmployeeAttandance/
├── attendance_system/          # Django project settings
├── core/                      # Main Django app
│   ├── models.py              # Database models
│   ├── views.py               # API views
│   ├── serializers.py         # API serializers
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin interface
│   └── signals.py             # Automatic notifications
├── frontend/                  # React frontend (separate dashboards)
│   ├── AdminDashboard/
│   ├── ManagerDashboard/
│   └── EmployeeDashboard/
├── media/                     # Uploaded files
├── static/                    # Static files
├── templates/                 # Django templates
├── requirements.txt           # Python dependencies
└── manage.py                 # Django management
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis (for background tasks)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EmployeeAttandance
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (For each dashboard)

1. **Navigate to dashboard directory**
   ```bash
   cd frontend/AdminDashboard  # or ManagerDashboard/EmployeeDashboard
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update profile
- `POST /api/auth/change-password/` - Change password

### Core Resources
- `GET/POST /api/offices/` - Office management
- `GET/POST /api/users/` - User management
- `GET/POST /api/devices/` - Device management
- `GET/POST /api/attendance/` - Attendance records
- `GET/POST /api/leaves/` - Leave management
- `GET/POST /api/documents/` - Document management
- `GET /api/notifications/` - Notifications
- `GET /api/dashboard/stats/` - Dashboard statistics

### JWT Endpoints
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

## 🗄️ Database Models

### Core Models
- **Office**: Multi-office support
- **CustomUser**: Extended user model with roles
- **Device**: Biometric device management
- **Attendance**: Daily attendance tracking
- **Leave**: Leave request management
- **Document**: File upload management
- **Notification**: System notifications
- **SystemSettings**: Configuration settings
- **AttendanceLog**: Audit trail

## 🔐 Authentication & Permissions

### Role-Based Access Control
- **Admin**: Full system access
- **Manager**: Office-specific access
- **Employee**: Personal data access only

### JWT Authentication
- Access tokens (1 hour lifetime)
- Refresh tokens (7 days lifetime)
- Automatic token rotation

## 📊 Features Overview

### ✅ Implemented
- [x] Multi-office architecture
- [x] Role-based user management
- [x] JWT authentication
- [x] RESTful API endpoints
- [x] Admin interface
- [x] Database models
- [x] Automatic notifications
- [x] File upload system
- [x] Attendance tracking
- [x] Leave management
- [x] Device management

### 🚧 In Progress
- [ ] Frontend dashboards
- [ ] Biometric device integration
- [ ] Real-time notifications
- [ ] Advanced reporting
- [ ] Email notifications

### 📋 Planned
- [ ] Department structure
- [ ] Payroll integration
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Multi-language support

## 🛡️ Security Features

- JWT-based authentication
- Role-based permissions
- CORS configuration
- Input validation
- SQL injection protection
- XSS protection
- CSRF protection

## 📈 Deployment

### Development
```bash
python manage.py runserver
```

### Production
1. Set `DEBUG = False`
2. Configure production database
3. Set up static file serving
4. Configure environment variables
5. Use Gunicorn + Nginx

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact: [your-email@example.com]

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added multi-office support
- **v1.2.0** - Enhanced API endpoints
- **v1.3.0** - Added notification system

---

**Built with ❤️ using Django & React**
