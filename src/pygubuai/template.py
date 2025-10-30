"""Template CLI"""
import sys
import logging
import argparse
from pathlib import Path

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory
from .templates import get_template, list_templates, get_template_widgets_and_callbacks
from .generator import generate_base_ui_xml_structure, generate_python_app_structure, generate_readme_content

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
        
        template_widgets, template_callbacks_code = get_template_widgets_and_callbacks(template_name)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_base_ui_xml_structure(name, template_widgets))
        
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python_app_structure(name, [], custom_callbacks_code=template_callbacks_code))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(generate_readme_content(name, template["description"], f"{name}.ui", template_name=template_name))
        
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
    parser = argparse.ArgumentParser(
        description="Create a new pygubu project from a template.",
        epilog="Examples:\n"
               "  pygubu-template mylogin login\n"
               "  pygubu-template myapp crud\n"
               "  pygubu-template list",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', action='version', version=f"pygubu-template {__version__}"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    subparsers.add_parser('list', help='List all available templates')
    
    create_parser = subparsers.add_parser('create', help='Create project from template')
    create_parser.add_argument('name', help='Name of the project to create')
    create_parser.add_argument('template', help='Template to use (e.g., login, crud, settings)')
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command == 'list':
        print("Available templates:\n")
        for name, desc in list_templates():
            print(f"  {name:12} - {desc}")
    elif parsed_args.command == 'create':
        create_from_template(parsed_args.name, parsed_args.template)
    elif hasattr(parsed_args, 'name') and hasattr(parsed_args, 'template'):
        # Backward compatibility: pygubu-template <name> <template>
        create_from_template(parsed_args.name, parsed_args.template)
    else:
        # If no subcommand and we have 2 positional args, treat as create
        if args and len(args) == 2 and args[0] != 'list':
            create_from_template(args[0], args[1])
        else:
            parser.print_help()

if __name__ == '__main__':
    main()
