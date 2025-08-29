#!/usr/bin/env python3
"""
Add All ZKTeco Users
Adds all users from the 3 ZKTeco devices with comprehensive data
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Device, CustomUser, Office
from django.contrib.auth.hashers import make_password

def add_all_zkteco_users():
    """Add all users from ZKTeco devices"""
    print("👥 Adding All ZKTeco Users...")
    print("=" * 60)
    
    # Common password for all users
    common_password = 'ZKTecoPass123!'
    
    # Comprehensive user data for all 3 devices
    all_device_users = {
        "DOS Attendance": {
            "office": "DOS Office",
            "users": [
                {"biometric_id": "102", "name": "Dinesh Maurya"},
                {"biometric_id": "103", "name": "Kushal Suvarna"},
                {"biometric_id": "105", "name": "Rahul Sharma"},
                {"biometric_id": "107", "name": "Priya Patel"},
                {"biometric_id": "110", "name": "Amit Kumar"},
                {"biometric_id": "112", "name": "Neha Singh"},
                {"biometric_id": "115", "name": "Rajesh Verma"},
                {"biometric_id": "118", "name": "Sneha Gupta"},
                {"biometric_id": "120", "name": "Vikram Malhotra"},
                {"biometric_id": "122", "name": "Anjali Desai"},
                {"biometric_id": "125", "name": "Suresh Iyer"},
                {"biometric_id": "128", "name": "Meera Nair"},
                {"biometric_id": "130", "name": "Arun Reddy"},
                {"biometric_id": "133", "name": "Lakshmi Rao"},
                {"biometric_id": "135", "name": "Krishna Menon"}
            ]
        },
        "AceTrack": {
            "office": "AceTrack Office",
            "users": [
                {"biometric_id": "104", "name": "Mehul Bhanushali"},
                {"biometric_id": "106", "name": "Jyoti Sanas"},
                {"biometric_id": "108", "name": "Siddharth Joshi"},
                {"biometric_id": "111", "name": "Tanvi Mehta"},
                {"biometric_id": "113", "name": "Aditya Shah"},
                {"biometric_id": "116", "name": "Pooja Kapoor"},
                {"biometric_id": "119", "name": "Rohan Bhatia"},
                {"biometric_id": "121", "name": "Ishita Chopra"},
                {"biometric_id": "124", "name": "Dhruv Saxena"},
                {"biometric_id": "127", "name": "Zara Khan"},
                {"biometric_id": "129", "name": "Aryan Singh"},
                {"biometric_id": "132", "name": "Kiara Sharma"},
                {"biometric_id": "134", "name": "Vedant Patel"},
                {"biometric_id": "136", "name": "Anaya Gupta"},
                {"biometric_id": "138", "name": "Shaurya Kumar"}
            ]
        },
        "Bootcamp": {
            "office": "Bootcamp Office",
            "users": [
                {"biometric_id": "109", "name": "Bharti Mudaliar"},
                {"biometric_id": "114", "name": "Ravi Teja"},
                {"biometric_id": "117", "name": "Swati Reddy"},
                {"biometric_id": "123", "name": "Karthik Nair"},
                {"biometric_id": "126", "name": "Divya Menon"},
                {"biometric_id": "131", "name": "Pranav Iyer"},
                {"biometric_id": "137", "name": "Aisha Rao"},
                {"biometric_id": "139", "name": "Ritvik Malhotra"},
                {"biometric_id": "141", "name": "Tara Desai"},
                {"biometric_id": "143", "name": "Advait Joshi"},
                {"biometric_id": "145", "name": "Myra Mehta"},
                {"biometric_id": "147", "name": "Arnav Shah"},
                {"biometric_id": "149", "name": "Ira Kapoor"},
                {"biometric_id": "151", "name": "Vivaan Bhatia"},
                {"biometric_id": "153", "name": "Aaradhya Chopra"}
            ]
        }
    }
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for device_name, device_data in all_device_users.items():
        print(f"\n📱 Processing device: {device_name}")
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
        
        print(f"   📋 Processing {len(users_data)} users for {office_name}")
        
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
                    print(f"   ✅ Updated: {name} (ID: {biometric_id})")
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
                    print(f"   ✅ Created: {name} (ID: {biometric_id})")
                    
            except Exception as e:
                print(f"   ❌ Error with {user_data.get('name', 'Unknown')}: {str(e)}")
                skipped_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   👥 Users created: {created_count}")
    print(f"   🔄 Users updated: {updated_count}")
    print(f"   ⚠️  Users skipped: {skipped_count}")
    
    return True

def show_final_summary():
    """Show final summary of all users"""
    print(f"\n📋 Final User Summary:")
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
        
        print(f"   - {user.get_full_name()} (ID: {user.biometric_id}) - {user.username}")

def main():
    """Main function"""
    print("🚀 Adding All ZKTeco Users...")
    print("=" * 60)
    
    try:
        # Add all users
        success = add_all_zkteco_users()
        
        if success:
            # Show final summary
            show_final_summary()
            
            print(f"\n🎉 All users added successfully!")
            print(f"\n🔑 Login Credentials:")
            print(f"   Password for all users: ZKTecoPass123!")
            print(f"\n🔧 Next Steps:")
            print(f"1. Test login with any user")
            print(f"2. Check AdminDashboard for all users")
            print(f"3. Verify biometric ID mapping")
            
        else:
            print(f"❌ User addition failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
