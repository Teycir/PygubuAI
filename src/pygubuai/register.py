#!/usr/bin/env python3
"""Register and manage pygubu projects globally"""
import sys
import pathlib
import logging
from datetime import datetime
from typing import Optional, Dict, List
from .registry import Registry
from .errors import ProjectNotFoundError, InvalidProjectError

logger = logging.getLogger(__name__)

def register_project(path: str) -> None:
    """Register a pygubu project"""
    project_path = pathlib.Path(path).resolve()
    if not project_path.exists():
        raise InvalidProjectError(str(path), "path does not exist")
    
    ui_files = list(project_path.glob("*.ui"))
    if not ui_files:
        raise InvalidProjectError(str(path), "no .ui files found")
    
    registry = Registry()
    project_name = project_path.name
    
    registry.add_project(project_name, str(project_path))
    
    print(f"✓ Registered: {project_name}")
    print(f"  Path: {project_path}")
    print(f"  UI files: {len(ui_files)}")

def set_active(project_name: str) -> None:
    """Set active project"""
    registry = Registry()
    projects = registry.list_projects()
    
    if project_name not in projects:
        available = ', '.join(projects.keys()) if projects else 'none'
        raise ProjectNotFoundError(project_name, f"Available: {available}")
    
    registry.set_active(project_name)
    print(f"✓ Active project: {project_name}")

def list_projects() -> None:
    """List all registered projects"""
    registry = Registry()
    projects = registry.list_projects()
    active = registry.get_active()
    
    if not projects:
        print("No projects registered")
        print("\nRegister a project:")
        print("  pygubu-register add /path/to/project")
        return
    
    print("📁 Registered Pygubu Projects:\n")
    for name, path in projects.items():
        active_marker = " ⭐" if name == active else ""
        project_path = pathlib.Path(path)
        ui_files = list(project_path.glob("*.ui")) if project_path.exists() else []
        print(f"  {name}{active_marker}")
        print(f"    Path: {path}")
        print(f"    UI files: {len(ui_files)}")
        print()

def get_active() -> Optional[str]:
    """Get active project info"""
    registry = Registry()
    active_name = registry.get_active()
    
    if not active_name:
        print("No active project")
        return None
    
    project_path = registry.get_project(active_name)
    if project_path:
        import json
        path_obj = pathlib.Path(project_path)
        ui_files = list(path_obj.glob("*.ui")) if path_obj.exists() else []
        py_files = list(path_obj.glob("*.py")) if path_obj.exists() else []
        print(json.dumps({
            "name": active_name,
            "path": project_path,
            "ui_files": [str(f) for f in ui_files],
            "py_files": [str(f) for f in py_files]
        }, indent=2))
    return project_path

def scan_directory(directory: str = ".") -> None:
    """Auto-scan directory for pygubu projects"""
    base = pathlib.Path(directory).resolve()
    if not base.exists():
        raise InvalidProjectError(str(directory), "directory does not exist")
    
    found = []
    for item in base.rglob("*.ui"):
        project_dir = item.parent
        if project_dir not in found:
            found.append(project_dir)
    
    if not found:
        print(f"No pygubu projects found in {directory}")
        return
    
    print(f"Found {len(found)} project(s):\n")
    registry = Registry()
    
    for proj_dir in found:
        name = proj_dir.name
        print(f"  {name} - {proj_dir}")
        registry.add_project(name, str(proj_dir))
    
    print(f"\n✓ Registered {len(found)} project(s)")

def main():
    """Main CLI entry point"""
    from . import __version__
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    if '--version' in sys.argv:
        print(f"pygubu-register {__version__}")
        return
    
    if '--help' in sys.argv or len(sys.argv) < 2:
        print(f"pygubu-register {__version__}")
        print("\nCommands:")
        print("  add <path>      - Register a project")
        print("  active <name>   - Set active project")
        print("  list            - List all projects")
        print("  info            - Show active project")
        print("  scan [dir]      - Auto-scan for projects")
        print("\nExamples:")
        print("  pygubu-register add ~/number_game")
        print("  pygubu-register active number_game")
        print("  pygubu-register scan ~/projects")
        sys.exit(0 if '--help' in sys.argv else 1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == "add" and len(sys.argv) == 3:
            register_project(sys.argv[2])
        elif cmd == "active" and len(sys.argv) == 3:
            set_active(sys.argv[2])
        elif cmd == "list":
            list_projects()
        elif cmd == "info":
            get_active()
        elif cmd == "scan":
            directory = sys.argv[2] if len(sys.argv) == 3 else "."
            scan_directory(directory)
        else:
            print("Invalid command")
            sys.exit(1)
    except (ProjectNotFoundError, InvalidProjectError) as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
