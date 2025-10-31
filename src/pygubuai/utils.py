"""Utility functions"""

import re
import hashlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_file_hash(filepath: Path) -> str:
    """Calculate SHA-256 hash of file contents.

    Args:
        filepath: Path to file to hash

    Returns:
        64-character hexadecimal SHA-256 hash

    Raises:
        OSError: If file cannot be read
    """
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()
    except OSError as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        raise


def validate_project_name(name: str) -> str:
    """Validate and sanitize project name"""
    if not name:
        raise ValueError("Project name cannot be empty")

    sanitized = re.sub(r"[^\w\-]", "_", name)
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
    # Prevent directory traversal attacks BEFORE resolving
    if ".." in Path(path).parts:
        raise ValueError(f"Path traversal not allowed: {path}")

    try:
        p = Path(path).resolve()
    except (ValueError, RuntimeError, OSError) as e:
        raise ValueError(f"Invalid path '{path}': {e}")

    if must_exist:
        if not p.exists():
            raise ValueError(f"Path does not exist: {p}")

    if must_be_dir:
        if p.exists() and not p.is_dir():
            raise ValueError(f"Path is not a directory: {p}")
        elif must_exist and not p.is_dir():
            raise ValueError(f"Path is not a directory: {p}")

    return p


def validate_safe_path(path: str, base_dir: str = None) -> Path:
    """Validate path is safe and within allowed directory.

    Args:
        path: Path to validate
        base_dir: Optional base directory to restrict path within

    Returns:
        Validated and resolved Path object

    Raises:
        ValueError: If path is unsafe or outside base_dir
    """
    if not path:
        raise ValueError("Path cannot be empty")

    try:
        p = Path(path).resolve()

        # Check for path traversal in original path
        if ".." in Path(path).parts:
            raise ValueError(f"Path traversal detected: {path}")

        # If base_dir specified, ensure path is within it
        if base_dir:
            base = Path(base_dir).resolve()
            try:
                p.relative_to(base)
            except ValueError:
                raise ValueError(f"Path outside allowed directory: {path}")

        return p
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")


def safe_xml_text(text: str) -> str:
    """Escape text for safe XML inclusion.

    Args:
        text: Text to escape

    Returns:
        XML-safe escaped text
    """
    if text is None:
        return ""
    from xml.sax.saxutils import escape

    return escape(str(text), {"'": "&apos;", '"': "&quot;"})
