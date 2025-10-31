#!/usr/bin/env python3
"""Database management CLI"""
import sys
import json
from .utils import validate_path

try:
    from rich.console import Console
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def init_database():
    """Initialize database"""
    from .db import init_db, get_db_path, SQLALCHEMY_AVAILABLE

    if not SQLALCHEMY_AVAILABLE:
        print("Error: SQLAlchemy not installed")
        print('Install with: pip install -e ".[db]"')
        return False

    db_path = get_db_path()

    if db_path.exists():
        print(f"Database already exists at {db_path}")
        response = input("Reinitialize? (y/N): ")
        if response.lower() != "y":
            return False
        db_path.unlink()

    if init_db():
        print(f"OK Database initialized at {db_path}")
        return True
    return False


def migrate_from_json():
    """Migrate data from JSON to database"""
    from .db import init_db, get_session, SQLALCHEMY_AVAILABLE
    from .db.operations import create_project, add_workflow_event
    from .registry import Registry

    if not SQLALCHEMY_AVAILABLE:
        print("Error: SQLAlchemy not installed")
        return False

    init_db()
    session = get_session()
    if not session:
        return False

    try:
        registry = Registry()
        projects = registry.list_projects_with_metadata()

        print(f"Migrating {len(projects)} projects...")

        for name, metadata in projects.items():
            path = metadata.get("path") if isinstance(metadata, dict) else metadata
            description = metadata.get("description", "") if isinstance(metadata, dict) else ""

            project = create_project(session, name, path, description)
            if project:
                print(f"  OK {name}")

                # Migrate workflow events
                project_path = validate_path(path, must_exist=True, must_be_dir=True)
                workflow_file = project_path / ".pygubu-workflow.json"
                if workflow_file.exists():
                    try:
                        with open(workflow_file) as f:
                            workflow_data = json.load(f)

                        history = workflow_data.get("history", workflow_data.get("changes", []))
                        for event in history[:100]:  # Limit to last 100
                            action = event.get("action", "file_changed")
                            desc = event.get("description", event.get("file", ""))
                            add_workflow_event(session, name, action, desc)
                    except Exception as e:
                        print(f"    Warning: Could not migrate workflow: {e}")

        print(f"\nOK Migration complete: {len(projects)} projects")
        return True

    except Exception as e:
        print(f"Error during migration: {e}")
        return False
    finally:
        session.close()


def show_stats():
    """Show database statistics"""
    from .db import get_session, SQLALCHEMY_AVAILABLE
    from .db.models import Project, Template, WorkflowEvent, Analytics

    if not SQLALCHEMY_AVAILABLE:
        print("Error: SQLAlchemy not installed")
        return

    session = get_session()
    if not session:
        print("Error: Database not initialized")
        return

    try:
        project_count = session.query(Project).count()
        template_count = session.query(Template).count()
        event_count = session.query(WorkflowEvent).count()
        analytics_count = session.query(Analytics).count()

        if RICH_AVAILABLE:
            console = Console()
            table = Table(title="Database Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Count", style="green")

            table.add_row("Projects", str(project_count))
            table.add_row("Templates", str(template_count))
            table.add_row("Workflow Events", str(event_count))
            table.add_row("Analytics Records", str(analytics_count))

            console.print(table)
        else:
            print("\nDatabase Statistics:")
            print(f"  Projects: {project_count}")
            print(f"  Templates: {template_count}")
            print(f"  Workflow Events: {event_count}")
            print(f"  Analytics Records: {analytics_count}")

    finally:
        session.close()


def backup_database(output_file: str):
    """Backup database"""
    import shutil
    from .db import get_db_path

    db_path = get_db_path()
    if not db_path.exists():
        print("Error: Database does not exist")
        return False

    output_path = validate_path(output_file)
    shutil.copy2(db_path, output_path)
    print(f"OK Database backed up to {output_path}")
    return True


def restore_database(backup_file: str):
    """Restore database from backup"""
    import shutil
    from .db import get_db_path

    backup_path = validate_path(backup_file, must_exist=True)
    if not backup_path.exists():
        print(f"Error: Backup file not found: {backup_file}")
        return False

    db_path = get_db_path()

    if db_path.exists():
        response = input(f"Overwrite existing database at {db_path}? (y/N): ")
        if response.lower() != "y":
            return False

    shutil.copy2(backup_path, db_path)
    print(f"OK Database restored from {backup_path}")
    return True


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: pygubu-db <command> [args]")
        print("\nCommands:")
        print("  init                  - Initialize database")
        print("  migrate               - Migrate from JSON to database")
        print("  stats                 - Show database statistics")
        print("  backup <file>         - Backup database")
        print("  restore <file>        - Restore database from backup")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_database()
    elif command == "migrate":
        migrate_from_json()
    elif command == "stats":
        show_stats()
    elif command == "backup":
        if len(sys.argv) < 3:
            print("Usage: pygubu-db backup <file>")
            sys.exit(1)
        backup_database(sys.argv[2])
    elif command == "restore":
        if len(sys.argv) < 3:
            print("Usage: pygubu-db restore <file>")
            sys.exit(1)
        restore_database(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


def add_table(project_name: str, table_name: str, schema: dict):
    """Add database table to project"""
    from .registry import Registry
    from .db import get_session, SQLALCHEMY_AVAILABLE
    from .db.operations import get_project

    if not SQLALCHEMY_AVAILABLE:
        print("Error: SQLAlchemy not installed")
        print('Install with: pip install -e ".[db]"')
        return False

    registry = Registry()
    project_path = registry.get_project(project_name)
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")

    session = get_session()
    if not session:
        return False

    try:
        project = get_project(session, project_name)
        if not project:
            print(f"Project '{project_name}' not found in database")
            return False

        # Add table creation logic here
        # This is a placeholder for the actual table creation functionality
        print(f"Table '{table_name}' would be added with schema: {schema}")
        print("Note: add_table functionality is not fully implemented yet")

        # Generate code for the project
        _generate_table_code(project_path, project_name, table_name, schema)

        return True

    finally:
        session.close()


def _generate_table_code(project_path: str, project_name: str, table_name: str, schema: dict):
    """Generate table-related code for project"""

    from pathlib import Path

    py_file = Path(project_path) / f"{project_name}.py"
    if not py_file.exists():
        return

    code = py_file.read_text()

    # Generate load method
    load_method = f"""
    def load_{table_name}(self):
        \"\"\"Load {table_name} from database\"\"\"
        # TODO: Implement database loading
        return []
"""

    # Generate add method
    fields = list(schema.keys())
    add_method = f"""
    def add_{table_name}(self, {', '.join(fields)}):
        \"\"\"Add new {table_name} to database\"\"\"
        # TODO: Implement database insertion
        pass
"""

    # Insert methods before run() method
    if "def run(self):" in code:
        code = code.replace("def run(self):", f"{load_method}{add_method}\n    def run(self):")
        py_file.write_text(code)


if __name__ == "__main__":
    main()
