"""Backup and rollback functionality"""
import shutil
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


def create_backup(project_path: Path) -> Optional[Path]:
    """Create backup of project directory"""
    if not project_path.exists():
        return None
    
    backup_dir = project_path.parent / ".pygubuai_backups"
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_name = f"{project_path.name}_{timestamp}"
    backup_path = backup_dir / backup_name
    
    try:
        shutil.copytree(project_path, backup_path)
        logger.info(f"Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return None


def restore_backup(backup_path: Path, target_path: Path) -> bool:
    """Restore project from backup"""
    if not backup_path.exists():
        logger.error(f"Backup not found: {backup_path}")
        return False
    
    try:
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(backup_path, target_path)
        logger.info(f"Restored from: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False


def list_backups(project_name: str, backup_dir: Optional[Path] = None) -> list:
    """List available backups for project"""
    if backup_dir is None:
        backup_dir = Path.cwd() / ".pygubuai_backups"
    
    if not backup_dir.exists():
        return []
    
    backups = []
    for item in backup_dir.iterdir():
        if item.is_dir() and item.name.startswith(f"{project_name}_"):
            backups.append(item)
    
    return sorted(backups, key=lambda x: x.name, reverse=True)
