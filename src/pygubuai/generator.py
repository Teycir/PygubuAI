"""Centralized code generation functions for PygubuAI."""

from typing import List, Tuple, Dict, Any, Optional


def generate_base_ui_xml_structure(project_name: str, widgets_data: List[Tuple[str, Dict[str, Any]]]) -> str:
    """Generate base UI XML structure with widgets."""
    from .widgets import generate_widget_xml
    from .utils import safe_xml_text

    xml_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        '<interface version="1.2">',
        '  <object class="tk.Toplevel" id="mainwindow">',
        f'    <property name="title">{safe_xml_text(project_name.replace("_", " ").title())}</property>',
        '    <property name="height">400</property>',
        '    <property name="width">600</property>',
        "    <child>",
        '      <object class="ttk.Frame" id="mainframe">',
        '        <property name="padding">20</property>',
        '        <layout manager="pack">',
        '          <property name="expand">true</property>',
        '          <property name="fill">both</property>',
        "        </layout>",
    ]

    for i, (widget_type, config) in enumerate(widgets_data, 1):
        widget_id = config.get("id", f"{widget_type}{i}")
        xml_parts.extend(generate_widget_xml(widget_type, widget_id, config, i))

    xml_parts.extend(["      </object>", "    </child>", "  </object>", "</interface>"])
    return "\n".join(xml_parts)


def generate_python_app_structure(project_name: str, callbacks: List[str], custom_callbacks_code: str = "") -> str:
    """Generate Python application structure."""
    class_name = project_name.replace("_", " ").title().replace(" ", "")

    code = f"""#!/usr/bin/env python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "{project_name}.ui"


class {class_name}App:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow', master)
        self.builder.connect_callbacks(self)
"""

    for callback in callbacks:
        code += f"""
    def {callback}(self):
        print("{callback} triggered")
"""

    if custom_callbacks_code:
        code += f"\n{custom_callbacks_code}\n"

    code += f"""
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = {class_name}App()
    app.run()
"""
    return code


def generate_readme_content(project_name: str, description: str, ui_file_name: str, template_name: Optional[str] = None) -> str:
    """Generate README.md content."""
    from .utils import find_pygubu_designer
    import html

    title = html.escape(project_name.replace("_", " ").title())
    template_info = f"\nTemplate: {html.escape(template_name)}" if template_name else ""
    description_safe = html.escape(description)

    return f"""# {title}
{template_info}
{description_safe}

## Run
```bash
python {project_name}.py
```

## Edit UI
```bash
{find_pygubu_designer()} {ui_file_name}
```
"""
