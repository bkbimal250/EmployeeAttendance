#!/usr/bin/env python3
"""
Database Connection Management Script
Monitors and manages database connections to prevent max_connections_per_hour errors
"""

import os
import sys
import django
import time
import logging
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
        logging.FileHandler('logs/db_connection_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_connection_status():
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
        logger.error(f"Error checking connection status: {e}")
        return None

def optimize_connections():
    """Optimize database connections"""
    try:
        logger.info("Starting connection optimization...")
        
        # Close old connections
        close_old_connections()
        
        # Use our database manager
        db_manager.optimize_connections()
        
        # Check status after optimization
        status = check_connection_status()
        if status:
            logger.info(f"Connection optimization completed. Current connections: {status['current_connections']}")
        
    except Exception as e:
        logger.error(f"Error optimizing connections: {e}")

def monitor_connections(interval=60):
    """Monitor database connections continuously"""
    logger.info(f"Starting database connection monitoring (interval: {interval}s)")
    
    while True:
        try:
            status = check_connection_status()
            if status:
                logger.info(f"DB Status - Current: {status['current_connections']}, "
                          f"Max: {status['max_connections']}, "
                          f"Usage: {status['connection_usage_percent']:.1f}%")
                
                # If usage is high, optimize connections
                if status['connection_usage_percent'] > 70:
                    logger.warning("High connection usage detected. Optimizing...")
                    optimize_connections()
            
            time.sleep(interval)
            
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
            time.sleep(interval)

def reset_connections():
    """Reset all database connections"""
    try:
        logger.info("Resetting all database connections...")
        db_manager.reset_connections()
        logger.info("Database connections reset successfully")
    except Exception as e:
        logger.error(f"Error resetting connections: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_db_connections.py check     - Check connection status")
        print("  python manage_db_connections.py optimize  - Optimize connections")
        print("  python manage_db_connections.py reset     - Reset all connections")
        print("  python manage_db_connections.py monitor   - Monitor connections continuously")
        return
    
    command = sys.argv[1]
    
    if command == 'check':
        status = check_connection_status()
        if status:
            print(f"Current connections: {status['current_connections']}")
            print(f"Max connections: {status['max_connections']}")
            print(f"Max connections per hour: {status['max_connections_per_hour']}")
            print(f"Usage: {status['connection_usage_percent']:.1f}%")
        else:
            print("Failed to check connection status")
    
    elif command == 'optimize':
        optimize_connections()
    
    elif command == 'reset':
        reset_connections()
    
    elif command == 'monitor':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        monitor_connections(interval)
    
    else:
        print(f"Unknown command: {command}")

if __name__ == '__main__':
    main()
