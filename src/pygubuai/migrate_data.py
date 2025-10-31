#!/usr/bin/env python3
"""Data migration script for Pydantic models"""
import json
import logging
from pathlib import Path
from typing import Dict
from .config import Config
from .registry import Registry

logger = logging.getLogger(__name__)


def migrate_registry() -> bool:
    """Migrate registry to new format"""
    try:
        from pydantic import ValidationError
        from .models import RegistryData
    except ImportError:
        logger.error("Pydantic not installed, cannot migrate")
        return False

    config = Config()
    registry_path = config.registry_path

    if not registry_path.exists():
        logger.info("No registry to migrate")
        return True

    # Backup
    backup_path = registry_path.with_suffix('.json.bak')
    registry_path.rename(backup_path)
    logger.info(f"Backed up registry to {backup_path}")

    try:
        with open(backup_path) as f:
            data = json.load(f)

        # Convert old format
        if 'active_project' in data:
            data['active'] = data.pop('active_project')

        # Validate
        registry_model = RegistryData(**data)

        # Write new format
        with open(registry_path, 'w') as f:
            json.dump(registry_model.model_dump(), f, indent=2)

        logger.info("Registry migrated successfully")
        return True

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        # Restore backup
        backup_path.rename(registry_path)
        logger.info("Restored from backup")
        return False


def migrate_workflow(project_path: Path) -> bool:
    """Migrate workflow file to new format"""
    try:
        from pydantic import ValidationError
        from .models import WorkflowData, WorkflowHistory
    except ImportError:
        logger.error("Pydantic not installed, cannot migrate")
        return False

    workflow_file = project_path / ".pygubu-workflow.json"

    if not workflow_file.exists():
        logger.info(f"No workflow file in {project_path}")
        return True

    # Backup
    backup_file = workflow_file.with_suffix('.json.bak')
    workflow_file.rename(backup_file)
    logger.info(f"Backed up workflow to {backup_file}")

    try:
        with open(backup_file) as f:
            data = json.load(f)

        # Convert old format
        if 'changes' in data:
            data['history'] = [
                WorkflowHistory(
                    timestamp=c.get('timestamp', ''),
                    action='file_changed',
                    description=f"File {c.get('file', 'unknown')} changed"
                ).model_dump()
                for c in data.pop('changes', [])
            ]

        if 'project' not in data:
            data['project'] = project_path.name

        # Validate
        workflow_model = WorkflowData(**data)

        # Write new format
        with open(workflow_file, 'w') as f:
            json.dump(workflow_model.model_dump(), f, indent=2)

        logger.info(f"Workflow migrated for {project_path.name}")
        return True

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        # Restore backup
        backup_file.rename(workflow_file)
        logger.info("Restored from backup")
        return False


def migrate_all() -> None:
    """Migrate all data to new format"""
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    print("Starting data migration to Pydantic models...\n")

    # Migrate registry
    print("1. Migrating registry...")
    if migrate_registry():
        print("   OK Registry migrated\n")
    else:
        print("   FAILED Registry migration failed\n")
        return

    # Migrate workflows
    print("2. Migrating workflow files...")
    registry = Registry()
    projects = registry.list_projects()

    success = 0
    failed = 0

    for name, path in projects.items():
        project_path = Path(path)
        if migrate_workflow(project_path):
            success += 1
        else:
            failed += 1

    print(f"   OK {success} workflows migrated")
    if failed:
        print(f"   FAILED {failed} workflows failed")

    print("\nMigration complete!")


def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: python -m pygubuai.migrate_data")
        print("\nMigrates registry and workflow files to Pydantic format")
        print("Creates backups with .bak extension")
        sys.exit(0)

    migrate_all()

if __name__ == '__main__':
    main()
