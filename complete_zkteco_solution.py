#!/usr/bin/env python3
"""
Complete ZKTeco Solution
Fetches all historical data and sets up 24/7 automatic fetching
"""

import os
import sys
import django
import logging
import time
import threading
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Device, CustomUser, Attendance, Office
from django.utils import timezone
from django.db import transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/complete_zkteco_solution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from zk import ZK
except ImportError:
    logger.error("pyzk library not found. Please install it with: pip install pyzk")
    ZK = None

class CompleteZKTecoSolution:
    """Complete ZKTeco solution for historical data and 24/7 automatic fetching"""
    
    def __init__(self):
        self.devices = []
        self.running = False
        self.thread = None
        self.interval = 30  # 30 seconds
        
    def get_all_devices(self):
        """Get all active ZKTeco devices"""
        self.devices = Device.objects.filter(
            device_type='zkteco',
            is_active=True
        )
        logger.info(f"Found {self.devices.count()} active ZKTeco devices")
        return self.devices
    
    def connect_to_device(self, device):
        """Connect to a ZKTeco device"""
        try:
            if not ZK:
                logger.error("pyzk library not available")
                return None
                
            zk = ZK(device.ip_address, port=device.port, timeout=30)
            conn = zk.connect()
            
            if conn:
                logger.info(f"Connected to {device.name} ({device.ip_address}:{device.port})")
                return conn
            else:
                logger.error(f"Failed to connect to {device.name}")
                return None
                
        except Exception as e:
            logger.error(f"Connection error to {device.name}: {str(e)}")
            return None
    
    def get_device_attendance(self, conn, device):
        """Get attendance records from device"""
        try:
            attendance_logs = conn.get_attendance()
            logger.info(f"Found {len(attendance_logs)} attendance records on {device.name}")
            return attendance_logs
        except Exception as e:
            logger.error(f"Error getting attendance from {device.name}: {str(e)}")
            return []
    
    def make_timezone_aware(self, timestamp):
        """Make timestamp timezone-aware"""
        if timezone.is_naive(timestamp):
            return timezone.make_aware(timestamp, timezone.get_current_timezone())
        return timestamp
    
    def process_attendance_records(self, logs, device):
        """Process attendance records with proper check-in/check-out logic"""
        if not logs:
            return 0, 0
            
        synced_count = 0
        error_count = 0
        
        # Group logs by user and date
        user_date_logs = {}
        
        for log in logs:
            user_id = log.user_id
            timestamp = self.make_timezone_aware(log.timestamp)
            date = timestamp.date()
            key = (user_id, date)
            
            if key not in user_date_logs:
                user_date_logs[key] = []
            user_date_logs[key].append(log)
        
        # Process each user's logs for each date
        for (user_id, date), user_logs in user_date_logs.items():
            try:
                # Find user in database
                try:
                    user = CustomUser.objects.get(employee_id=str(user_id))
                except CustomUser.DoesNotExist:
                    logger.warning(f"User with employee_id {user_id} not found")
                    error_count += 1
                    continue
                
                # Sort logs by timestamp
                user_logs.sort(key=lambda x: x.timestamp)
                
                # Get or create attendance record
                attendance, created = Attendance.objects.get_or_create(
                    user=user,
                    date=date,
                    defaults={
                        'status': 'Present',
                        'device': device
                    }
                )
                
                # Process check-in and check-out times
                check_in_time = None
                check_out_time = None
                
                for log in user_logs:
                    timestamp = log.timestamp
                    
                    # Determine if this is check-in or check-out
                    if len(user_logs) == 1:
                        # Single log - determine by time
                        if timestamp.hour < 12:
                            check_in_time = timestamp
                        else:
                            check_out_time = timestamp
                    else:
                        # Multiple logs - first is check-in, last is check-out
                        if log == user_logs[0]:  # First log
                            check_in_time = timestamp
                        elif log == user_logs[-1]:  # Last log
                            check_out_time = timestamp
                
                # Update attendance record
                updated = False
                
                if check_in_time and not attendance.check_in_time:
                    attendance.check_in_time = check_in_time
                    updated = True
                    logger.info(f"Check-in: {user.get_full_name()} at {check_in_time.strftime('%H:%M')}")
                
                if check_out_time and not attendance.check_out_time:
                    attendance.check_out_time = check_out_time
                    updated = True
                    logger.info(f"Check-out: {user.get_full_name()} at {check_out_time.strftime('%H:%M')}")
                
                if updated:
                    attendance.device = device
                    attendance.save()
                    synced_count += 1
                
            except Exception as e:
                logger.error(f"Error processing attendance for user {user_id}: {str(e)}")
                error_count += 1
        
        return synced_count, error_count
    
    def fetch_historical_data(self):
        """Fetch all historical data from all devices"""
        logger.info("Starting historical ZKTeco data fetch...")
        
        devices = self.get_all_devices()
        if not devices:
            logger.error("No ZKTeco devices found")
            return 0, 0
        
        total_synced = 0
        total_errors = 0
        
        for device in devices:
            logger.info(f"Fetching historical data from {device.name}")
            
            # Connect to device
            conn = self.connect_to_device(device)
            if not conn:
                continue
            
            try:
                # Get attendance records
                attendance_logs = self.get_device_attendance(conn, device)
                
                if attendance_logs:
                    # Process attendance records
                    synced_count, error_count = self.process_attendance_records(attendance_logs, device)
                    total_synced += synced_count
                    total_errors += error_count
                    
                    logger.info(f"{device.name}: {synced_count} synced, {error_count} errors")
                else:
                    logger.warning(f"No data found on {device.name}")
                    
            except Exception as e:
                logger.error(f"Error fetching from {device.name}: {str(e)}")
            
            finally:
                # Disconnect
                try:
                    conn.disconnect()
                    logger.info(f"Disconnected from {device.name}")
                except:
                    pass
            
            # Small delay between devices
            time.sleep(2)
        
        logger.info(f"Historical fetch complete: {total_synced} synced, {total_errors} errors")
        return total_synced, total_errors
    
    def start_automatic_fetching(self):
        """Start 24/7 automatic fetching"""
        if self.running:
            logger.warning("Automatic fetching is already running")
            return
        
        logger.info("Starting 24/7 automatic ZKTeco data fetching...")
        self.running = True
        
        # Start the background thread
        self.thread = threading.Thread(target=self._run_automatic_fetching, daemon=True)
        self.thread.start()
        
        logger.info(f"Automatic fetching started. Fetching every {self.interval} seconds")
    
    def stop_automatic_fetching(self):
        """Stop automatic fetching"""
        logger.info("Stopping automatic ZKTeco data fetching...")
        self.running = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        logger.info("Automatic fetching stopped")
    
    def _run_automatic_fetching(self):
        """Main loop for automatic fetching"""
        logger.info("Automatic fetching loop started")
        
        while self.running:
            try:
                # Fetch from all devices
                devices = self.get_all_devices()
                
                for device in devices:
                    if not self.running:
                        break
                    
                    try:
                        logger.info(f"Auto-fetching from {device.name}")
                        
                        # Connect to device
                        conn = self.connect_to_device(device)
                        if not conn:
                            continue
                        
                        try:
                            # Get attendance records
                            attendance_logs = self.get_device_attendance(conn, device)
                            
                            if attendance_logs:
                                # Process attendance records
                                synced_count, error_count = self.process_attendance_records(attendance_logs, device)
                                
                                if synced_count > 0:
                                    logger.info(f"Auto-synced {synced_count} records from {device.name}")
                                
                                # Update device last sync time
                                device.last_sync = timezone.now()
                                device.save(update_fields=['last_sync'])
                            
                        finally:
                            # Disconnect
                            try:
                                conn.disconnect()
                            except:
                                pass
                        
                    except Exception as e:
                        logger.error(f"Error auto-fetching from {device.name}: {str(e)}")
                
                # Wait for next interval
                time.sleep(self.interval)
                
            except Exception as e:
                logger.error(f"Error in automatic fetching loop: {str(e)}")
                time.sleep(self.interval)
    
    def get_status(self):
        """Get current status"""
        today = timezone.now().date()
        today_count = Attendance.objects.filter(date=today).count()
        total_count = Attendance.objects.count()
        
        return {
            'running': self.running,
            'devices_count': self.devices.count(),
            'today_attendance': today_count,
            'total_attendance': total_count,
            'interval': self.interval
        }

