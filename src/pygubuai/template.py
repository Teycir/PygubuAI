"""Template CLI"""
import sys
import logging
from pathlib import Path

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory
from .templates import get_template, list_templates, get_template_widgets_and_callbacks
from .generator import generate_base_ui_xml_structure, generate_python_app_structure, generate_readme_content

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_from_template(name: str, template_name: str, skip_validation: bool = False):
    """Create project from template"""
    try:
        if not skip_validation:
            validate_pygubu()
        
        template = get_template(template_name)
        if not template:
            raise PygubuAIError(
                f"Template '{template_name}' not found",
                "Use 'pygubu-template list' to see available templates"
            )
        
        name = validate_project_name(name)
        base = ensure_directory(Path.cwd() / name)
        
        template_widgets, template_callbacks_code = get_template_widgets_and_callbacks(template_name)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_base_ui_xml_structure(name, template_widgets))
        
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python_app_structure(name, [], custom_callbacks_code=template_callbacks_code))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(generate_readme_content(name, template["description"], f"{name}.ui", template_name=template_name))
        
        logger.info(f"[SUCCESS] Created from '{template_name}' template: {base}/")
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
