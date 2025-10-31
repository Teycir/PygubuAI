#!/usr/bin/env python3
"""AI context generation for enhanced Amazon Q integration"""
import json
from pathlib import Path
from typing import Dict
from datetime import datetime, timezone



def generate_context(project_name: str) -> Dict:
    """Generate rich AI context for project"""
    from .registry import Registry
    from .db import get_session, SQLALCHEMY_AVAILABLE

    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return {"error": f"Project '{project_name}' not found"}

    context = {
        "project": project_name,
        "path": project_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "widgets": [],
        "callbacks": [],
        "history": [],
        "metrics": {}
    }

    # Get widget info from UI file
    ui_file = Path(project_path) / f"{project_name}.ui"
    if ui_file.exists():
        widgets, callbacks = _parse_ui_file(ui_file)
        context["widgets"] = widgets
        context["callbacks"] = callbacks
        context["metrics"]["widget_count"] = len(widgets)
        context["metrics"]["callback_count"] = len(callbacks)

    # Get history from database if available
    if SQLALCHEMY_AVAILABLE:
        session = get_session()
        if session:
            try:
                from .db.operations import get_workflow_events
                events = get_workflow_events(session, project_name, limit=10)
                context["history"] = [
                    {
                        "action": e.action,
                        "description": e.description,
                        "timestamp": e.timestamp.isoformat()
                    }
                    for e in events
                ]
            finally:
                session.close()

    return context



def _parse_ui_file(ui_file: Path) -> tuple:
    """Parse UI file for widgets and callbacks"""
    import xml.etree.ElementTree as ET

    try:
        tree = ET.parse(ui_file)
        root = tree.getroot()

        widgets = []
        callbacks = set()

        for obj in root.findall(".//object[@id]"):
            widget_id = obj.get("id")
            widget_class = obj.get("class")
            widgets.append({"id": widget_id, "class": widget_class})

            for prop in obj.findall("property[@name='command']"):
                if prop.text:
                    callbacks.add(prop.text)

        return widgets, list(callbacks)
    except Exception:
        return [], []



def format_for_ai(context: Dict) -> str:
    """Format context for AI consumption"""
    lines = [
        f"# Project: {context['project']}",
        f"Path: {context['path']}",
        "",
        f"## Widgets ({context['metrics'].get('widget_count', 0)})",
    ]

    for widget in context.get("widgets", [])[:10]:
        lines.append(f"- {widget['id']}: {widget['class']}")

    if context.get("callbacks"):
        lines.append(f"\n## Callbacks ({len(context['callbacks'])})")
        for cb in context["callbacks"]:
            lines.append(f"- {cb}")

    if context.get("history"):
        lines.append("\n## Recent History")
        for event in context["history"][:5]:
            lines.append(f"- {event['action']}: {event['description']}")

    return "\n".join(lines)



def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-ai-context <project>")
        sys.exit(1)

    project_name = sys.argv[1]
    context = generate_context(project_name)

    if "error" in context:
        print(f"Error: {context['error']}")
        sys.exit(1)

    # Output formatted context
    print(format_for_ai(context))

    # Also save JSON for programmatic use
    output_file = Path.home() / ".amazonq" / "prompts" / f"{project_name}-context.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(context, f, indent=2)

    print(f"\nContext saved to: {output_file}")


if __name__ == "__main__":
    main()
