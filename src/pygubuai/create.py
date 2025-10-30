"""Project creation with error handling"""
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

from . import __version__
from .errors import PygubuAIError, validate_pygubu
from .utils import validate_project_name, ensure_directory
from .widgets import detect_widgets, get_callbacks
from .generator import generate_base_ui_xml_structure, generate_python_app_structure, generate_readme_content
from .git_integration import init_git_repo
from .interactive import interactive_create
from .registry import Registry

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_project(name: str, description: str, skip_validation: bool = False, 
                  dry_run: bool = False, init_git: bool = False, 
                  template: Optional[str] = None, tags: list = None) -> None:
    """Create project with error handling"""
    try:
        if not skip_validation:
            validate_pygubu()
        name = validate_project_name(name)
        base = Path.cwd() / name
        
        if dry_run:
            logger.info("[DRY RUN] Would create:")
            logger.info(f"  Directory: {base}/")
            logger.info(f"  Files: {name}.ui, {name}.py, README.md")
            if init_git:
                logger.info(f"  Git: Initialize repository with .gitignore")
            if template:
                logger.info(f"  Template: {template}")
            logger.info(f"\nDescription: {description}")
            return
        
        base = ensure_directory(base)
        
        # Use template if specified
        if template:
            from .template import create_from_template
            # Template function creates files, just return after
            return
        
        widgets = detect_widgets(description)
        callbacks = get_callbacks(widgets)
        
        ui_file = base / f"{name}.ui"
        ui_file.write_text(generate_base_ui_xml_structure(name, widgets))
        
        py_file = base / f"{name}.py"
        py_file.write_text(generate_python_app_structure(name, callbacks))
        py_file.chmod(0o755)
        
        readme = base / "README.md"
        readme.write_text(generate_readme_content(name, description, f"{name}.ui"))
        
        # Initialize git if requested
        if init_git:
            if init_git_repo(base):
                logger.info("  Git: Initialized repository")
        
        # Register project
        registry = Registry()
        registry.add_project(name, str(base), description=description, tags=tags or [])
        
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
               "  pygubu-create todo 'todo app with entry, button, and list'\n"
               "  pygubu-create --interactive\n"
               "  pygubu-create myapp 'app' --dry-run --git",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--version', action='version', version=f"pygubu-create {__version__}"
    )
    parser.add_argument('name', nargs='?', help='Name of the project to create.')
    parser.add_argument('description', nargs='?', help='Natural language description of the UI.')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode with prompts')
    parser.add_argument('--dry-run', action='store_true', help='Preview without creating files')
    parser.add_argument('--git', action='store_true', help='Initialize git repository')
    parser.add_argument('--template', '-t', help='Use template (login, crud, settings, etc.)')
    parser.add_argument('--tags', help='Comma-separated tags for project')
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.interactive:
        config = interactive_create()
        create_project(
            config['name'], 
            config['description'], 
            dry_run=parsed_args.dry_run,
            init_git=config['git'],
            template=config['template']
        )
    else:
        if not parsed_args.name or not parsed_args.description:
            parser.error("name and description are required (or use --interactive)")
        
        tags = [t.strip() for t in parsed_args.tags.split(',')] if parsed_args.tags else None
        create_project(
            parsed_args.name, 
            parsed_args.description,
            dry_run=parsed_args.dry_run,
            init_git=parsed_args.git,
            template=parsed_args.template,
            tags=tags
        )

if __name__ == '__main__':
    main()
