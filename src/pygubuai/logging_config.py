"""Centralized logging configuration for PygubuAI."""
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Default log format with context
DEFAULT_FORMAT = '%(levelname)s: %(message)s'
DEBUG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def get_log_level() -> int:
    """Get log level from environment or default to INFO.

    Returns:
        Logging level constant (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    level_name = os.environ.get('PYGUBUAI_LOG_LEVEL', 'INFO').upper()
    return getattr(logging, level_name, logging.INFO)

def setup_logging(name: Optional[str] = None, level: Optional[int] = None) -> logging.Logger:
    """Configure logging with consistent format and level.

    Args:
        name: Logger name (defaults to 'pygubuai')
        level: Logging level (defaults to environment or INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or 'pygubuai')

    if logger.handlers:
        return logger

    log_level = level if level is not None else get_log_level()
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    fmt = DEBUG_FORMAT if log_level == logging.DEBUG else DEFAULT_FORMAT
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with standard configuration.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return setup_logging(name)
