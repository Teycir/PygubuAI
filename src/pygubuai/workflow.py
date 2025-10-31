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

try:
    from pydantic import ValidationError
    from .models import WorkflowData, WorkflowHistory

    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    ValidationError = Exception

logger = logging.getLogger(__name__)


def get_file_hash(filepath: pathlib.Path) -> Optional[str]:
    """Get SHA256 hash of file"""
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        return None


def get_file_hash_if_changed(filepath: pathlib.Path, prev_hash: Optional[str], prev_mtime: Optional[float]) -> tuple:
    """Get hash only if mtime changed (optimization)"""
    if not filepath or not isinstance(filepath, pathlib.Path):
        logger.error(f"Invalid filepath: {filepath}")
        return None, None

    try:
        stat = filepath.stat()
        if prev_mtime and stat.st_mtime == prev_mtime:
            return prev_hash, prev_mtime  # Skip hashing

        hash_val = hashlib.sha256(filepath.read_bytes()).hexdigest()
        return hash_val, stat.st_mtime
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        return None, None


def load_workflow(project_path: pathlib.Path) -> Dict:
    """Load workflow tracking file with validation"""
    if not project_path or not isinstance(project_path, pathlib.Path):
        raise ValueError(f"Invalid project_path: {project_path}")

    workflow_file = project_path / ".pygubu-workflow.json"

    if not workflow_file.exists():
        return {"project": project_path.name, "file_hashes": {}, "file_mtimes": {}, "last_sync": None, "history": []}

    try:
        with open(workflow_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            data = {}

        # Convert old format to new format
        if "changes" in data:
            data["history"] = [
                {
                    "timestamp": c.get("timestamp", datetime.now(timezone.utc).isoformat()),
                    "action": "file_changed",
                    "description": f"File {c.get('file', 'unknown')} changed",
                }
                for c in data.pop("changes", [])
            ]
        
        # Validate with Pydantic if available
        if PYDANTIC_AVAILABLE:
            try:
                if "project" not in data:
                    data["project"] = project_path.name
                workflow_model = WorkflowData(**data)
                data = workflow_model.model_dump()
            except ValidationError as e:
                logger.debug(f"Workflow validation failed: {e}, using raw data with defaults")

        data.setdefault("file_hashes", {})
        data.setdefault("file_mtimes", {})
        data.setdefault("last_sync", None)
        data.setdefault("history", [])
        data.setdefault("project", project_path.name)
        return data
    except Exception as e:
        logger.warning(f"Failed to load workflow file: {e}. Using defaults.")
        return {"project": project_path.name, "file_hashes": {}, "file_mtimes": {}, "last_sync": None, "history": []}


def save_workflow(project_path: pathlib.Path, data: Dict) -> None:
    """Save workflow tracking with atomic write and validation."""
    import tempfile
    import shutil

    workflow_file = project_path / ".pygubu-workflow.json"
    data["last_sync"] = datetime.now(timezone.utc).isoformat()

    if PYDANTIC_AVAILABLE:
        try:
            if "project" not in data:
                data["project"] = project_path.name
            workflow_model = WorkflowData(**data)
            data = workflow_model.model_dump()
        except ValidationError as e:
            logger.debug(f"Workflow validation failed before save: {e}, saving raw data")

    if "history" in data and len(data["history"]) > 100:
        data["history"] = data["history"][-100:]
    if "changes" in data and len(data["changes"]) > 100:
        data["changes"] = data["changes"][-100:]

    tmp_path = None
    try:
        # Write to temporary file first (atomic operation)
        with tempfile.NamedTemporaryFile(
            mode="w", dir=project_path, prefix=".pygubu-workflow-", suffix=".tmp", delete=False
        ) as tmp:
            tmp_path = tmp.name
            json.dump(data, tmp, indent=2)

        # Atomic rename (POSIX guarantees atomicity)
        shutil.move(tmp_path, workflow_file)
        tmp_path = None  # Successfully moved, don't clean up

    except Exception as e:
        # Clean up temp file on error
        if tmp_path and pathlib.Path(tmp_path).exists():
            try:
                pathlib.Path(tmp_path).unlink()
            except Exception as cleanup_err:
                logger.debug(f"Failed to clean up temp file: {cleanup_err}")
        logger.error(f"Failed to save workflow file: {e}")
        raise


def get_watch_interval(config: Optional[Config] = None) -> float:
    """Get watch interval from config or default to 2.0s"""
    import os
    env_interval = os.environ.get("PYGUBUAI_WATCH_INTERVAL")
    if env_interval:
        try:
            interval = float(env_interval)
            return interval if interval > 0 else 2.0
        except (ValueError, TypeError):
            pass
    config = config or Config()
    try:
        interval = float(config.get("watch_interval", 2.0))
        return interval if interval > 0 else 2.0
    except (ValueError, TypeError):
        return 2.0


def get_file_patterns(config: Optional[Config] = None) -> List[str]:
    """Get file patterns to watch from config or default to ['*.ui']"""
    import os
    env_patterns = os.environ.get("PYGUBUAI_WATCH_PATTERNS")
    if env_patterns:
        patterns = [p.strip() for p in env_patterns.split(",") if p.strip()]
        if patterns:
            return patterns
    config = config or Config()
    patterns_str = config.get("watch_patterns", "*.ui")
    if isinstance(patterns_str, str):
        patterns = [p.strip() for p in patterns_str.split(",") if p.strip()]
        return patterns if patterns else ["*.ui"]
    elif isinstance(patterns_str, list):
        return patterns_str if patterns_str else ["*.ui"]
    return ["*.ui"]


def watch_project(project_name: str, interval: Optional[float] = None) -> None:
    """Watch project for UI changes with error recovery and circuit breaker."""
    registry = Registry()
    projects = registry.list_projects()

    if project_name not in projects:
        available = ", ".join(projects.keys()) if projects else "none"
        raise ProjectNotFoundError(project_name, f"Available: {available}")

    project_path = pathlib.Path(projects[project_name]).resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise ProjectNotFoundError(project_name, f"Invalid project path: {project_path}")

    config = Config()
    interval = interval if interval is not None else get_watch_interval(config)
    patterns = get_file_patterns(config)

    MAX_FILES = 1000  # Resource limit
    try:
        all_files = [f for pattern in patterns for f in project_path.glob(pattern)]
        if len(all_files) > MAX_FILES:
            logger.warning(f"Project has {len(all_files)} files, limiting to {MAX_FILES}")
            all_files = all_files[:MAX_FILES]
    except Exception as e:
        logger.error(f"Failed to scan project directory: {e}")
        raise RuntimeError(f"Cannot access project directory: {e}") from e

    if not all_files:
        logger.warning(f"No files matching patterns {patterns} in {project_name}")
        return

    print(f"Watching {project_name}...")
    print(f"   Path: {project_path}")
    print(f"   Files: {len(all_files)} matching {patterns}")
    print("\nPress Ctrl+C to stop\n")

    workflow = load_workflow(project_path)
    error_count = 0
    MAX_ERRORS = 5  # Circuit breaker threshold

    try:
        while True:
            try:
                # Rescan files in each loop to detect new/deleted files
                current_files = {f for p in patterns for f in project_path.glob(p)}
                _check_ui_changes(list(current_files), workflow, project_path, project_name)

                # Reset error count on success
                error_count = 0
                time.sleep(interval)

            except KeyboardInterrupt:
                raise

            except Exception as e:
                error_count += 1
                logger.error(f"Error during watch cycle ({error_count}/{MAX_ERRORS}): {e}", exc_info=True)

                # Circuit breaker: stop after too many consecutive errors
                if error_count >= MAX_ERRORS:
                    logger.error(f"Too many consecutive errors ({MAX_ERRORS}), stopping watch")
                    print(f"\n Watch stopped after {MAX_ERRORS} consecutive errors")
                    print("Check logs for details")
                    sys.exit(1)

                # Try to recover workflow state
                try:
                    workflow = load_workflow(project_path)
                except Exception as load_err:
                    logger.error(f"Failed to reload workflow: {load_err}")
                    # Continue with existing workflow

                time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nStopped watching")


def _check_ui_changes(
    ui_files: List[pathlib.Path], workflow: Dict, project_path: pathlib.Path, project_name: str
) -> None:
    """Check UI files for changes and update workflow"""
    for ui_file in ui_files:
        if not ui_file.exists():
            continue

        file_key = ui_file.name
        prev_hash = workflow["file_hashes"].get(file_key)
        prev_mtime = workflow.get("file_mtimes", {}).get(file_key)

        # Use mtime optimization
        current_hash, current_mtime = get_file_hash_if_changed(ui_file, prev_hash, prev_mtime)
        if current_hash is None:
            continue

        if prev_hash is None:
            workflow["file_hashes"][file_key] = current_hash
            workflow.setdefault("file_mtimes", {})[file_key] = current_mtime
            save_workflow(project_path, workflow)
        elif current_hash != prev_hash:
            _notify_ui_change(ui_file, project_name)
            workflow["file_hashes"][file_key] = current_hash
            workflow.setdefault("file_mtimes", {})[file_key] = current_mtime

            if "history" not in workflow:
                workflow["history"] = []
            if len(workflow["history"]) >= 99:
                workflow["history"] = workflow["history"][-98:]

            workflow["history"].append(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "action": "file_changed",
                    "description": f"File {ui_file.name} changed",
                }
            )
            save_workflow(project_path, workflow)


