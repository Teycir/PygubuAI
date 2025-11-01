"""Data export functionality for PygubuAI projects"""

from pathlib import Path
from typing import List, Union, Optional
from defusedxml import ElementTree as ET
from .registry import Registry
from .utils import validate_path


def add_export_capability(project_name: str, formats: List[str], widget_id: Union[str, None] = None) -> bool:
    """Add export capability to project"""
    registry = Registry()
    project_path = registry.get_project(project_name)
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")

    validated_path = validate_path(project_path, must_exist=True, must_be_dir=True)

    # Add export button to UI
    _add_export_button(str(validated_path), project_name, formats)

    # Generate export code
    _generate_export_code(str(validated_path), project_name, formats, widget_id)

    return True


def _add_export_button(project_path: str, project_name: str, formats: List[str]) -> None:
    """Add export button to UI file"""
    ui_file = Path(project_path) / f"{project_name}.ui"
    if not ui_file.exists():
        return

    tree = ET.parse(ui_file)
    root = tree.getroot()

    # Find main frame
    frame = root.find(".//object[@id='mainframe']")
    if frame is None:
        return

    # Add export button
    button = ET.SubElement(frame, "object", {"class": "ttk.Button", "id": "export_button"})
    text_prop = ET.SubElement(button, "property", {"name": "text"})
    text_prop.text = "Export"
    cmd_prop = ET.SubElement(button, "property", {"name": "command"})
    cmd_prop.text = "on_export"

    # Layout
    layout = ET.SubElement(button, "layout", {"manager": "pack"})
    side_prop = ET.SubElement(layout, "property", {"name": "side"})
    side_prop.text = "bottom"

    tree.write(ui_file, encoding="utf-8", xml_declaration=True)


def _generate_export_code(project_path: str, project_name: str, formats: List[str], widget_id: Optional[str]) -> None:
    """Generate export callback code"""
    py_file = Path(project_path) / f"{project_name}.py"
    if not py_file.exists():
        return

    code = py_file.read_text()

    # Generate export method
    export_method = _create_export_method(formats, widget_id)

    # Insert before run() method
    if "def run(self):" in code:
        code = code.replace("def run(self):", f"{export_method}\n\n    def run(self):")
        py_file.write_text(code)


def _create_export_method(formats: List[str], widget_id: Union[str, None] = None) -> str:
    """Create export method code"""
    method = '''    def on_export(self):
        """Export data"""
        from tkinter import filedialog
        import csv
        import json

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:
            return

        # Get data from widget
        data = self._get_export_data()

        # Export based on format
        if filename.endswith('.csv'):
            self._export_csv(data, filename)
        elif filename.endswith('.json'):
            self._export_json(data, filename)

    def _get_export_data(self):
        """Get data to export"""
        # TODO: Implement based on widget type
        return []

    def _export_csv(self, data, filename):
        """Export to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def _export_json(self, data, filename):
        """Export to JSON"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)'''

    return method


def generate_treeview_export(widget_id: str) -> str:
    """Generate Treeview export code"""
    return f'''    def _get_export_data(self):
        """Get data from Treeview"""
        tree = self.builder.get_object('{widget_id}')
        data = []

        # Get columns
        columns = tree['columns']
        data.append(list(columns))

        # Get rows
        for item in tree.get_children():
            values = tree.item(item)['values']
            data.append(list(values))

        return data'''


def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: pygubu-export <command> <project> [options]")
        print("Commands:")
        print("  add <project> --format csv,json,pd")
        print("  add-button <project>")
        sys.exit(1)

    command = sys.argv[1]
    project = sys.argv[2]

    if command == "add":
        formats = ["csv", "json"]
        if "--format" in sys.argv:
            idx = sys.argv.index("--format")
            if idx + 1 < len(sys.argv):
                formats = sys.argv[idx + 1].split(",")

        try:
            add_export_capability(project, formats)
            print(f"OK Added export capability to '{project}'")
            print(f"  Formats: {', '.join(formats)}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "add-button":
        try:
            _add_export_button(project, project, ["csv"])
            print(f"OK Added export button to '{project}'")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
