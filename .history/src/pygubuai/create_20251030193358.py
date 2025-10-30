"""Project creation with error handling"""
import sys
import logging
from pathlib import Path
from typing import List, Tuple

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory
from .widgets import detect_widgets, get_callbacks
from .generator import generate_base_ui_xml_structure, generate_python_app_structure, generate_readme_content

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)



def create_project(name: str, description: str) -> None:
    """Create project with error handling"""
    try:
        validate_pygubu()
        name = validate_project_name(name)
        
        base = ensure_directory(Path.cwd() / name)
        widgets = detect_widgets(description)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_base_ui_xml_structure(name, widgets))
        
        callbacks = get_callbacks(widgets)
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python_app_structure(name, callbacks))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(generate_readme_content(name, description, f"{name}.ui"))
        
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
    if args is None:
        args = sys.argv[1:]
    
    if '--version' in args:
        print(f"pygubu-create {__version__}")
        return
    
    if len(args) != 2 or '--help' in args:
        print(f"pygubu-create {__version__}")
        print("\nUsage: pygubu-create <name> '<description>'")
        print("\nExamples:")
        print("  pygubu-create login 'login form with username and password'")
        print("  pygubu-create todo 'todo app with entry, button, and list'")
        sys.exit(0 if '--help' in args else 1)
    
    create_project(args[0], args[1])

if __name__ == '__main__':
    main()
