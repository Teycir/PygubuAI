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
from .config import Config

logger = logging.getLogger(__name__)

def get_file_hash(filepath: pathlib.Path) -> Optional[str]:
    """Get SHA256 hash of file"""
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        return None

def load_workflow(project_path: pathlib.Path) -> Dict:
    """Load workflow tracking file"""
    workflow_file = project_path / ".pygubu-workflow.json"
    
    if not workflow_file.exists():
        return {"file_hashes": {}, "last_sync": None, "changes": []}
    
    try:
        data = json.loads(workflow_file.read_text())
        if not isinstance(data, dict):
            data = {}
        # Ensure required keys exist
        data.setdefault("file_hashes", {})
        data.setdefault("last_sync", None)
        data.setdefault("changes", [])
        return data
    except Exception as e:
        logger.warning(f"Failed to load workflow file: {e}. Using defaults.")
        return {"file_hashes": {}, "last_sync": None, "changes": []}

def save_workflow(project_path: pathlib.Path, data: Dict) -> None:
    """Save workflow tracking"""
    workflow_file = project_path / ".pygubu-workflow.json"
    data["last_sync"] = datetime.now(timezone.utc).isoformat()
    # Limit changes history to last 100 entries
    if "changes" in data and len(data["changes"]) > 100:
        data["changes"] = data["changes"][-100:]
    try:
        workflow_file.write_text(json.dumps(data, indent=2))
    except Exception as e:
        logger.error(f"Failed to save workflow file: {e}")

def get_watch_interval() -> float:
    """Get watch interval from config or default to 2.0s"""
    try:
        interval = float(Config().get("watch_interval", 2.0))
        return interval if interval > 0 else 2.0
    except (ValueError, TypeError):
        return 2.0

def get_file_patterns() -> List[str]:
    """Get file patterns to watch from config or default to ['*.ui']"""
    patterns_str = Config().get("watch_patterns", "*.ui")
    if isinstance(patterns_str, str):
        patterns = [p.strip() for p in patterns_str.split(',') if p.strip()]
        return patterns if patterns else ["*.ui"]
    elif isinstance(patterns_str, list):
        return patterns_str if patterns_str else ["*.ui"]
    return ["*.ui"]

def watch_project(project_name: str, interval: Optional[float] = None) -> None:
    """Watch project for UI changes"""
    registry = Registry()
    projects = registry.list_projects()
    
    if project_name not in projects:
        available = ', '.join(projects.keys()) if projects else 'none'
        raise ProjectNotFoundError(project_name, f"Available: {available}")
    
    project_path = pathlib.Path(projects[project_name]).resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise ProjectNotFoundError(project_name, f"Invalid project path: {project_path}")
    
    interval = interval if interval is not None else get_watch_interval()
    patterns = get_file_patterns()
    
    try:
        all_files = [f for pattern in patterns for f in project_path.glob(pattern)]
    except Exception as e:
        logger.error(f"Failed to scan project directory: {e}")
        raise RuntimeError(f"Cannot access project directory: {e}") from e
    
    if not all_files:
        logger.warning(f"No files matching patterns {patterns} in {project_name}")
        return
    
    print(f"👁️  Watching {project_name}...")
    print(f"   Path: {project_path}")
    print(f"   Files: {len(all_files)} matching {patterns}")
    print("\nPress Ctrl+C to stop\n")
    
    workflow = load_workflow(project_path)
    
    try:
        while True:
            try:
                # Rescan files in each loop to detect new/deleted files
                current_files = {f for p in patterns for f in project_path.glob(p)}
                _check_ui_changes(list(current_files), workflow, project_path, project_name)
                time.sleep(interval)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logger.error(f"Error during watch cycle: {e}", exc_info=True)
                workflow = load_workflow(project_path)
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n✓ Stopped watching")

def _check_ui_changes(ui_files: List[pathlib.Path], workflow: Dict, 
                      project_path: pathlib.Path, project_name: str) -> None:
    """Check UI files for changes and update workflow"""
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
            _notify_ui_change(ui_file, project_name)
            workflow["file_hashes"][file_key] = current_hash
            workflow.setdefault("changes", []).append({
                "file": ui_file.name,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            save_workflow(project_path, workflow)

def _notify_ui_change(ui_file: pathlib.Path, project_name: str) -> None:
    """Print notification when UI file changes"""
    print(f"🔄 UI changed: {ui_file.name}")
    print(f"   Time: {datetime.now(timezone.utc).strftime('%H:%M:%S')}")
    print("\n💡 Suggested action:")
    print(f"   Tell your AI: 'I updated {ui_file.name}, sync the Python code'")
    print(f"   Or: 'Review changes in {project_name}'\n")

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
    watch_parser.add_argument('--interval', type=float, metavar='SECONDS',
                             help='Poll interval in seconds (default: from config or 2.0)')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'watch':
            watch_project(args.project_name, interval=args.interval)
    except ProjectNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
