#!/usr/bin/env python3
"""Project analysis for AI insights"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict
from collections import Counter


def analyze_project(project_name: str) -> Dict:
    """Analyze project structure and complexity"""
    from .registry import Registry

    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return {"error": f"Project '{project_name}' not found"}

    ui_file = Path(project_path) / f"{project_name}.ui"
    py_file = Path(project_path) / f"{project_name}.py"

    analysis = {
        "project": project_name,
        "complexity": 0.0,
        "widget_count": 0,
        "callback_count": 0,
        "layout_patterns": [],
        "widget_types": {},
        "suggestions": []
    }

    if ui_file.exists():
        _analyze_ui(ui_file, analysis)

    if py_file.exists():
        _analyze_code(py_file, analysis)

    _calculate_complexity(analysis)
    _generate_suggestions(analysis)

    return analysis


def _analyze_ui(ui_file: Path, analysis: Dict):
    """Analyze UI file"""
    try:
        tree = ET.parse(ui_file)
        root = tree.getroot()

        widgets = root.findall(".//object[@id]")
        analysis["widget_count"] = len(widgets)

        widget_types = Counter()
        layouts = set()
        callbacks = set()

        for obj in widgets:
            widget_class = obj.get("class", "")
            widget_types[widget_class] += 1

            layout = obj.find("layout")
            if layout is not None:
                layouts.add(layout.get("manager", ""))

            for prop in obj.findall("property[@name='command']"):
                if prop.text:
                    callbacks.add(prop.text)

        analysis["widget_types"] = dict(widget_types)
        analysis["layout_patterns"] = list(layouts)
        analysis["callback_count"] = len(callbacks)

    except Exception:
        pass


def _analyze_code(py_file: Path, analysis: Dict):
    """Analyze Python code"""
    try:
        content = py_file.read_text()
        analysis["code_lines"] = len(content.splitlines())
        analysis["has_docstrings"] = '"""' in content or "'''" in content
    except Exception:
        pass


def _calculate_complexity(analysis: Dict):
    """Calculate complexity score"""
    score = 0.0

    score += analysis["widget_count"] * 0.2
    score += analysis["callback_count"] * 0.5
    score += len(analysis["layout_patterns"]) * 1.0

    analysis["complexity"] = round(score, 1)


def _generate_suggestions(analysis: Dict):
    """Generate improvement suggestions"""
    suggestions = []

    if analysis["widget_count"] > 20:
        suggestions.append("Consider breaking into multiple windows")

    if "tk." in str(analysis.get("widget_types", {})):
        suggestions.append("Use ttk widgets for better theming")

    if analysis["callback_count"] == 0:
        suggestions.append("Add event handlers for interactivity")

    if not analysis.get("has_docstrings"):
        suggestions.append("Add docstrings for better documentation")

    analysis["suggestions"] = suggestions


def main():
    """CLI entry point"""
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: pygubu-ai-analyze <project>")
        sys.exit(1)

    project_name = sys.argv[1]
    analysis = analyze_project(project_name)

    if "error" in analysis:
        print(f"Error: {analysis['error']}")
        sys.exit(1)

    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
