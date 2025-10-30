"""Project creation with error handling"""
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Tuple

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory, find_pygubu_designer
from .widgets import detect_widgets, generate_widget_xml, get_callbacks

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def generate_ui(name: str, description: str) -> str:
    """Generate UI XML"""
    widgets = detect_widgets(description)
    
    xml = [
        "<?xml version='1.0' encoding='utf-8'?>",
        '<interface version="1.2">',
        '  <object class="tk.Toplevel" id="mainwindow">',
        f'    <property name="title">{name.replace("_", " ").title()}</property>',
        '    <property name="height">400</property>',
        '    <property name="width">600</property>',
        '    <child>',
        '      <object class="ttk.Frame" id="mainframe">',
        '        <property name="padding">20</property>',
        '        <layout manager="pack">',
        '          <property name="expand">true</property>',
        '          <property name="fill">both</property>',
        '        </layout>',
    ]
    
    for i, (widget_type, config) in enumerate(widgets, 1):
        xml.extend(generate_widget_xml(widget_type, f"{widget_type}{i}", config, i))
    
    xml.extend(['      </object>', '    </child>', '  </object>', '</interface>'])
    return '\n'.join(xml)

def generate_python(name: str, widgets: List[Tuple]) -> str:
    """Generate Python code"""
    class_name = name.replace('_', ' ').title().replace(' ', '')
    callbacks = get_callbacks(widgets)
    
    code = f'''#!/usr/bin/env python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "{name}.ui"

class {class_name}App:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow', master)
        self.builder.connect_callbacks(self)
'''
    
    for callback in callbacks:
        code += f'''
    def {callback}(self):
        print("{callback} triggered")
'''
    
    code += f'''
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = {class_name}App()
    app.run()
'''
    return code

def create_project(name: str, description: str) -> None:
    """Create project with error handling"""
    try:
        validate_pygubu()
        name = validate_project_name(name)
        
        base = ensure_directory(Path.cwd() / name)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_ui(name, description))
        
        widgets = detect_widgets(description)
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python(name, widgets))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(f'''# {name.replace("_", " ").title()}

{description}

## Run
```bash
python {name}.py
```

## Edit UI
```bash
{find_pygubu_designer()} {name}.ui
```
''')
        
        logger.info(f"✓ Created project: {base}/")
        logger.info(f"  Files: {name}.ui, {name}.py, README.md")
        logger.info(f"\n🚀 Next: cd {name} && python {name}.py")
        
    except PygubuAIError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

def main(args=None):
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Create a new pygubu project from a natural language description.",
        epilog="Examples:\n"
               "  pygubu-create login 'login form with username and password'\n"
               "  pygubu-create todo 'todo app with entry, button, and list'",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', action='version', version=f"pygubu-create {__version__}"
    )
    parser.add_argument('name', help='Name of the project to create.')
    parser.add_argument('description', help='Natural language description of the UI.')
    
    parsed_args = parser.parse_args(args)
    create_project(parsed_args.name, parsed_args.description)

if __name__ == '__main__':
    main()
