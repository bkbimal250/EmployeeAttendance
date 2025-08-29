#!/usr/bin/env python3
"""
Create ZKTeco Users from Devices
Creates users for all employees that exist on the 3 ZKTeco devices
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Device, CustomUser, Office
from django.contrib.auth.hashers import make_password

def create_zkteco_users():
    """Create users for all ZKTeco device employees"""
    print("👥 Creating ZKTeco Users from Devices...")
    print("=" * 60)
    
    # Common password for all users
    common_password = 'ZKTecoPass123!'
    
    # Device-specific user data (based on your test output)
    device_users = {
        "DOS Attendance": {
            "office": "DOS Office",
            "users": [
                {"biometric_id": "102", "name": "Dinesh Maurya"},
                {"biometric_id": "103", "name": "Kushal Suvarna"},
                # Add more users from DOS device
            ]
        },
        "AceTrack": {
            "office": "AceTrack Office", 
            "users": [
                {"biometric_id": "104", "name": "Mehul Bhanushali"},
                {"biometric_id": "106", "name": "Jyoti Sanas"},
                # Add more users from AceTrack device
            ]
        },
        "Bootcamp": {
            "office": "Bootcamp Office",
            "users": [
                {"biometric_id": "109", "name": "Bharti Mudaliar"},
                # Add more users from Bootcamp device
            ]
        }
    }
    
    # Get all ZKTeco devices from database
    zkteco_devices = Device.objects.filter(device_type='zkteco', is_active=True)
    print(f"✅ Found {zkteco_devices.count()} ZKTeco devices in database")
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for device in zkteco_devices:
        print(f"\n📱 Processing device: {device.name}")
        print(f"   IP: {device.ip_address}:{device.port}")
        print(f"   Office: {device.office.name}")
        
        # Get device users data
        if device.name in device_users:
            device_data = device_users[device.name]
            office_name = device_data["office"]
            users_data = device_data["users"]
            
            # Get or create office
            office, created = Office.objects.get_or_create(
                name=office_name,
                defaults={
                    'address': f'{office_name} Building',
                    'phone': '+91-1234567890',
                    'email': f'{office_name.lower().replace(" ", "")}@company.com'
                }
            )
            
            print(f"   📋 Creating {len(users_data)} users for {office_name}")
            
            for user_data in users_data:
                try:
                    biometric_id = user_data['biometric_id']
                    name = user_data['name']
                    
                    # Parse name
                    name_parts = name.strip().split(' ', 1)
                    first_name = name_parts[0] if name_parts else name
                    last_name = name_parts[1] if len(name_parts) > 1 else ""
                    
                    # Check if user already exists
                    existing_user = CustomUser.objects.filter(
                        biometric_id=biometric_id
                    ).first()
                    
                    if existing_user:
                        # Update existing user
                        existing_user.first_name = first_name
                        existing_user.last_name = last_name
                        existing_user.office = office
                        existing_user.save()
                        updated_count += 1
                        print(f"   ✅ Updated user: {name} (ID: {biometric_id}) - {office_name}")
                    else:
                        # Create new user
                        username = f"zkteco_{biometric_id}"
                        email = f"zkteco_{biometric_id}@company.com"
                        
                        user = CustomUser.objects.create(
                            username=username,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            biometric_id=biometric_id,
                            employee_id=f"EMP{biometric_id}",
                            office=office,
                            department="Operations",
                            designation="Employee",
                            role='employee',
                            password=make_password(common_password),
                            is_active=True
                        )
                        created_count += 1
                        print(f"   ✅ Created user: {name} (ID: {biometric_id}) - {office_name}")
                        
                except Exception as e:
                    print(f"   ❌ Error creating user {user_data.get('name', 'Unknown')}: {str(e)}")
                    skipped_count += 1
        else:
            print(f"   ⚠️  No user data found for device: {device.name}")
    
    print(f"\n📊 Summary:")
    print(f"   👥 Users created: {created_count}")
    print(f"   🔄 Users updated: {updated_count}")
    print(f"   ⚠️  Users skipped: {skipped_count}")
    
    return True

def show_all_users():
    """Show all users with biometric IDs"""
    print(f"\n📋 All Users with Biometric IDs:")
    print("=" * 60)
    
    users_with_biometric = CustomUser.objects.filter(
        biometric_id__isnull=False
    ).exclude(biometric_id='').order_by('office__name', 'first_name')
    
    print(f"👥 Total Users: {users_with_biometric.count()}")
    
    # Group by office
    current_office = None
    for user in users_with_biometric:
        office_name = user.office.name if user.office else "No Office"
        
        if office_name != current_office:
            print(f"\n🏢 {office_name}:")
            current_office = office_name
        
        print(f"   - {user.get_full_name()} (ID: {user.biometric_id}) - Username: {user.username}")

def main():
    """Main function"""
    print("🚀 Creating ZKTeco Users from Devices...")
    print("=" * 60)
    
    try:
        # Create users for all devices
        success = create_zkteco_users()
        
        if success:
            # Show all users
            show_all_users()
            
            print(f"\n🎉 User creation completed successfully!")
            print(f"\n🔑 Login Credentials:")
            print(f"   Password for all users: ZKTecoPass123!")
            print(f"\n🔧 Next Steps:")
            print(f"1. Test login with created users")
            print(f"2. Verify biometric ID mapping")
            print(f"3. Check AdminDashboard for users")
            
        else:
            print(f"❌ User creation failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
