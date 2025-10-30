"""Error handling for PygubuAI"""

class PygubuAIError(Exception):
    """Base exception"""
    def __init__(self, message: str, suggestion: str = ""):
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)
    
    def __str__(self):
        error = f"[ERROR] {self.message}"
        if self.suggestion:
            error += f"\n[SUGGESTION] {self.suggestion}"
        return error

class ProjectNotFoundError(PygubuAIError):
    """Project not found"""
    def __init__(self, project_name: str, suggestion: str = ""):
        super().__init__(f"Project '{project_name}' not found", suggestion)

class InvalidProjectError(PygubuAIError):
    """Invalid project structure"""
    def __init__(self, path: str, reason: str):
        super().__init__(f"Invalid project at '{path}': {reason}")

class DependencyError(PygubuAIError):
    """Missing dependency"""
    pass

def validate_pygubu():
    """Check pygubu is installed"""
    try:
        import pygubu
    except ImportError:
        raise DependencyError("pygubu not installed", "pip install pygubu")
