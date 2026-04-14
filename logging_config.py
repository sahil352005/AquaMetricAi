"""
Logging configuration for AquaMetric AI.

This module sets up comprehensive logging for the entire application.
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging():
    """Set up logging for the entire application."""
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('aquametric')
    logger.setLevel(logging.DEBUG)
    
    # Log file path
    log_file = os.path.join(log_dir, f'aquametric_{datetime.now().strftime("%Y%m%d")}.log')
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Initialize logger
app_logger = setup_logging()


def get_logger(name):
    """Get logger instance for a module."""
    logger = logging.getLogger(f'aquametric.{name}')
    return logger
