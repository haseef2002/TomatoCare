"""
TomatoCare Expert System - Centralized Logging Module
---------------------------------------------------
Handles system event tracking, error auditing, and debugging.
Configured for production deployment with Rotating File Handlers 
to prevent memory overflow during continuous edge-device operation.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Define the directory where logs will be stored
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, 'system_runtime.log')

def get_logger(module_name):
    """
    Initializes and returns a configured logger for a specific module.
    
    Usage:
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("System booted successfully.")
        logger.error("Failed to load weights.")
    """
    
    # Create a custom logger
    logger = logging.getLogger(module_name)
    
    # Prevent duplicate logs if the logger is requested multiple times
    if logger.hasHandlers():
        return logger

    # Set the base logging level (DEBUG catches everything, INFO catches normal ops)
    logger.setLevel(logging.INFO)

    # Define the professional log format
    # Example: 2026-04-03 10:15:30 - ERROR - [engine.py:45] - Model weights missing!
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. File Handler (Archives logs up to 5MB, keeps the last 3 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, 
        maxBytes=5 * 1024 * 1024, # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 2. Console Handler (Prints to your Streamlit terminal for active debugging)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING) # Only print Warnings and Errors to console

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger