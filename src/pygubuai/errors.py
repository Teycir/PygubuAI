"""Error handling for PygubuAI"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PygubuAIError(Exception):
    """Base exception for all PygubuAI errors"""
    def __init__(self, message: str, suggestion: str = "", cause: Optional[Exception] = None):
        self.message = message
        self.suggestion = suggestion
        self.cause = cause
        super().__init__(self.message)

    def __str__(self):
        error = f"[ERROR] {self.message}"
        if self.suggestion:
            error += f"\n[SUGGESTION] {self.suggestion}"
        if self.cause:
            error += f"\n[CAUSE] {type(self.cause).__name__}: {self.cause}"
        return error

class ProjectNotFoundError(PygubuAIError):
    """Project not found in registry"""
    def __init__(self, project_name: str, suggestion: str = ""):
        if not suggestion:
            suggestion = "Use 'pygubu-register list' to see available projects"
        super().__init__(f"Project '{project_name}' not found", suggestion)

class InvalidProjectError(PygubuAIError):
    """Invalid project structure or configuration"""
    def __init__(self, path: str, reason: str, suggestion: str = ""):
        if not suggestion:
            suggestion = "Check that .ui and .py files exist and are valid"
        super().__init__(f"Invalid project at '{path}': {reason}", suggestion)

class DependencyError(PygubuAIError):
    """Missing or incompatible dependency"""
    def __init__(self, dependency: str, suggestion: str = ""):
        if not suggestion:
            suggestion = f"Install with: pip install {dependency}"
        super().__init__(f"Missing dependency: {dependency}", suggestion)

class FileOperationError(PygubuAIError):
    """File operation failed"""
    def __init__(self, operation: str, path: str, cause: Exception):
        suggestion = "Check file permissions and disk space"
        super().__init__(f"Failed to {operation} '{path}'", suggestion, cause)

class ValidationError(PygubuAIError):
    """Input validation failed"""
    def __init__(self, field: str, value: str, reason: str, suggestion: str = ""):
        if not suggestion:
            suggestion = f"Provide a valid {field}"
        super().__init__(f"Invalid {field}: '{value}' - {reason}", suggestion)

class RegistryError(PygubuAIError):
    """Registry operation failed"""
    def __init__(self, operation: str, reason: str, cause: Optional[Exception] = None):
        suggestion = "Try 'pygubu-register list' to check registry status"
        super().__init__(f"Registry {operation} failed: {reason}", suggestion, cause)

class UIParseError(PygubuAIError):
    """UI file parsing failed"""
    def __init__(self, file_path: str, reason: str, cause: Optional[Exception] = None):
        suggestion = "Check XML syntax with pygubu-designer"
        super().__init__(f"Failed to parse UI file '{file_path}': {reason}", suggestion, cause)

class GitError(PygubuAIError):
    """Git operation failed"""
    def __init__(self, operation: str, reason: str):
        suggestion = "Ensure git is installed and repository is valid"
        super().__init__(f"Git {operation} failed: {reason}", suggestion)

def validate_pygubu():
    """Check pygubu is installed and compatible"""
    try:
        import pygubu
        version = getattr(pygubu, '__version__', 'unknown')
        logger.debug(f"Found pygubu version: {version}")
    except ImportError as e:
        raise DependencyError("pygubu", "pip install pygubu>=0.39") from e

def validate_pygubu_designer():
    """Check pygubu-designer is available"""
    import shutil
    if not shutil.which("pygubu-designer"):
        raise DependencyError(
            "pygubu-designer",
            "pip install pygubu-designer>=0.42"
        )

def handle_file_operation(operation: str, path: str, func, *args, **kwargs):
    """Safely execute file operation with proper error handling"""
    try:
        return func(*args, **kwargs)
    except PermissionError as e:
        raise FileOperationError(operation, path, e) from e
    except OSError as e:
        raise FileOperationError(operation, path, e) from e
    except Exception as e:
        logger.error(f"Unexpected error during {operation} on {path}: {e}")
        raise FileOperationError(operation, path, e) from e
