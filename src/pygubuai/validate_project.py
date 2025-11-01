#!/usr/bin/env python3
"""Project validator for common issues"""
from pathlib import Path
from typing import List
import re
from .registry import Registry

try:
    from rich.console import Console
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ValidationIssue:
    def __init__(self, severity: str, category: str, message: str, location: str = ""):
        self.severity = severity  # error, warning, info
        self.category = category
        self.message = message
        self.location = location

    def __repr__(self):
        loc = f" ({self.location})" if self.location else ""
        return f"[{self.severity.upper()}] {self.category}: {self.message}{loc}"


def validate_project(project_name: str) -> List[ValidationIssue]:
    """Validate project for common issues"""
    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return [ValidationIssue("error", "Project", f"Project '{project_name}' not found")]

    project_dir = Path(project_path)
    ui_file = project_dir / f"{project_name}.ui"
    py_file = project_dir / f"{project_name}.py"

    issues = []

    # Check file existence
    if not ui_file.exists():
        issues.append(ValidationIssue("error", "Files", f"UI file missing: {ui_file}"))
        return issues

    if not py_file.exists():
        issues.append(ValidationIssue("warning", "Files", f"Python file missing: {py_file}"))

    # Validate UI file
    try:
        from defusedxml.ElementTree import parse
        tree = parse(ui_file)
        root = tree.getroot()

        # Check for duplicate IDs
        widget_ids = []
        for obj in root.findall(".//object[@id]"):
            widget_id = obj.get("id")
            if widget_id in widget_ids:
                issues.append(ValidationIssue("error", "UI", f"Duplicate widget ID: {widget_id}"))
            widget_ids.append(widget_id)

        # Check for missing IDs
        for obj in root.findall(".//object"):
            if not obj.get("id"):
                widget_class = obj.get("class", "unknown")
                issues.append(ValidationIssue("warning", "UI", f"Widget without ID: {widget_class}"))

        # Check for callbacks
        callbacks = set()
        for prop in root.findall(".//property[@name='command']"):
            if prop.text:
                callbacks.add(prop.text)

        # Validate Python file if exists
        if py_file.exists():
            py_content = py_file.read_text()

            # Check if callbacks are defined
            for callback in callbacks:
                if f"def {callback}" not in py_content:
                    issues.append(ValidationIssue("warning", "Code", f"Callback not found in Python: {callback}"))

            # Check for unused callbacks
            defined_methods = re.findall(r"def (on_\w+)", py_content)
            for method in defined_methods:
                if method not in callbacks and method != "on_closing":
                    issues.append(ValidationIssue("info", "Code", f"Defined callback not used in UI: {method}"))

    except Exception as e:
        if "ParseError" in str(type(e).__name__):
            issues.append(ValidationIssue("error", "UI", f"XML parse error: {e}"))
        else:
            raise
    except Exception as e:
        issues.append(ValidationIssue("error", "Validation", f"Unexpected error: {e}"))

    return issues


def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-validate <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    issues = validate_project(project_name)

    if not issues:
        if RICH_AVAILABLE:
            console = Console()
            console.print(f"[green]OK Project '{project_name}' validation passed - no issues found[/green]")
        else:
            print(f"OK Project '{project_name}' validation passed - no issues found")
        sys.exit(0)

    # Group by severity
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    infos = [i for i in issues if i.severity == "info"]

    if RICH_AVAILABLE:
        console = Console()
        console.print(f"\n[bold]Validation Results for '{project_name}':[/bold]\n")

        if errors or warnings or infos:
            table = Table()
            table.add_column("Severity", style="bold")
            table.add_column("Category")
            table.add_column("Message")

            for issue in errors:
                table.add_row("[red]ERROR[/red]", issue.category, issue.message)
            for issue in warnings:
                table.add_row("[yellow]WARNING[/yellow]", issue.category, issue.message)
            for issue in infos:
                table.add_row("[blue]INFO[/blue]", issue.category, issue.message)

            console.print(table)

        console.print(f"\n[bold]Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info[/bold]")
    else:
        print(f"\nValidation Results for '{project_name}':\n")

        if errors:
            print("ERRORS:")
            for issue in errors:
                print(f"  ERROR {issue}")
            print()

        if warnings:
            print("WARNINGS:")
            for issue in warnings:
                print(f"  WARNING  {issue}")
            print()

        if infos:
            print("INFO:")
            for issue in infos:
                print(f"  ℹ️  {issue}")
            print()

        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
