#!/usr/bin/env python3
"""Widget inspector for UI files"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Dict, List
from .registry import Registry
from .utils import validate_path

try:
    from rich.console import Console
    from rich.tree import Tree
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def inspect_widget(project_name: str, widget_id: str) -> Optional[Dict]:
    """Inspect specific widget"""
    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return None

    validated_path = validate_path(project_path, must_exist=True, must_be_dir=True)
    ui_file = validated_path / f"{project_name}.ui"
    if not ui_file.exists():
        return None

    tree = ET.parse(ui_file)
    root = tree.getroot()

    # Find widget
    widget = root.find(f".//object[@id='{widget_id}']")
    if widget is None:
        return None

    # Extract info
    info = {
        "id": widget_id,
        "class": widget.get("class"),
        "properties": {},
        "layout": {},
        "children": [],
        "parent": None
    }

    # Get properties
    for prop in widget.findall("property"):
        info["properties"][prop.get("name")] = prop.text

    # Get layout
    layout = widget.find("layout")
    if layout is not None:
        info["layout"]["manager"] = layout.get("manager")
        for prop in layout.findall("property"):
            info["layout"][prop.get("name")] = prop.text

    # Get children
    for child in widget.findall(".//object[@id]"):
        if child != widget:
            info["children"].append(child.get("id"))

    # Find parent
    for obj in root.findall(".//object[@id]"):
        if widget in obj.findall(".//object"):
            info["parent"] = obj.get("id")
            break

    return info

def show_tree(project_name: str) -> Optional[str]:
    """Show widget hierarchy tree"""
    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return None

    validated_path = validate_path(project_path, must_exist=True, must_be_dir=True)
    ui_file = validated_path / f"{project_name}.ui"
    if not ui_file.exists():
        return None

    tree = ET.parse(ui_file)
    root = tree.getroot()

    def build_tree(element, indent=0):
        lines = []
        for obj in element.findall("object[@id]"):
            widget_id = obj.get("id")
            widget_class = obj.get("class")
            prefix = "  " * indent + ("└─ " if indent > 0 else "")
            lines.append(f"{prefix}{widget_id} ({widget_class})")
            lines.extend(build_tree(obj, indent + 1))
        return lines

    return "\\n".join(build_tree(root))

def list_callbacks(project_name: str) -> List[Dict]:
    """List all callbacks in project"""
    registry = Registry()
    project_path = registry.get_project(project_name)

    if not project_path:
        return []

    validated_path = validate_path(project_path, must_exist=True, must_be_dir=True)
    ui_file = validated_path / f"{project_name}.ui"
    if not ui_file.exists():
        return []

    tree = ET.parse(ui_file)
    root = tree.getroot()

    callbacks = []
    for obj in root.findall(".//object[@id]"):
        widget_id = obj.get("id")
        for prop in obj.findall("property[@name='command']"):
            if prop.text:
                callbacks.append({
                    "widget": widget_id,
                    "callback": prop.text
                })

    return callbacks

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-inspect <project> [options]")
        print("\\nOptions:")
        print("  --widget <id>    Inspect specific widget")
        print("  --tree           Show widget hierarchy")
        print("  --callbacks      List all callbacks")
        sys.exit(1)

    project_name = sys.argv[1]

    if len(sys.argv) == 2 or "--tree" in sys.argv:
        tree_str = show_tree(project_name)
        if tree_str:
            if RICH_AVAILABLE:
                console = Console()
                console.print(f"\n[bold cyan]Widget Tree for '{project_name}':[/bold cyan]\n")
                console.print(tree_str)
            else:
                print(f"\nWidget Tree for '{project_name}':\n")
                print(tree_str)
        else:
            print(f"Error: Could not load project '{project_name}'")
            sys.exit(1)

    elif "--widget" in sys.argv:
        idx = sys.argv.index("--widget")
        if idx + 1 >= len(sys.argv):
            print("Error: --widget requires widget ID")
            sys.exit(1)

        widget_id = sys.argv[idx + 1]
        info = inspect_widget(project_name, widget_id)

        if not info:
            print(f"Error: Widget '{widget_id}' not found")
            sys.exit(1)

        print(f"\\nWidget: {info['id']}")
        print("=" * (8 + len(info['id'])))
        print(f"Class: {info['class']}")
        print(f"Parent: {info['parent'] or 'None'}")

        if info['properties']:
            print("\\nProperties:")
            for key, value in info['properties'].items():
                print(f"  {key}: {value}")

        if info['layout']:
            print("\\nLayout:")
            for key, value in info['layout'].items():
                print(f"  {key}: {value}")

        if info['children']:
            print(f"\\nChildren: {', '.join(info['children'])}")

    elif "--callbacks" in sys.argv:
        callbacks = list_callbacks(project_name)

        if not callbacks:
            print(f"No callbacks found in '{project_name}'")
        else:
            if RICH_AVAILABLE:
                console = Console()
                table = Table(title=f"Callbacks in '{project_name}'")
                table.add_column("Widget", style="cyan")
                table.add_column("Callback", style="green")

                for cb in callbacks:
                    table.add_row(cb['widget'], cb['callback'])

                console.print(table)
                console.print(f"\nTotal: {len(callbacks)} callbacks", style="bold green")
            else:
                print(f"\nCallbacks in '{project_name}':\n")
                for cb in callbacks:
                    print(f"  {cb['widget']:20} -> {cb['callback']}")
                print(f"\nTotal: {len(callbacks)} callbacks")

    else:
        print("Invalid option")
        sys.exit(1)

if __name__ == "__main__":
    main()
