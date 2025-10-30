"""Project creation with error handling"""
import sys
import logging
import argparse
from pathlib import Path

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory
from .widgets import detect_widgets, get_callbacks
from .generator import generate_base_ui_xml_structure, generate_python_app_structure, generate_readme_content

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_project(name: str, description: str, skip_validation: bool = False) -> None:
    """Create project with error handling"""
    try:
        if not skip_validation:
            validate_pygubu()
        name = validate_project_name(name)
        base = ensure_directory(Path.cwd() / name)
        
        widgets = detect_widgets(description)
        callbacks = get_callbacks(widgets)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_base_ui_xml_structure(name, widgets))
        
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python_app_structure(name, callbacks))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(generate_readme_content(name, description, f"{name}.ui"))
        
        logger.info(f"[SUCCESS] Created project: {base}/")
        logger.info(f"  Files: {name}.ui, {name}.py, README.md")
        logger.info(f"\nNext: cd {name} && python {name}.py")
        
    except PygubuAIError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
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
