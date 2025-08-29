#!/usr/bin/env python3
"""
Database Connection Middleware
Automatically manages database connections for all requests
"""

import logging
import time
from django.db import close_old_connections
from core.db_manager import db_manager

logger = logging.getLogger(__name__)

class DatabaseConnectionMiddleware:
    """Middleware to manage database connections"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Close old connections before processing request
        close_old_connections()
        
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Close connections after processing
        close_old_connections()
        
        # Log slow requests
        duration = time.time() - start_time
        if duration > 5:  # Log requests taking more than 5 seconds
            logger.warning(f"Slow request: {request.path} took {duration:.2f}s")
        
        return response
    
    def process_exception(self, request, exception):
        """Handle exceptions and ensure connections are closed"""
        logger.error(f"Exception in request {request.path}: {str(exception)}")
        close_old_connections()
        return None
