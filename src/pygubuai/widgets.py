"""Widget detection, generation, and library browser"""

from typing import List, Dict, Optional
from .widget_data import WIDGET_LIBRARY, CATEGORIES

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

WIDGET_PATTERNS = {
    "label": {"keywords": ["label", "title", "heading"], "class": "ttk.Label", "properties": {"text": "Label"}},
    "entry": {"keywords": ["entry", "input", "field"], "class": "ttk.Entry", "properties": {}},
    "button": {
        "keywords": ["button", "submit", "click"],
        "class": "ttk.Button",
        "properties": {"text": "Button", "command": "on_button_click"},
    },
    "treeview": {"keywords": ["list", "table", "tree"], "class": "ttk.Treeview", "properties": {}, "expand": True},
    "text": {
        "keywords": ["text area", "textarea", "multiline"],
        "class": "tk.Text",
        "properties": {"height": "10"},
        "expand": True,
    },
    "combobox": {"keywords": ["dropdown", "select", "combo"], "class": "ttk.Combobox", "properties": {}},
    "checkbutton": {"keywords": ["checkbox", "check"], "class": "ttk.Checkbutton", "properties": {"text": "Option"}},
}

CONTEXT_PATTERNS = {
    "form": ["label", "entry", "entry", "button"],
    "login": ["label", "entry", "label", "entry", "button"],
    "search": ["entry", "button", "treeview"],
}


def detect_widgets(description):
    """Detect widgets from description"""
    desc_lower = description.lower()

    for context, widget_list in CONTEXT_PATTERNS.items():
        if context in desc_lower:
            return [(w, WIDGET_PATTERNS[w]) for w in widget_list if w in WIDGET_PATTERNS]

    widgets = []
    for widget_type, config in WIDGET_PATTERNS.items():
        if any(kw in desc_lower for kw in config["keywords"]):
            widgets.append((widget_type, config))

    return widgets if widgets else [("label", WIDGET_PATTERNS["label"]), ("button", WIDGET_PATTERNS["button"])]


def generate_widget_xml(widget_type: str, widget_id: str, config: dict, index: int = 1) -> List[str]:
    """Generate XML for widget"""
    xml = ["        <child>", f'          <object class="{config.get("class", "ttk.Label")}" id="{widget_id}">']

    for prop, value in config.get("properties", {}).items():
        xml.append(f'            <property name="{prop}">{value}</property>')

    layout = '            <layout manager="pack">'
    if config.get("expand"):
        xml.extend(
            [
                layout,
                '              <property name="expand">true</property>',
                '              <property name="fill">both</property>',
                "            </layout>",
            ]
        )
    else:
        xml.append(layout + '<property name="pady">5</property></layout>')

    xml.extend(["          </object>", "        </child>"])
    return xml


def get_callbacks(widgets):
    """Extract callbacks"""
    callbacks = set()
    for _, config in widgets:
        if "command" in config.get("properties", {}):
            callbacks.add(config["properties"]["command"])
    return list(callbacks)


def list_widgets(category: Optional[str] = None) -> Dict[str, Dict]:
    """List all widgets, optionally filtered by category"""
    if category:
        return {name: info for name, info in WIDGET_LIBRARY.items() if info["category"] == category}
    return WIDGET_LIBRARY


def search_widgets(query: str) -> Dict[str, Dict]:
    """Search widgets by name or description"""
    query_lower = query.lower()
    results = {}
    for name, info in WIDGET_LIBRARY.items():
        if query_lower in name.lower() or query_lower in info["description"].lower():
            results[name] = info
    return results


def get_widget_info(widget_name: str) -> Optional[Dict]:
    """Get detailed info about a specific widget"""
    return WIDGET_LIBRARY.get(widget_name)


def main():
    """CLI entry point for widget browser"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-widgets <command> [args]")
        print("Commands:")
        print("  list [--category <cat>]  - List all widgets")
        print("  search <query>           - Search widgets")
        print("  info <widget>            - Show widget details")
        print("  categories               - List all categories")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        category = None
        if len(sys.argv) > 2 and sys.argv[2] == "--category" and len(sys.argv) > 3:
            category = sys.argv[3]

        widgets = list_widgets(category)

        if RICH_AVAILABLE:
            console = Console()
            title = f"{CATEGORIES.get(category, category)} Widgets" if category else "All Available Widgets"
            table = Table(title=title)
            table.add_column("Widget", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")
            table.add_column("Category", style="magenta")

            for name, info in sorted(widgets.items()):
                table.add_row(name, info["description"], info["category"])

            console.print(table)
            console.print(f"\nTotal: {len(widgets)} widgets", style="bold green")
        else:
            if category:
                print(f"\n{CATEGORIES.get(category, category)} Widgets:\n")
            else:
                print("\nAll Available Widgets:\n")

            for name, info in sorted(widgets.items()):
                print(f"  {name:20} - {info['description']}")
            print(f"\nTotal: {len(widgets)} widgets")

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: pygubu-widgets search <query>")
            sys.exit(1)

        query = sys.argv[2]
        results = search_widgets(query)

        print(f"\nSearch results for '{query}':\n")
        for name, info in sorted(results.items()):
            print(f"  {name:20} - {info['description']}")
        print(f"\nFound: {len(results)} widgets")

    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: pygubu-widgets info <widget_name>")
            sys.exit(1)

        widget_name = sys.argv[2]
        info = get_widget_info(widget_name)

        if not info:
            print(f"Widget '{widget_name}' not found")
            sys.exit(1)

        if RICH_AVAILABLE:
            console = Console()
            panel_content = f"[cyan]Category:[/cyan] {info['category']}\n"
            panel_content += f"[cyan]Description:[/cyan] {info['description']}\n\n"
            panel_content += f"[cyan]Properties:[/cyan] {', '.join(info['properties'])}\n\n"
            panel_content += "[cyan]Common Use Cases:[/cyan]\n"
            for use_case in info["use_cases"]:
                panel_content += f"  • {use_case}\n"

            console.print(Panel(panel_content, title=f"[bold]{widget_name}[/bold]", border_style="blue"))
        else:
            print(f"\n{widget_name}")
            print("=" * len(widget_name))
            print(f"Category: {info['category']}")
            print(f"Description: {info['description']}")
            print(f"\nProperties: {', '.join(info['properties'])}")
            print(f"\nCommon Use Cases:")
            for use_case in info["use_cases"]:
                print(f"  • {use_case}")

    elif command == "categories":
        print("\nWidget Categories:\n")
        for cat, desc in CATEGORIES.items():
            count = len([w for w in WIDGET_LIBRARY.values() if w["category"] == cat])
            print(f"  {cat:12} - {desc} ({count} widgets)")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
