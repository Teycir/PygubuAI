"""Utility functions"""
import re
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def get_file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of file contents.
    
    Args:
        filepath: Path to file to hash
        
    Returns:
        32-character hexadecimal MD5 hash
        
    Raises:
        OSError: If file cannot be read
    """
    try:
        return hashlib.md5(filepath.read_bytes()).hexdigest()
    except OSError as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        raise

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

def validate_path(path: str, must_exist: bool = False, must_be_dir: bool = False) -> Path:
    """Validate and sanitize file paths to prevent security issues.
    
    Args:
        path: Path string to validate
        must_exist: Require path to exist
        must_be_dir: Require path to be a directory
        
    Returns:
        Validated Path object
        
    Raises:
        ValueError: If path is invalid, unsafe, or doesn't meet requirements
    """
    try:
        p = Path(path).resolve()
    except (ValueError, RuntimeError, OSError) as e:
        raise ValueError(f"Invalid path '{path}': {e}")
    
    # Prevent directory traversal attacks
    if ".." in Path(path).parts:
        raise ValueError(f"Path traversal not allowed: {path}")
    
    if must_exist and not p.exists():
        raise ValueError(f"Path does not exist: {p}")
    
    if must_be_dir and p.exists() and not p.is_dir():
        raise ValueError(f"Path is not a directory: {p}")
    
    return p
