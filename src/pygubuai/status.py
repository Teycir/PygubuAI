#!/usr/bin/env python3
"""Project status checker"""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from .registry import Registry
from .utils import validate_path

try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def get_project_status(project_name: Optional[str] = None) -> Dict:
    """Get project sync status"""
    registry = Registry()
    
    if not project_name:
        project_name = registry.get_active()
        if not project_name:
            return {"error": "No active project. Use: pygubu-register active <name>"}
    
    project_path = registry.get_project(project_name)
    if not project_path:
        return {"error": f"Project '{project_name}' not found"}
    
    project_dir = validate_path(project_path, must_exist=True, must_be_dir=True)
    ui_file = project_dir / f"{project_name}.ui"
    py_file = project_dir / f"{project_name}.py"
    workflow_file = project_dir / ".pygubu-workflow.json"
    
    if not ui_file.exists():
        return {"error": f"UI file not found: {ui_file}"}
    if not py_file.exists():
        return {"error": f"Python file not found: {py_file}"}
    
    ui_mtime = ui_file.stat().st_mtime
    py_mtime = py_file.stat().st_mtime
    
    status = {
        "project": project_name,
        "path": str(project_dir),
        "ui_file": str(ui_file),
        "py_file": str(py_file),
        "ui_modified": datetime.fromtimestamp(ui_mtime).isoformat(),
        "py_modified": datetime.fromtimestamp(py_mtime).isoformat(),
    }
    
    # Check workflow history
    if workflow_file.exists():
        try:
            with open(workflow_file) as f:
                workflow = json.load(f)
                status["last_sync"] = workflow.get("history", [{}])[-1].get("timestamp", "Never")
        except:
            status["last_sync"] = "Unknown"
    else:
        status["last_sync"] = "Never"
    
    # Determine sync status
    time_diff = abs(ui_mtime - py_mtime)
    if time_diff < 2:  # Within 2 seconds
        status["sync_status"] = "In Sync"
    elif ui_mtime > py_mtime:
        status["sync_status"] = "UI Ahead"
        status["message"] = "UI file modified after Python file. Consider updating code."
    else:
        status["sync_status"] = "Code Ahead"
        status["message"] = "Python file modified after UI. Consider updating UI."
    
    return status

def main():
    """CLI entry point"""
    import sys
    project_name = sys.argv[1] if len(sys.argv) > 1 else None
    
    status = get_project_status(project_name)
    
    if "error" in status:
        print(f"Error: {status['error']}")
        sys.exit(1)
    
    if RICH_AVAILABLE:
        console = Console()
        table = Table(title=f"Project Status: {status['project']}")
        table.add_column("Component", style="cyan")
        table.add_column("Value", style="green")
        
        status_color = "green" if status['sync_status'] == "In Sync" else "yellow"
        table.add_row("Status", f"[{status_color}]{status['sync_status']}[/{status_color}]")
        table.add_row("UI Modified", status['ui_modified'])
        table.add_row("Code Modified", status['py_modified'])
        table.add_row("Last Sync", status['last_sync'])
        
        console.print(table)
        if "message" in status:
            console.print(f"\nWARNING  [yellow]{status['message']}[/yellow]")
    else:
        print(f"Project: {status['project']}")
        print(f"Status: {status['sync_status']}")
        print(f"UI Modified: {status['ui_modified']}")
        print(f"Code Modified: {status['py_modified']}")
        print(f"Last Sync: {status['last_sync']}")
        if "message" in status:
            print(f"\nWARNING  {status['message']}")

def check_project_status(project_name: Optional[str] = None) -> Dict:
    """Alias for get_project_status for backward compatibility"""
    return get_project_status(project_name)
if __name__ == "__main__":
    main()
