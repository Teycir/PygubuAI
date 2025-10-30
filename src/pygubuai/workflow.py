#!/usr/bin/env python3
"""Watch pygubu projects for UI changes and sync with code"""
import sys
import json
import time
import pathlib
import hashlib
import logging
import argparse
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from .registry import Registry
from .errors import ProjectNotFoundError

logger = logging.getLogger(__name__)

def get_watch_interval() -> float:
    """Get watch interval from environment or default"""
    return float(os.environ.get('PYGUBUAI_WATCH_INTERVAL', '2.0'))

def get_file_patterns() -> List[str]:
    """Get file patterns to watch from environment or default"""
    patterns = os.environ.get('PYGUBUAI_WATCH_PATTERNS', '*.ui')
    return [p.strip() for p in patterns.split(',')]

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
    return {"ui_hash": None, "last_sync": None, "changes": [], "file_hashes": {}}

def save_workflow(project_path: pathlib.Path, data: Dict) -> None:
    """Save workflow tracking"""
    workflow_file = project_path / ".pygubu-workflow.json"
    data["last_sync"] = datetime.now(timezone.utc).isoformat()
    try:
        workflow_file.write_text(json.dumps(data, indent=2))
    except (OSError, IOError) as e:
        logger.error(f"Failed to save workflow file: {e}")

def watch_project(project_name: str, interval: Optional[float] = None, patterns: Optional[List[str]] = None) -> None:
    """Watch project for UI changes"""
    registry = Registry()
    projects = registry.list_projects()
    
    if project_name not in projects:
        available = ', '.join(projects.keys()) if projects else 'none'
        raise ProjectNotFoundError(project_name, f"Available: {available}")
    
    project_path = pathlib.Path(projects[project_name]).resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise ProjectNotFoundError(project_name, f"Invalid project path: {project_path}")
    
    interval = interval or get_watch_interval()
    patterns = patterns or get_file_patterns()
    
    try:
        ui_files = []
        for pattern in patterns:
            ui_files.extend(project_path.glob(pattern))
    except OSError as e:
        logger.error(f"Failed to scan project directory: {e}")
        return
    
    if not ui_files:
        logger.warning(f"No files matching {patterns} in {project_name}")
        return
    
    print(f"👁️  Watching {project_name}...")
    print(f"   Path: {project_path}")
    print(f"   Files: {len(ui_files)} ({', '.join(patterns)})")
    print(f"   Interval: {interval}s")
    print("\nPress Ctrl+C to stop\n")
    
    workflow = load_workflow(project_path)
    if "file_hashes" not in workflow:
        workflow["file_hashes"] = {}
    
    try:
        while True:
            try:
                for ui_file in ui_files:
                    if not ui_file.exists():
                        continue
                    
                    current_hash = get_file_hash(ui_file)
                    if current_hash is None:
                        continue
                    
                    file_key = ui_file.name
                    prev_hash = workflow["file_hashes"].get(file_key)
                    
                    if prev_hash is None:
                        workflow["file_hashes"][file_key] = current_hash
                        save_workflow(project_path, workflow)
                    elif current_hash != prev_hash:
                        print(f"🔄 UI changed: {ui_file.name}")
                        print(f"   Time: {datetime.now(timezone.utc).strftime('%H:%M:%S')}")
                        print("\n💡 Suggested action:")
                        print(f"   Tell your AI: 'I updated {ui_file.name}, sync the Python code'")
                        print(f"   Or: 'Review changes in {project_name}'\n")
                        
                        workflow["file_hashes"][file_key] = current_hash
                        workflow["changes"].append({
                            "file": ui_file.name,
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        })
                        save_workflow(project_path, workflow)
                
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error during watch cycle: {e}")
                time.sleep(interval)
    
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
    
    watch_parser = subparsers.add_parser('watch', help='Watch project(s) for UI changes')
    watch_parser.add_argument('project_name', help='Project name(s), comma-separated or "all"')
    watch_parser.add_argument('--interval', type=float, help='Watch interval in seconds (default: 2.0)')
    watch_parser.add_argument('--patterns', help='File patterns to watch, comma-separated (default: *.ui)')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'watch':
            patterns = [p.strip() for p in args.patterns.split(',')] if args.patterns else None
            
            if args.project_name == 'all':
                from .multi_watch import watch_all_projects
                watch_all_projects(interval=args.interval, patterns=patterns)
            elif ',' in args.project_name:
                from .multi_watch import watch_multiple_projects
                projects = [p.strip() for p in args.project_name.split(',')]
                watch_multiple_projects(projects, interval=args.interval, patterns=patterns)
            else:
                watch_project(args.project_name, interval=args.interval, patterns=patterns)
    except ProjectNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
