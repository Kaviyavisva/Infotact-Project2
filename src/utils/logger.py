import logging
import sys
from src.utils.config import settings

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger with the specified name.
    
    Args:
        name (str): The name of the logger (typically __name__).
        
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Only configure the logger if it hasn't been configured yet
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        
        # Create console handler with standard stdout formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        
        # Create formatter and add it to the handler
        formatter = logging.Formatter(settings.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        
        # Add handler to the logger
        logger.addHandler(console_handler)
        
        # Prevent propagation to the root logger to avoid duplicate logs
        logger.propagate = False
        
    return logger
