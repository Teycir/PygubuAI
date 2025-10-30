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
    pass

class InvalidProjectError(PygubuAIError):
    """Invalid project structure"""
    pass

class DependencyError(PygubuAIError):
    """Missing dependency"""
    pass

def validate_pygubu():
    """Check pygubu is installed"""
    try:
        import pygubu
    except ImportError:
        raise DependencyError("pygubu not installed", "pip install pygubu")
