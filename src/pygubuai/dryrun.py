"""Dry-run mode for previewing operations without executing."""
from pathlib import Path
from typing import List, Dict, Any


class DryRunOperation:
    """Represents a dry-run operation."""
    
    def __init__(self, action: str, target: str, details: Dict[str, Any]):
        self.action = action
        self.target = target
        self.details = details
    
    def __str__(self) -> str:
        lines = [f"[{self.action}] {self.target}"]
        for key, value in self.details.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)


class DryRunContext:
    """Context manager for dry-run operations."""
    
    def __init__(self):
        self.operations: List[DryRunOperation] = []
        self.enabled = False
    
    def __enter__(self):
        self.enabled = True
        return self
    
    def __exit__(self, *args):
        self.enabled = False
    
    def record(self, action: str, target: str, **details):
        """Record an operation."""
        if self.enabled:
            self.operations.append(DryRunOperation(action, target, details))
    
    def preview(self) -> str:
        """Get preview of all operations."""
        if not self.operations:
            return "No operations to perform."
        
        lines = ["Dry-run preview:", ""]
        for op in self.operations:
            lines.append(str(op))
            lines.append("")
        return "\n".join(lines)


# Global dry-run context
_context = DryRunContext()


def enable_dryrun():
    """Enable dry-run mode."""
    _context.enabled = True


def disable_dryrun():
    """Disable dry-run mode."""
    _context.enabled = False


def is_dryrun() -> bool:
    """Check if dry-run is enabled."""
    return _context.enabled


def record_operation(action: str, target: str, **details):
    """Record a dry-run operation."""
    _context.record(action, target, **details)


def get_preview() -> str:
    """Get preview of recorded operations."""
    return _context.preview()


def clear_operations():
    """Clear recorded operations."""
    _context.operations.clear()
