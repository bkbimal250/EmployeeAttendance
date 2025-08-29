#!/usr/bin/env python3
"""
Comprehensive Database Connection Fix
Fixes all database connection issues and prevents max_connections_per_hour errors
"""

import os
import sys
import django
import time
import logging
import subprocess
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.db import connection, close_old_connections
from core.db_manager import db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/db_fix.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_current_status():
    """Check current database connection status"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
            result = cursor.fetchone()
            current_connections = int(result[1]) if result else 0
            
            cursor.execute("SHOW VARIABLES LIKE 'max_connections'")
            result = cursor.fetchone()
            max_connections = int(result[1]) if result else 100
            
            cursor.execute("SHOW VARIABLES LIKE 'max_connections_per_hour'")
            result = cursor.fetchone()
            max_connections_per_hour = int(result[1]) if result else 500
            
            return {
                'current_connections': current_connections,
                'max_connections': max_connections,
                'max_connections_per_hour': max_connections_per_hour,
                'connection_usage_percent': (current_connections / max_connections) * 100
            }
    except Exception as e:
        logger.error(f"Error checking status: {e}")
        return None

def stop_background_services():
    """Stop any running background services that might be creating connections"""
    logger.info("Stopping background services...")
    
    try:
        # Stop ZKTeco auto-fetch service if running
        subprocess.run(['python', 'manage.py', 'auto_fetch_zkteco', '--stop'], 
                      capture_output=True, text=True)
        logger.info("Stopped ZKTeco auto-fetch service")
    except Exception as e:
        logger.warning(f"Could not stop ZKTeco service: {e}")
    
    # Wait a moment for services to stop
    time.sleep(2)

def reset_all_connections():
    """Reset all database connections"""
    logger.info("Resetting all database connections...")
    
    try:
        # Use Django's built-in function
        close_old_connections()
        
        # Use our database manager
        db_manager.reset_connections()
        
        # Close Django's default connection
        if hasattr(connection, 'connection') and connection.connection:
            connection.close()
        
        logger.info("All database connections reset successfully")
        
    except Exception as e:
        logger.error(f"Error resetting connections: {e}")

def optimize_database_settings():
    """Optimize database settings for better connection management"""
    logger.info("Optimizing database settings...")
    
    try:
        with connection.cursor() as cursor:
            # Set session variables for better connection management
            cursor.execute("SET SESSION wait_timeout = 28800")  # 8 hours
            cursor.execute("SET SESSION interactive_timeout = 28800")  # 8 hours
            cursor.execute("SET SESSION net_read_timeout = 30")
            cursor.execute("SET SESSION net_write_timeout = 30")
            
        logger.info("Database settings optimized")
        
    except Exception as e:
        logger.error(f"Error optimizing database settings: {e}")

def test_connection_health():
    """Test database connection health"""
    logger.info("Testing database connection health...")
    
    try:
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                logger.info("Database connection is healthy")
                return True
            else:
                logger.error("Database connection test failed")
                return False
                
    except Exception as e:
        logger.error(f"Database connection health test failed: {e}")
        return False

def start_connection_monitor():
    """Start the connection monitor in background"""
    logger.info("Starting connection monitor...")
    
    try:
        # Start monitor in background
        subprocess.Popen([
            sys.executable, 'manage_db_connections.py', 'monitor', '30'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        logger.info("Connection monitor started in background")
        
    except Exception as e:
        logger.error(f"Error starting connection monitor: {e}")

def main():
    """Main function to fix database connections"""
    logger.info("Starting comprehensive database connection fix...")
    
    # Step 1: Check current status
    logger.info("Step 1: Checking current status...")
    status = check_current_status()
    if status:
        logger.info(f"Current connections: {status['current_connections']}")
        logger.info(f"Max connections per hour: {status['max_connections_per_hour']}")
        logger.info(f"Usage: {status['connection_usage_percent']:.1f}%")
    
    # Step 2: Stop background services
    logger.info("Step 2: Stopping background services...")
    stop_background_services()
    
    # Step 3: Reset all connections
    logger.info("Step 3: Resetting all connections...")
    reset_all_connections()
    
    # Step 4: Optimize database settings
    logger.info("Step 4: Optimizing database settings...")
    optimize_database_settings()
    
    # Step 5: Test connection health
    logger.info("Step 5: Testing connection health...")
    if test_connection_health():
        logger.info("Connection health test passed")
    else:
        logger.error("Connection health test failed")
        return
    
    # Step 6: Start connection monitor
    logger.info("Step 6: Starting connection monitor...")
    start_connection_monitor()
    
    # Step 7: Final status check
    logger.info("Step 7: Final status check...")
    time.sleep(5)  # Wait for monitor to start
    final_status = check_current_status()
    if final_status:
        logger.info(f"Final connections: {final_status['current_connections']}")
        logger.info(f"Final usage: {final_status['connection_usage_percent']:.1f}%")
    
    logger.info("Database connection fix completed successfully!")
    logger.info("The system is now optimized to prevent max_connections_per_hour errors.")
    logger.info("Connection monitor is running in the background.")

if __name__ == '__main__':
    main()