def _notify_ui_change(ui_file: pathlib.Path, project_name: str) -> None:
    """Print notification when UI file changes"""
    print(f" UI changed: {ui_file.name}")
    print(f"   Time: {datetime.now(timezone.utc).strftime('%H:%M:%S')}")
    print("\nSuggested action:")
    print(f"   Tell your AI: 'I updated {ui_file.name}, sync the Python code'")
    print(f"   Or: 'Review changes in {project_name}'\n")


def main():
    """Main CLI entry point"""
    from . import __version__

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(
        prog="pygubu-ai-workflow", description="Watch pygubu projects for UI changes and sync with code"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    watch_parser = subparsers.add_parser("watch", help="Watch project for UI changes")
    watch_parser.add_argument("project_name", help="Name of project to watch")
    watch_parser.add_argument(
        "--interval", type=float, metavar="SECONDS", help="Poll interval in seconds (default: from config or 2.0)"
    )

    args = parser.parse_args()

    try:
        if args.command == "watch":
            watch_project(args.project_name, interval=args.interval)
    except ProjectNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


class WorkflowTracker:
    """Tracks workflow events for a project"""

    def __init__(self, project_path: str):
        from pathlib import Path
        self.project_path = Path(project_path)
        self.workflow_file = self.project_path / ".pygubu-workflow.json"

    def add_event(self, action: str, description: str):
        """Add a workflow event"""
        workflow = load_workflow(self.project_path)

        if "history" not in workflow:
            workflow["history"] = []

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "description": description
        }

        workflow["history"].append(event)

        # Keep only last 100 events
        if len(workflow["history"]) > 100:
            workflow["history"] = workflow["history"][-100:]

        save_workflow(self.project_path, workflow)

    def get_history(self) -> list:
        """Get workflow history"""
        workflow = load_workflow(self.project_path)
        return workflow.get("history", [])
