"""Template CLI"""
import sys
import logging
from pathlib import Path

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory, find_pygubu_designer
from .templates import get_template, list_templates, generate_from_template, generate_callbacks

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_from_template(name: str, template_name: str):
    """Create project from template"""
    try:
        validate_pygubu()
        
        template = get_template(template_name)
        if not template:
            raise PygubuAIError(
                f"Template '{template_name}' not found",
                "Use 'pygubu-template list' to see available templates"
            )
        
        name = validate_project_name(name)
        base = ensure_directory(Path.cwd() / name)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_from_template(template_name))
        
        class_name = name.replace('_', ' ').title().replace(' ', '')
        callbacks = generate_callbacks(template_name)
        
        py_content = f'''#!/usr/bin/env python3
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

{callbacks}
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = {class_name}App()
    app.run()
'''
        
        py_file = base / f"{name}.py"
        py_file.write_text(py_content)
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(f'''# {name.replace("_", " ").title()}

Template: {template_name}
{template["description"]}

## Run
```bash
python {name}.py
```

## Edit UI
```bash
{find_pygubu_designer()} {name}.ui
```
''')
        
        logger.info(f"✓ Created from '{template_name}' template: {base}/")
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
    if args is None:
        args = sys.argv[1:]
    
    if '--version' in args:
        print(f"pygubu-template {__version__}")
        return
    
    if len(args) == 1 and args[0] == 'list':
        print("Available templates:\n")
        for name, desc in list_templates():
            print(f"  {name:12} - {desc}")
        return
    
    if len(args) != 2 or '--help' in args:
        print(f"pygubu-template {__version__}")
        print("\nUsage: pygubu-template <name> <template>")
        print("       pygubu-template list")
        print("\nExamples:")
        print("  pygubu-template mylogin login")
        print("  pygubu-template myapp crud")
        sys.exit(0 if '--help' in args else 1)
    
    create_from_template(args[0], args[1])

if __name__ == '__main__':
    main()
