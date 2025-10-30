"""Utility functions"""
import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def validate_project_name(name: str) -> str:
    """Validate and sanitize project name"""
    if not name:
        raise ValueError("Project name cannot be empty")
    
    sanitized = re.sub(r'[^\w\-]', '_', name)
    if sanitized != name:
        logger.warning(f"Project name sanitized: '{name}' -> '{sanitized}'")
    
    return sanitized

def ensure_directory(path: Path) -> Path:
    """Ensure directory exists"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except OSError as e:
        raise OSError(f"Cannot create directory {path}: {e}")

def find_pygubu_designer() -> str:
    """Find pygubu-designer executable"""
    import shutil
    designer = shutil.which("pygubu-designer")
    return designer if designer else "pygubu-designer"
