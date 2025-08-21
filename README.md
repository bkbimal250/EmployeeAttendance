# Employee Attendance Management System

A comprehensive Django REST API + React frontend for managing employee attendance with biometric device integration, leave management, document uploads, chat system, and real-time notifications.

## 🆕 **New Features Added:**

- **👤 User Activities Tracking**: Monitor all user actions (login, clock in/out, document uploads, etc.)
- **📄 Document Management**: Upload, share, and manage documents with categories
- **💬 Chat System**: Real-time messaging between users
- **📧 Email Notifications**: Automatic email alerts for leave approvals, document sharing, etc.
- **📊 Enhanced Dashboard**: Comprehensive statistics and reports
- **👥 Admin Document Sharing**: Admins can share documents with multiple users
- **📅 Joining Date**: Track when users joined the organization
- **🔔 Real-time Notifications**: In-app and email notifications
- **📈 Activity Logs**: Detailed user activity tracking with IP addresses
- **⚛️ React Frontend**: Modern admin dashboard with Material-UI

## Features

- **User Management**: Custom user model with roles (user/superuser) and joining dates
- **Department Management**: Organize users by departments
- **Attendance Tracking**: Real-time attendance from biometric devices
- **Leave Management**: Apply, approve, and reject leave requests with email notifications
- **Document Upload & Sharing**: Secure file uploads with admin-to-user sharing
- **Chat System**: User-to-user messaging with read status
- **Notifications**: Email and in-app notifications for all activities
- **Dashboard**: Comprehensive statistics and reports for admins and users
- **Biometric Integration**: Support for ESSL/ZKTeco devices
- **Background Tasks**: Celery for automated tasks and notifications
- **User Activities**: Complete audit trail of all user actions
- **React Admin Dashboard**: Modern, responsive frontend interface

## Tech Stack

### Backend
- **Django 5.2.4**: Web framework
- **Django REST Framework**: API development
- **MySQL**: Database
- **Celery + Redis**: Background tasks
- **Jazzmin**: Admin interface styling

### Frontend
- **React 18**: Modern React with hooks
- **Material-UI (MUI)**: Professional UI components
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing
- **Recharts**: Data visualization

## Quick Start

### 1. Backend Setup

```bash
# Clone and setup backend
cd EmployeeAttandance

# Create and activate virtual environment
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup MySQL database
python test_mysql.py

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

### 3. Access the Application

- **Django Admin**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/
- **React Dashboard**: http://localhost:3000/

## Installation (Detailed)

### Backend Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EmployeeAttandance
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL Database**
   ```bash
   # Create database (if not exists)
   python test_mysql.py
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Start Celery worker (in a new terminal)**
   ```bash
   celery -A EmployeeAttandance worker -l info
   ```

9. **Start Celery beat (in another terminal)**
   ```bash
   celery -A EmployeeAttandance beat -l info
   ```

### Frontend Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

## Database Configuration

The system is configured to use MySQL with the following settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'attendance_db',
        'USER': 'root',
        'PASSWORD': 'DishaSolution@8989',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## API Endpoints

### Authentication
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login
- `POST /api/auth/token/` - Get authentication token

### Users
- `GET /api/users/` - List users (admin only)
- `POST /api/users/` - Create user (admin only)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user (admin only)
- `DELETE /api/users/{id}/` - Delete user (admin only)
- `GET /api/users/profile/` - Get current user profile
- `PUT /api/users/update_profile/` - Update current user profile
- `GET /api/users/list_for_chat/` - List users for chat selection

### Departments
- `GET /api/departments/` - List departments
- `POST /api/departments/` - Create department (admin only)
- `GET /api/departments/{id}/` - Get department details
- `PUT /api/departments/{id}/` - Update department (admin only)
- `DELETE /api/departments/{id}/` - Delete department (admin only)

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Create attendance record
- `GET /api/attendance/{id}/` - Get attendance details
- `POST /api/attendance/clock_in/` - Clock in
- `POST /api/attendance/clock_out/` - Clock out
- `GET /api/attendance/today_status/` - Get today's attendance status

### Leaves
- `GET /api/leaves/` - List leave requests
- `POST /api/leaves/` - Apply for leave
- `GET /api/leaves/{id}/` - Get leave details
- `PUT /api/leaves/{id}/` - Update leave request
- `DELETE /api/leaves/{id}/` - Delete leave request
- `POST /api/leaves/{id}/approve/` - Approve leave (admin only)
- `POST /api/leaves/{id}/reject/` - Reject leave (admin only)

