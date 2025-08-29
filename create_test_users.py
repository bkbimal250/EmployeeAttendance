#!/usr/bin/env python3
"""
Create test users for each role to test role-based dashboard access
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import CustomUser, Office

def create_test_users():
    """Create test users for each role"""
    
    print("🚀 Creating test users for role-based dashboard access...")
    print("=" * 60)
    
    # Get or create an office
    office, created = Office.objects.get_or_create(
        name="Test Office",
        defaults={
            'address': "123 Test Street, Test City, Test State 12345",
            'phone': "+1-555-0000",
            'email': "test@company.com"
        }
    )
    
    # Create Admin user
    admin_user, created = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@company.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'phone': '+1-555-0001',
            'employee_id': 'ADM001'
        }
    )
    if created:
        admin_user.set_password('admin')
        admin_user.save()
        print("✅ Created admin user: admin / admin")
    else:
        admin_user.set_password('admin')
        admin_user.save()
        print("✅ Updated admin user: admin / admin")
    
    # Create Manager user
    try:
        manager_user = CustomUser.objects.get(username='manager')
        manager_user.email = 'manager@company.com'
        manager_user.first_name = 'Manager'
        manager_user.last_name = 'User'
        manager_user.role = 'manager'
        manager_user.office = office
        manager_user.phone = '+1-555-0002'
        manager_user.employee_id = 'MGR003'
        manager_user.set_password('manager')
        manager_user.save()
        print("✅ Updated manager user: manager / manager")
    except CustomUser.DoesNotExist:
        manager_user = CustomUser.objects.create(
            username='manager',
            email='manager@company.com',
            first_name='Manager',
            last_name='User',
            role='manager',
            office=office,
            phone='+1-555-0002',
            employee_id='MGR003'
        )
        manager_user.set_password('manager')
        manager_user.save()
        print("✅ Created manager user: manager / manager")
    
    # Create Employee user
    try:
        employee_user = CustomUser.objects.get(username='employee')
        employee_user.email = 'employee@company.com'
        employee_user.first_name = 'Employee'
        employee_user.last_name = 'User'
        employee_user.role = 'employee'
        employee_user.office = office
        employee_user.phone = '+1-555-0003'
        employee_user.employee_id = 'EMP005'
        employee_user.set_password('employee')
        employee_user.save()
        print("✅ Updated employee user: employee / employee")
    except CustomUser.DoesNotExist:
        employee_user = CustomUser.objects.create(
            username='employee',
            email='employee@company.com',
            first_name='Employee',
            last_name='User',
            role='employee',
            office=office,
            phone='+1-555-0003',
            employee_id='EMP005'
        )
        employee_user.set_password('employee')
        employee_user.save()
        print("✅ Created employee user: employee / employee")
    
    print("\n" + "=" * 60)
    print("🎯 Test Users Created Successfully!")
    print("=" * 60)
    print("📋 Login Credentials:")
    print("   Admin Dashboard: admin / admin")
    print("   Manager Dashboard: manager / manager")
    print("   Employee Dashboard: employee / employee")
    print("\n🔒 Role-Based Access:")
    print("   • Admin can only login to Admin Dashboard")
    print("   • Manager can only login to Manager Dashboard")
    print("   • Employee can only login to Employee Dashboard")
    print("=" * 60)

if __name__ == '__main__':
    create_test_users()
