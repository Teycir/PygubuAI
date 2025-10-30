#!/usr/bin/env python3
"""Register and manage pygubu projects globally"""
import sys
import pathlib
import logging
import argparse
from datetime import datetime
from typing import Optional, Dict, List
from .registry import Registry
from .errors import ProjectNotFoundError, InvalidProjectError

logger = logging.getLogger(__name__)

def register_project(path: str, description: str = "", tags: List[str] = None) -> None:
    """Register a pygubu project"""
    project_path = pathlib.Path(path).resolve()
    if not project_path.exists():
        raise InvalidProjectError(str(path), "path does not exist")
    
    ui_files = list(project_path.glob("*.ui"))
    if not ui_files:
        raise InvalidProjectError(str(path), "no .ui files found")
    
    registry = Registry()
    project_name = project_path.name
    
    registry.add_project(project_name, str(project_path), description=description, tags=tags or [])
    
    print(f"[SUCCESS] Registered: {project_name}")
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
    print(f"[SUCCESS] Active project: {project_name}")

def list_projects(show_metadata: bool = False) -> None:
    """List all registered projects"""
    registry = Registry()
    projects = registry.list_projects_with_metadata() if show_metadata else registry.list_projects()
    active = registry.get_active()
    
    if not projects:
        print("No projects registered")
        print("\nRegister a project:")
        print("  pygubu-register add /path/to/project")
        return
    
    print("Registered Pygubu Projects:\n")
    for name, data in projects.items():
        active_marker = " [ACTIVE]" if name == active else ""
        
        if isinstance(data, dict):
            path = data['path']
            description = data.get('description', '')
            tags = data.get('tags', [])
            created = data.get('created', '')
        else:
            path = data
            description = tags = created = ''
        
        project_path = pathlib.Path(path)
        ui_files = list(project_path.glob("*.ui")) if project_path.exists() else []
        
        print(f"  {name}{active_marker}")
        print(f"    Path: {path}")
        print(f"    UI files: {len(ui_files)}")
        
        if show_metadata:
            if description:
                print(f"    Description: {description}")
            if tags:
                print(f"    Tags: {', '.join(tags)}")
            if created:
                print(f"    Created: {created[:10]}")
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
        registry.add_project(name, str(proj_dir), description="Auto-discovered project")
    
    print(f"\n[SUCCESS] Registered {len(found)} project(s)")

def search_projects(query: str) -> None:
    """Search projects by name, description, or tags"""
    registry = Registry()
    results = registry.search_projects(query)
    
    if not results:
        print(f"No projects found matching '{query}'")
        return
    
    print(f"Found {len(results)} project(s) matching '{query}':\n")
    for name, metadata in results.items():
        print(f"  {name}")
        print(f"    Path: {metadata['path']}")
        if metadata.get('description'):
            print(f"    Description: {metadata['description']}")
        if metadata.get('tags'):
            print(f"    Tags: {', '.join(metadata['tags'])}")
        print()

def main():
    """Main CLI entry point"""
    from . import __version__
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    parser = argparse.ArgumentParser(
        description="Register and manage pygubu projects globally.",
        epilog="Examples:\n"
               "  pygubu-register add ~/number_game\n"
               "  pygubu-register active number_game\n"
               "  pygubu-register scan ~/projects",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', action='version', version=f"pygubu-register {__version__}"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    add_parser = subparsers.add_parser('add', help='Register a project')
    add_parser.add_argument('path', help='Path to the project directory')
    
    active_parser = subparsers.add_parser('active', help='Set active project')
    active_parser.add_argument('name', help='Name of the project to set as active')
    
    list_parser = subparsers.add_parser('list', help='List all registered projects')
    list_parser.add_argument('--metadata', '-m', action='store_true', help='Show full metadata')
    
    subparsers.add_parser('info', help='Show active project information')
    
    scan_parser = subparsers.add_parser('scan', help='Auto-scan directory for projects')
    scan_parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current directory)')
    
    search_parser = subparsers.add_parser('search', help='Search projects by name, description, or tags')
    search_parser.add_argument('query', help='Search query')
    
    add_parser.add_argument('--description', '-d', help='Project description')
    add_parser.add_argument('--tags', '-t', help='Comma-separated tags')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'add':
            tags = [t.strip() for t in args.tags.split(',')] if hasattr(args, 'tags') and args.tags else None
            description = args.description if hasattr(args, 'description') else ""
            register_project(args.path, description=description, tags=tags)
        elif args.command == 'active':
            set_active(args.name)
        elif args.command == 'list':
            show_metadata = args.metadata if hasattr(args, 'metadata') else False
            list_projects(show_metadata=show_metadata)
        elif args.command == 'info':
            get_active()
        elif args.command == 'scan':
            scan_directory(args.directory)
        elif args.command == 'search':
            search_projects(args.query)
        else:
            parser.print_help()
    except (ProjectNotFoundError, InvalidProjectError) as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