### Documents
- `GET /api/documents/` - List documents
- `POST /api/documents/` - Upload document
- `GET /api/documents/{id}/` - Get document details
- `PUT /api/documents/{id}/` - Update document
- `DELETE /api/documents/{id}/` - Delete document
- `POST /api/documents/share_document/` - Share document with users (admin only)

### Chat System
- `GET /api/chat-rooms/` - List chat rooms
- `POST /api/chat-rooms/create_room/` - Create new chat room
- `GET /api/chat-messages/` - List chat messages
- `POST /api/chat-messages/` - Send chat message
- `GET /api/chat-messages/room_messages/` - Get messages for specific room

### Notifications
- `GET /api/notifications/` - List notifications
- `GET /api/notifications/{id}/` - Get notification details
- `POST /api/notifications/{id}/mark_as_read/` - Mark notification as read
- `POST /api/notifications/mark_all_as_read/` - Mark all notifications as read

### User Activities
- `GET /api/user-activities/` - List user activities
- `GET /api/user-activities/{id}/` - Get activity details

### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics
- `POST /api/dashboard/attendance_report/` - Generate attendance report

## Frontend Features

### Dashboard
- **Statistics Cards**: Total users, today's attendance, pending leaves, departments
- **Recent Activities**: Latest attendance records and notifications
- **Quick Actions**: Direct links to common tasks

### User Management
- **User List**: View all users with their details
- **User Cards**: Display user information in an organized layout
- **Status Indicators**: Active/inactive user status

### Department Management
- **Department List**: View all departments
- **Department Cards**: Display department information
- **User Count**: Number of users per department

### Navigation
- **Sidebar Menu**: Easy navigation between sections
- **Responsive Design**: Collapsible sidebar on mobile
- **Active State**: Visual indication of current section

## Usage Examples

### User Registration with Joining Date
```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "phone": "+1234567890",
    "employee_id": "EMP001",
    "joining_date": "2024-01-01"
  }'
```

### Upload Document
```bash
curl -X POST http://localhost:8000/api/documents/ \
  -H "Authorization: Token your-token-here" \
  -F "document_type=aadhaar" \
  -F "title=Aadhaar Card" \
  -F "description=My Aadhaar card" \
  -F "file=@/path/to/aadhaar.pdf"
```

### Create Chat Room
```bash
curl -X POST http://localhost:8000/api/chat-rooms/create_room/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "participant_ids": ["user-uuid-1", "user-uuid-2"]
  }'
```

### Send Chat Message
```bash
curl -X POST http://localhost:8000/api/chat-messages/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": "room-uuid",
    "message": "Hello! How are you?"
  }'
```

### Admin Share Document
```bash
curl -X POST http://localhost:8000/api/documents/share_document/ \
  -H "Authorization: Token admin-token-here" \
  -F "document_type=company_policy" \
  -F "title=New Company Policy" \
  -F "description=Updated company policy document" \
  -F "file=@/path/to/policy.pdf" \
  -F "recipient_ids=[\"user-uuid-1\", \"user-uuid-2\"]"
```

## Email Notifications

The system automatically sends email notifications for:
- Leave approvals/rejections
- Document sharing
- Attendance anomalies
- Chat messages (optional)
- Daily summaries (for admins)

Configure email settings in your environment:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Background Tasks

The system uses Celery for background tasks:

- **Biometric Data Sync**: Every 30 seconds
- **Attendance Anomaly Check**: Every hour
- **Notification Sending**: Every 5 minutes
- **Daily Summary**: Every day at midnight
- **Data Cleanup**: Every week

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage:
- Users and departments
- Attendance records
- Leave requests
- Documents (with sharing capabilities)
- Notifications (with email resend)
- Chat rooms and messages
- User activities

## API Documentation

Interactive API documentation is available at `http://localhost:8000/api/docs/`

## Testing

Run the enhanced test script to test all features:
```bash
python test_enhanced_api.py
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure MySQL with proper credentials
3. Set up Redis for Celery
4. Configure proper email settings
5. Use a production web server (Gunicorn + Nginx)
6. Configure static file serving
7. Set up SSL/TLS certificates
8. Configure proper security headers
9. Build React frontend: `cd frontend && npm run build`
10. Serve React build files through Django or a separate web server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
#   E m p l o y e e A t t e n d a n c e  
 