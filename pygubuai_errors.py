#!/usr/bin/env python3
"""Enhanced error handling for PygubuAI"""

class PygubuAIError(Exception):
    """Base exception for PygubuAI"""
    def __init__(self, message: str, suggestion: str = ""):
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)
    
    def __str__(self):
        error = f"❌ Error: {self.message}"
        if self.suggestion:
            error += f"\n💡 Suggestion: {self.suggestion}"
        return error

class ProjectNotFoundError(PygubuAIError):
    """Project not found"""
    def __init__(self, project_name: str):
        super().__init__(
            f"Project '{project_name}' not found",
            "Use 'pygubu-register list' to see available projects or 'pygubu-register scan' to discover projects"
        )

class InvalidProjectError(PygubuAIError):
    """Invalid project structure"""
    def __init__(self, path: str, reason: str):
        super().__init__(
            f"Invalid project at {path}: {reason}",
            "Ensure the directory contains .ui files for a valid Pygubu project"
        )

class DependencyError(PygubuAIError):
    """Missing dependency"""
    def __init__(self, dependency: str):
        super().__init__(
            f"Missing required dependency: {dependency}",
            f"Install with: pip install {dependency}"
        )

def validate_pygubu_installed():
    """Check if pygubu is installed"""
    try:
        import pygubu
    except ImportError:
        raise DependencyError("pygubu")

def validate_project_structure(path):
    """Validate project has required files"""
    from pathlib import Path
    project_path = Path(path)
    
    if not project_path.exists():
        raise InvalidProjectError(str(path), "Directory does not exist")
    
    ui_files = list(project_path.glob("*.ui"))
    if not ui_files:
        raise InvalidProjectError(str(path), "No .ui files found")
    
    return True
