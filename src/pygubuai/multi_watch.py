"""Multi-project watch mode"""
import time
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime, timezone

from .workflow import get_file_hash, load_workflow, save_workflow, get_watch_interval, get_file_patterns
from .registry import Registry
from .errors import ProjectNotFoundError

logger = logging.getLogger(__name__)


def watch_multiple_projects(project_names: List[str], interval: float = None, patterns: List[str] = None):
    """Watch multiple projects simultaneously"""
    registry = Registry()
    all_projects = registry.list_projects()
    
    # Validate all projects exist
    projects_to_watch = {}
    for name in project_names:
        if name not in all_projects:
            raise ProjectNotFoundError(name, f"Project not found: {name}")
        projects_to_watch[name] = Path(all_projects[name])
    
    interval = interval or get_watch_interval()
    patterns = patterns or get_file_patterns()
    
    # Initialize workflows for all projects
    workflows = {}
    for name, path in projects_to_watch.items():
        workflows[name] = load_workflow(path)
        if "file_hashes" not in workflows[name]:
            workflows[name]["file_hashes"] = {}
    
    print(f"👁️  Watching {len(projects_to_watch)} project(s)...")
    for name, path in projects_to_watch.items():
        ui_files = []
        for pattern in patterns:
            ui_files.extend(path.glob(pattern))
        print(f"   {name}: {len(ui_files)} files")
    print(f"   Interval: {interval}s\n")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            for name, path in projects_to_watch.items():
                _check_project_changes(name, path, workflows[name], patterns)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n✓ Stopped watching")


def _check_project_changes(name: str, path: Path, workflow: Dict, patterns: List[str]):
    """Check single project for changes"""
    ui_files = []
    for pattern in patterns:
        ui_files.extend(path.glob(pattern))
    
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
            save_workflow(path, workflow)
        elif current_hash != prev_hash:
            print(f"🔄 [{name}] {ui_file.name} changed at {datetime.now(timezone.utc).strftime('%H:%M:%S')}")
            workflow["file_hashes"][file_key] = current_hash
            workflow["changes"].append({
                "file": ui_file.name,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            save_workflow(path, workflow)


def watch_all_projects(interval: float = None, patterns: List[str] = None):
    """Watch all registered projects"""
    registry = Registry()
    projects = registry.list_projects()
    
    if not projects:
        print("No projects registered")
        return
    
    watch_multiple_projects(list(projects.keys()), interval, patterns)
