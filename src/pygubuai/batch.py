#!/usr/bin/env python3
"""Batch operations across multiple projects"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict
from .registry import Registry
from .theme import apply_theme
from .validate_project import validate_project

def rename_widget(project_name: str, old_id: str, new_id: str) -> bool:
    """Rename widget ID in project"""
    registry = Registry()
    project_path = registry.get_project(project_name)
    
    if not project_path:
        return False
    
    ui_file = Path(project_path) / f"{project_name}.ui"
    if not ui_file.exists():
        return False
    
    # Parse and modify
    tree = ET.parse(ui_file)
    root = tree.getroot()
    
    widget = root.find(f".//object[@id='{old_id}']")
    if widget is None:
        return False
    
    widget.set("id", new_id)
    
    # Update references in Python file
    py_file = Path(project_path) / f"{project_name}.py"
    if py_file.exists():
        content = py_file.read_text()
        content = content.replace(f"'{old_id}'", f"'{new_id}'")
        content = content.replace(f'"{old_id}"', f'"{new_id}"')
        py_file.write_text(content)
    
    tree.write(ui_file, encoding='utf-8', xml_declaration=True)
    return True

def batch_update_theme(theme_name: str, projects: List[str] = None) -> Dict[str, bool]:
    """Apply theme to multiple projects"""
    registry = Registry()
    
    if projects is None:
        projects = list(registry.list_projects().keys())
    
    results = {}
    for project in projects:
        try:
            apply_theme(project, theme_name, backup=True)
            results[project] = True
        except Exception as e:
            results[project] = False
    
    return results

def batch_validate(projects: List[str] = None) -> Dict[str, List]:
    """Validate multiple projects"""
    registry = Registry()
    
    if projects is None:
        projects = list(registry.list_projects().keys())
    
    results = {}
    for project in projects:
        issues = validate_project(project)
        results[project] = issues
    
    return results

def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: pygubu-batch <command> [args]")
        print("\\nCommands:")
        print("  rename-widget <project> <old_id> <new_id>")
        print("  update-theme <theme> [projects...]")
        print("  validate [projects...]")
        print("\\nExamples:")
        print("  pygubu-batch rename-widget myapp btn_old btn_new")
        print("  pygubu-batch update-theme clam")
        print("  pygubu-batch validate myapp1 myapp2")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "rename-widget":
        if len(sys.argv) < 5:
            print("Usage: pygubu-batch rename-widget <project> <old_id> <new_id>")
            sys.exit(1)
        
        project = sys.argv[2]
        old_id = sys.argv[3]
        new_id = sys.argv[4]
        
        if rename_widget(project, old_id, new_id):
            print(f"✓ Renamed '{old_id}' to '{new_id}' in project '{project}'")
        else:
            print(f"✗ Failed to rename widget in '{project}'")
            sys.exit(1)
    
    elif command == "update-theme":
        if len(sys.argv) < 3:
            print("Usage: pygubu-batch update-theme <theme> [projects...]")
            sys.exit(1)
        
        theme = sys.argv[2]
        projects = sys.argv[3:] if len(sys.argv) > 3 else None
        
        print(f"\\nApplying theme '{theme}' to projects...\\n")
        results = batch_update_theme(theme, projects)
        
        success = sum(1 for v in results.values() if v)
        failed = len(results) - success
        
        for project, status in results.items():
            symbol = "✓" if status else "✗"
            print(f"  {symbol} {project}")
        
        print(f"\\nCompleted: {success} succeeded, {failed} failed")
    
    elif command == "validate":
        projects = sys.argv[2:] if len(sys.argv) > 2 else None
        
        print("\\nValidating projects...\\n")
        results = batch_validate(projects)
        
        for project, issues in results.items():
            errors = sum(1 for i in issues if i.severity == "error")
            warnings = sum(1 for i in issues if i.severity == "warning")
            
            if not issues:
                print(f"  ✓ {project}: No issues")
            else:
                print(f"  ⚠️  {project}: {errors} errors, {warnings} warnings")
        
        total_issues = sum(len(issues) for issues in results.values())
        print(f"\\nTotal issues found: {total_issues}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
