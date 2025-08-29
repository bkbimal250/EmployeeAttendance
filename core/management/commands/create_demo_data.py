from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import date, timedelta
import random
from core.models import Office, CustomUser, Device, Attendance, Leave


class Command(BaseCommand):
    help = 'Create demo data with 3 offices, managers, employees, and devices'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        # Office.objects.all().delete()
        # CustomUser.objects.filter(role__in=['manager', 'employee']).delete()
        # Device.objects.all().delete()
        
        # Create 3 Offices
        offices = []
        office_data = [
            {
                'name': 'Head Office - Mumbai',
                'address': '123 Business Park, Andheri West, Mumbai, Maharashtra 400058',
                'phone': '+91-22-12345678',
                'email': 'mumbai@company.com'
            },
            {
                'name': 'Branch Office - Delhi',
                'address': '456 Corporate Tower, Connaught Place, New Delhi, Delhi 110001',
                'phone': '+91-11-87654321',
                'email': 'delhi@company.com'
            },
            {
                'name': 'Development Center - Bangalore',
                'address': '789 Tech Park, Electronic City, Bangalore, Karnataka 560100',
                'phone': '+91-80-11223344',
                'email': 'bangalore@company.com'
            }
        ]
        
        for office_info in office_data:
            office, created = Office.objects.get_or_create(
                name=office_info['name'],
                defaults=office_info
            )
            offices.append(office)
            if created:
                self.stdout.write(f'Created office: {office.name}')
            else:
                self.stdout.write(f'Office already exists: {office.name}')
        
        # Create Managers for each office
        managers = []
        manager_data = [
            {
                'username': 'mumbai_manager',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'email': 'rajesh.kumar@company.com',
                'phone': '+91-9876543210',
                'employee_id': 'MGR001',
                'department': 'Operations',
                'designation': 'Office Manager'
            },
            {
                'username': 'delhi_manager',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'email': 'priya.sharma@company.com',
                'phone': '+91-9876543211',
                'employee_id': 'MGR002',
                'department': 'Sales',
                'designation': 'Regional Manager'
            },
            {
                'username': 'bangalore_manager',
                'first_name': 'Arun',
                'last_name': 'Reddy',
                'email': 'arun.reddy@company.com',
                'phone': '+91-9876543212',
                'employee_id': 'MGR003',
                'department': 'Development',
                'designation': 'Tech Manager'
            }
        ]
        
        for i, manager_info in enumerate(manager_data):
            manager, created = CustomUser.objects.get_or_create(
                username=manager_info['username'],
                defaults={
                    **manager_info,
                    'role': 'manager',
                    'office': offices[i],
                    'password': make_password('manager123'),
                    'is_active': True,
                    'joining_date': date(2023, 1, 1),
                    'salary': 75000.00
                }
            )
            managers.append(manager)
            if created:
                self.stdout.write(f'Created manager: {manager.get_full_name()} for {manager.office.name}')
            else:
                self.stdout.write(f'Manager already exists: {manager.get_full_name()}')
        
        # Create Employees for each office
        employees = []
        employee_data = [
            # Mumbai Office Employees
            {
                'username': 'mumbai_emp1',
                'first_name': 'Amit',
                'last_name': 'Patel',
                'email': 'amit.patel@company.com',
                'phone': '+91-9876543220',
                'employee_id': 'EMP001',
                'department': 'IT',
                'designation': 'Software Developer',
                'office': offices[0]
            },
            {
                'username': 'mumbai_emp2',
                'first_name': 'Neha',
                'last_name': 'Singh',
                'email': 'neha.singh@company.com',
                'phone': '+91-9876543221',
                'employee_id': 'EMP002',
                'department': 'HR',
                'designation': 'HR Executive',
                'office': offices[0]
            },
            {
                'username': 'mumbai_emp3',
                'first_name': 'Vikram',
                'last_name': 'Joshi',
                'email': 'vikram.joshi@company.com',
                'phone': '+91-9876543222',
                'employee_id': 'EMP003',
                'department': 'Finance',
                'designation': 'Accountant',
                'office': offices[0]
            },
            # Delhi Office Employees
            {
                'username': 'delhi_emp1',
                'first_name': 'Sneha',
                'last_name': 'Gupta',
                'email': 'sneha.gupta@company.com',
                'phone': '+91-9876543230',
                'employee_id': 'EMP004',
                'department': 'Sales',
                'designation': 'Sales Executive',
                'office': offices[1]
            },
            {
                'username': 'delhi_emp2',
                'first_name': 'Rahul',
                'last_name': 'Verma',
                'email': 'rahul.verma@company.com',
                'phone': '+91-9876543231',
                'employee_id': 'EMP005',
                'department': 'Marketing',
                'designation': 'Marketing Specialist',
                'office': offices[1]
            },
            {
                'username': 'delhi_emp3',
                'first_name': 'Anjali',
                'last_name': 'Malhotra',
                'email': 'anjali.malhotra@company.com',
                'phone': '+91-9876543232',
                'employee_id': 'EMP006',
                'department': 'Customer Support',
                'designation': 'Support Executive',
                'office': offices[1]
            },
            # Bangalore Office Employees
            {
                'username': 'bangalore_emp1',
                'first_name': 'Karthik',
                'last_name': 'Iyer',
                'email': 'karthik.iyer@company.com',
                'phone': '+91-9876543240',
                'employee_id': 'EMP007',
                'department': 'Development',
                'designation': 'Senior Developer',
                'office': offices[2]
            },
            {
                'username': 'bangalore_emp2',
                'first_name': 'Divya',
                'last_name': 'Nair',
                'email': 'divya.nair@company.com',
                'phone': '+91-9876543241',
                'employee_id': 'EMP008',
                'department': 'QA',
                'designation': 'QA Engineer',
                'office': offices[2]
            },
            {
                'username': 'bangalore_emp3',
                'first_name': 'Suresh',
                'last_name': 'Menon',
                'email': 'suresh.menon@company.com',
                'phone': '+91-9876543242',
                'employee_id': 'EMP009',
                'department': 'DevOps',
                'designation': 'DevOps Engineer',
                'office': offices[2]
            }
        ]
        
        for emp_info in employee_data:
            employee, created = CustomUser.objects.get_or_create(
                username=emp_info['username'],
                defaults={
                    **emp_info,
                    'role': 'employee',
                    'password': make_password('employee123'),
                    'is_active': True,
                    'joining_date': date(2023, 6, 1),
                    'salary': 45000.00
                }
            )
            employees.append(employee)
            if created:
                self.stdout.write(f'Created employee: {employee.get_full_name()} for {employee.office.name}')
            else:
                self.stdout.write(f'Employee already exists: {employee.get_full_name()}')
        
        # Create Devices for each office (using the 3 ESSL devices from your image)
        devices = []
        device_data = [
            {
                'name': 'DOS Attendance',
                'device_type': 'essl',
                'ip_address': '192.168.200.64',
                'port': 4370,
                'serial_number': 'DOS001',
                'location': 'Main Entrance',
                'office': offices[0]  # Mumbai Office
            },
            {
                'name': 'Ace Track',
                'device_type': 'essl',
                'ip_address': '192.168.200.150',
                'port': 4370,
                'serial_number': 'ACE001',
                'location': 'Reception Area',
                'office': offices[1]  # Delhi Office
            },
            {
                'name': 'Bootcamp',
                'device_type': 'essl',
                'ip_address': '192.168.150.74',
                'port': 4370,
                'serial_number': 'BOOT001',
                'location': 'Development Floor',
                'office': offices[2]  # Bangalore Office
            }
        ]
        
        for device_info in device_data:
            device, created = Device.objects.get_or_create(
                name=device_info['name'],
                defaults=device_info
            )
            devices.append(device)
            if created:
                self.stdout.write(f'Created ESSL device: {device.name} for {device.office.name}')
            else:
                self.stdout.write(f'Device already exists: {device.name}')
        
        # Create some sample attendance records
        self.create_sample_attendance(employees, devices)
        
        # Create some sample leave requests
        self.create_sample_leaves(employees, managers)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created demo data:\n'
                f'- {len(offices)} Offices\n'
                f'- {len(managers)} Managers\n'
                f'- {len(employees)} Employees\n'
                f'- {len(devices)} ESSL Devices (Port 4370)\n'
                f'- Sample attendance and leave records'
            )
        )
        
        # Print login credentials
        self.stdout.write('\n=== LOGIN CREDENTIALS ===')
        self.stdout.write('Admin: admin / admin123')
        for manager in managers:
            self.stdout.write(f'Manager ({manager.office.name}): {manager.username} / manager123')
        for employee in employees[:3]:  # Show first 3 employees
            self.stdout.write(f'Employee ({employee.office.name}): {employee.username} / employee123')
    
    def create_sample_attendance(self, employees, devices):
        """Create sample attendance records for the last 7 days"""
        today = date.today()
        
        for employee in employees:
            device = next(d for d in devices if d.office == employee.office)
            
            for i in range(7):
                attendance_date = today - timedelta(days=i)
                
                # Skip weekends
                if attendance_date.weekday() >= 5:
                    continue
                
                # Create attendance record
                attendance, created = Attendance.objects.get_or_create(
                    user=employee,
                    date=attendance_date,
                    defaults={
                        'check_in_time': timezone.make_aware(
                            timezone.datetime.combine(attendance_date, timezone.datetime.min.time().replace(hour=9, minute=0))
                        ),
                        'check_out_time': timezone.make_aware(
                            timezone.datetime.combine(attendance_date, timezone.datetime.min.time().replace(hour=18, minute=0))
                        ),
                        'status': 'present',
                        'device': device
                    }
                )
                
                if created:
                    attendance.calculate_total_hours()
                    attendance.save()
    
    def create_sample_leaves(self, employees, managers):
        """Create sample leave requests"""
        leave_data = [
            {
                'leave_type': 'casual',
                'start_date': date.today() + timedelta(days=5),
                'end_date': date.today() + timedelta(days=5),
                'reason': 'Personal work',
                'status': 'pending'
            },
            {
                'leave_type': 'sick',
                'start_date': date.today() + timedelta(days=10),
                'end_date': date.today() + timedelta(days=12),
                'reason': 'Not feeling well',
                'status': 'pending'
            },
            {
                'leave_type': 'annual',
                'start_date': date.today() + timedelta(days=20),
                'end_date': date.today() + timedelta(days=25),
                'reason': 'Family vacation',
                'status': 'pending'
            }
        ]
        
        for i, leave_info in enumerate(leave_data):
            employee = employees[i % len(employees)]
            total_days = (leave_info['end_date'] - leave_info['start_date']).days + 1
            
            leave, created = Leave.objects.get_or_create(
                user=employee,
                start_date=leave_info['start_date'],
                end_date=leave_info['end_date'],
                defaults={
                    **leave_info,
                    'total_days': total_days
                }
            )
            
            if created:
                self.stdout.write(f'Created leave request for {employee.get_full_name()}')
