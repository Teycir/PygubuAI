#!/usr/bin/env python3
"""Watch pygubu projects for UI changes and sync with code."""
import sys
import json
import time
import pathlib
import hashlib
import logging
from datetime import datetime
from typing import Dict, List, Optional
from .registry import Registry
from .errors import ProjectNotFoundError
from .logging_config import get_logger

logger = get_logger(__name__)

def get_file_hash(filepath: pathlib.Path) -> str:
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

def load_workflow(project_path: pathlib.Path) -> Dict:
    """Load workflow tracking data from project directory.
    
    Args:
        project_path: Path to project directory
        
    Returns:
        Workflow tracking dictionary with keys:
        - ui_hash: Last known UI file hash
        - last_sync: ISO timestamp of last sync
        - changes: List of change records
    """
    workflow_file = project_path / ".pygubu-workflow.json"
    if workflow_file.exists():
        try:
            return json.loads(workflow_file.read_text())
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid workflow file, using defaults: {e}")
    return {"ui_hash": None, "last_sync": None, "changes": []}

def save_workflow(project_path: pathlib.Path, data: Dict) -> None:
    """Save workflow tracking data to project directory.
    
    Args:
        project_path: Path to project directory
        data: Workflow data dictionary to save
        
    Raises:
        OSError: If unable to write workflow file
    """
    workflow_file = project_path / ".pygubu-workflow.json"
    data["last_sync"] = datetime.now().isoformat()
    try:
        workflow_file.write_text(json.dumps(data, indent=2))
        logger.debug(f"Saved workflow to {workflow_file}")
    except OSError as e:
        logger.error(f"Failed to save workflow: {e}")
        raise

def watch_project(project_name: str) -> None:
    """Watch project for UI file changes and suggest sync actions.
    
    Monitors .ui files in the project directory and detects changes
    by comparing file hashes. When changes are detected, suggests
    appropriate AI sync commands to the user.
    
    Args:
        project_name: Name of registered project to watch
        
    Raises:
        ProjectNotFoundError: If project is not registered
    """
    logger.debug(f"Starting watch for project: {project_name}")
    registry = Registry()
    projects = registry.list_projects()
    
    if project_name not in projects:
        available = ', '.join(projects.keys()) if projects else 'none'
        logger.error(f"Project '{project_name}' not found")
        raise ProjectNotFoundError(project_name, f"Available: {available}")
    
    project_path = pathlib.Path(projects[project_name])
    if not project_path.exists():
        logger.error(f"Project path does not exist: {project_path}")
        return
    
    ui_files = list(project_path.glob("*.ui"))
    
    if not ui_files:
        logger.warning(f"No .ui files found in {project_name}")
        return
    
    print(f"👁️  Watching {project_name}...")
    print(f"   Path: {project_path}")
    print(f"   UI files: {len(ui_files)}")
    print("\nPress Ctrl+C to stop\n")
    
    workflow = load_workflow(project_path)
    
    try:
        while True:
            for ui_file in ui_files:
                if not ui_file.exists():
                    continue
                
                current_hash = get_file_hash(ui_file)
                
                if workflow["ui_hash"] is None:
                    workflow["ui_hash"] = current_hash
                    save_workflow(project_path, workflow)
                elif current_hash != workflow["ui_hash"]:
                    print(f"🔄 UI changed: {ui_file.name}")
                    print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                    print("\n💡 Suggested action:")
                    print(f"   Tell your AI: 'I updated {ui_file.name}, sync the Python code'")
                    print(f"   Or: 'Review changes in {project_name}'\n")
                    
                    workflow["ui_hash"] = current_hash
                    workflow["changes"].append({
                        "file": str(ui_file),
                        "timestamp": datetime.now().isoformat()
                    })
                    save_workflow(project_path, workflow)
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n✓ Stopped watching")

def main():
    """Main CLI entry point"""
    from . import __version__
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    if '--version' in sys.argv:
        print(f"pygubu-ai-workflow {__version__}")
        return
    
    if '--help' in sys.argv or len(sys.argv) < 3 or sys.argv[1] != "watch":
        print(f"pygubu-ai-workflow {__version__}")
        print("\nUsage: pygubu-ai-workflow watch <project_name>")
        print("\nExample:")
        print("  pygubu-ai-workflow watch myapp")
        print("\nThis monitors .ui file changes and suggests AI sync actions")
        sys.exit(0 if '--help' in sys.argv else 1)
    
    try:
        watch_project(sys.argv[2])
    except ProjectNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception:
        logger.exception("An unexpected error occurred while watching the project.")
        sys.exit(1)

if __name__ == '__main__':
    main()