def main():
    """Main function"""
    print("="*60)
    print("Complete ZKTeco Solution")
    print("="*60)
    
    solution = CompleteZKTecoSolution()
    
    # Step 1: Fetch historical data
    print("\nStep 1: Fetching historical data...")
    try:
        synced, errors = solution.fetch_historical_data()
        print(f"Historical data fetch complete: {synced} synced, {errors} errors")
    except Exception as e:
        print(f"Error fetching historical data: {str(e)}")
    
    # Step 2: Start automatic fetching
    print("\nStep 2: Starting 24/7 automatic fetching...")
    try:
        solution.start_automatic_fetching()
        print("Automatic fetching started successfully!")
        
        # Show status
        status = solution.get_status()
        print(f"\nStatus:")
        print(f"- Automatic fetching: {'Running' if status['running'] else 'Stopped'}")
        print(f"- Devices: {status['devices_count']}")
        print(f"- Today's attendance: {status['today_attendance']}")
        print(f"- Total attendance: {status['total_attendance']}")
        print(f"- Fetch interval: {status['interval']} seconds")
        
        print("\nThe system is now running 24/7!")
        print("Press Ctrl+C to stop...")
        
        # Keep running
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nStopping automatic fetching...")
            solution.stop_automatic_fetching()
            print("System stopped.")
            
    except Exception as e:
        print(f"Error starting automatic fetching: {str(e)}")

if __name__ == '__main__':
    main()
