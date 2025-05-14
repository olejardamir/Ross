import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from Ross_git.src.app.config.app_config import get_section


def setup_logger():
    # Load logging configuration from the .config file
    logging_config = get_section("logging")

    # Get values from the configuration or use defaults
    log_level_str = logging_config.get("log_level", "INFO").upper()
    log_dir = logging_config.get("log_dir", "Ross_git/logs")
    log_max_size = int(logging_config.get("log_max_size", 10000))  # Max logs per file (in KB)
    log_backup_count = int(logging_config.get("log_backup_count", 5))  # Max backup files
    log_file_prefix = logging_config.get("log_file_prefix", "speech_generator")
    log_format = logging_config.get("log_format", "%(asctime)s - %(levelname)s - %(message)s")

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Generate log file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{log_file_prefix}_{timestamp}.log")

    # Map string to logging level
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Create a rotating file handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=log_max_size * 1024, backupCount=log_backup_count
    )

    # Set logging format for file handler (includes timestamp)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Set up the logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(file_handler)

    # Also log to the console with a timestamp
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)  # Add timestamp to console log as well
    logger.addHandler(console_handler)

    return logger


from log_manager import setup_logger

# Initialize the logger
logger = setup_logger()

# Example of logging at different levels

# Information level log
logger.info("This is an info message indicating normal operation.")

# Debug level log (useful for development or debugging)
logger.debug("This is a debug message for troubleshooting purposes.")

# Warning level log (indicates a potential issue)
logger.warning("This is a warning message indicating a potential issue.")

# Error level log (indicates an error occurred)
logger.error("This is an error message indicating an issue that needs attention.")

# Critical level log (indicates a severe issue that requires immediate action)
logger.critical("This is a critical message indicating a severe problem.")
