#!/usr/bin/env python3
"""Watch pygubu projects for UI changes and sync with code"""
import sys
import json
import time
import pathlib
import hashlib
import logging
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional
from .registry import Registry
from .errors import ProjectNotFoundError

logger = logging.getLogger(__name__)

def get_file_hash(filepath: pathlib.Path) -> Optional[str]:
    """Get SHA256 hash of file"""
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()
    except (OSError, IOError) as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        return None

def load_workflow(project_path: pathlib.Path) -> Dict:
    """Load workflow tracking file"""
    workflow_file = project_path / ".pygubu-workflow.json"
    if workflow_file.exists():
        try:
            return json.loads(workflow_file.read_text())
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to load workflow file: {e}. Using defaults.")
    return {"ui_hash": None, "last_sync": None, "changes": []}

def save_workflow(project_path: pathlib.Path, data: Dict) -> None:
    """Save workflow tracking"""
    workflow_file = project_path / ".pygubu-workflow.json"
    data["last_sync"] = datetime.now(timezone.utc).isoformat()
    try:
        workflow_file.write_text(json.dumps(data, indent=2))
    except (OSError, IOError) as e:
        logger.error(f"Failed to save workflow file: {e}")

def watch_project(project_name: str) -> None:
    """Watch project for UI changes"""
    registry = Registry()
    projects = registry.list_projects()
    
    if project_name not in projects:
        available = ', '.join(projects.keys()) if projects else 'none'
        raise ProjectNotFoundError(project_name, f"Available: {available}")
    
    project_path = pathlib.Path(projects[project_name]).resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise ProjectNotFoundError(project_name, f"Invalid project path: {project_path}")
    
    try:
        ui_files = list(project_path.glob("*.ui"))
    except OSError as e:
        logger.error(f"Failed to scan project directory: {e}")
        return
    
    if not ui_files:
        logger.warning(f"No .ui files in {project_name}")
        return
    
    print(f"👁️  Watching {project_name}...")
    print(f"   Path: {project_path}")
    print(f"   UI files: {len(ui_files)}")
    print("\nPress Ctrl+C to stop\n")
    
    workflow = load_workflow(project_path)
    
    try:
        while True:
            try:
                for ui_file in ui_files:
                    if not ui_file.exists():
                        continue
                    
                    current_hash = get_file_hash(ui_file)
                    if current_hash is None:
                        continue
                    
                    if workflow["ui_hash"] is None:
                        workflow["ui_hash"] = current_hash
                        save_workflow(project_path, workflow)
                    elif current_hash != workflow["ui_hash"]:
                        print(f"🔄 UI changed: {ui_file.name}")
                        print(f"   Time: {datetime.now(timezone.utc).strftime('%H:%M:%S')}")
                        print("\n💡 Suggested action:")
                        print(f"   Tell your AI: 'I updated {ui_file.name}, sync the Python code'")
                        print(f"   Or: 'Review changes in {project_name}'\n")
                        
                        workflow["ui_hash"] = current_hash
                        workflow["changes"].append({
                            "file": str(ui_file),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        })
                        save_workflow(project_path, workflow)
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Error during watch cycle: {e}")
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n✓ Stopped watching")

def main():
    """Main CLI entry point"""
    from . import __version__
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    parser = argparse.ArgumentParser(
        prog='pygubu-ai-workflow',
        description='Watch pygubu projects for UI changes and sync with code'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    watch_parser = subparsers.add_parser('watch', help='Watch project for UI changes')
    watch_parser.add_argument('project_name', help='Name of project to watch')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'watch':
            watch_project(args.project_name)
    except ProjectNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
