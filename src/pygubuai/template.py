"""Template CLI"""
import sys
import logging
import argparse
from pathlib import Path

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory
from .template_data import get_template, list_templates, get_template_widgets_and_callbacks
from .generator import generate_base_ui_xml_structure, generate_python_app_structure, generate_readme_content

logger = logging.getLogger(__name__)

def create_from_template(name: str, template_name: str, skip_validation: bool = False,
                        dry_run: bool = False, init_git: bool = False):
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
        base = Path.cwd() / name
        
        if dry_run:
            logger.info("[DRY RUN] Would create from template:")
            logger.info(f"  Template: {template_name}")
            logger.info(f"  Directory: {base}/")
            logger.info(f"  Files: {name}.ui, {name}.py, README.md")
            if init_git:
                logger.info(f"  Git: Initialize repository with .gitignore")
            return
        
        base = ensure_directory(base)
        
        template_widgets, template_callbacks_code = get_template_widgets_and_callbacks(template_name)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_base_ui_xml_structure(name, template_widgets))
        
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python_app_structure(name, [], custom_callbacks_code=template_callbacks_code))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(generate_readme_content(name, template["description"], f"{name}.ui", template_name=template_name))
        
        # Initialize git if requested
        if init_git:
            from .git_integration import init_git_repo
            if init_git_repo(base):
                logger.info("  Git: Initialized repository")
        
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
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = argparse.ArgumentParser(
        prog='pygubu-template',
        description='Create pygubu projects from templates'
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(dest='command')
    
    list_parser = subparsers.add_parser('list', help='List available templates')
    
    create_parser = subparsers.add_parser('create', help='Create project from template')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('template', help='Template name')
    
    # Support legacy positional args: pygubu-template <name> <template>
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command == 'list':
        print("Available templates:\n")
        for name, desc in list_templates():
            print(f"  {name:12} - {desc}")
    elif parsed_args.command == 'create':
        create_from_template(parsed_args.name, parsed_args.template)
    else:
        # Legacy mode: pygubu-template <name> <template>
        if args is None:
            args = sys.argv[1:]
        if len(args) == 1 and args[0] == 'list':
            print("Available templates:\n")
            for name, desc in list_templates():
                print(f"  {name:12} - {desc}")
        elif len(args) == 2:
            create_from_template(args[0], args[1])
        else:
            parser.print_help()
            sys.exit(1)

if __name__ == '__main__':
    main()
