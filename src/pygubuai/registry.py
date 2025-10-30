"""Thread-safe project registry"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List
from contextlib import contextmanager
from datetime import datetime, timezone

try:
    from filelock import FileLock
except ImportError:
    FileLock = None

from .config import Config

logger = logging.getLogger(__name__)

class Registry:
    """Thread-safe registry with file locking"""
    REGISTRY_FILE = None  # For testing override
    
    def __init__(self):
        if self.REGISTRY_FILE:
            self.registry_path = self.REGISTRY_FILE
        else:
            self.config = Config()
            self.registry_path = self.config.registry_path
        self._ensure_registry()
    
    def _ensure_registry(self):
        """Initialize registry if missing"""
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            self._write({"projects": {}, "active_project": None})
    
    @contextmanager
    def _lock(self, mode='r'):
        """Cross-platform file locking context manager"""
        if FileLock:
            lock = FileLock(str(self.registry_path) + '.lock', timeout=10)
            with lock:
                with open(self.registry_path, mode) as f:
                    yield f
        else:
            # Fallback without locking if filelock not available
            logger.warning("filelock not installed, registry operations not thread-safe")
            with open(self.registry_path, mode) as f:
                yield f
    
    def _read(self) -> Dict:
        """Read with lock"""
        try:
            with self._lock('r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Registry read error: {e}, reinitializing")
            return {"projects": {}, "active_project": None}
    
    def _write(self, data: Dict):
        """Write with lock"""
        with self._lock('w') as f:
            json.dump(data, f, indent=2)
    
    def add_project(self, name: str, path: str, description: str = "", tags: List[str] = None):
        """Add project with metadata"""
        data = self._read()
        data["projects"][name] = {
            "path": str(Path(path).resolve()),
            "created": datetime.now(timezone.utc).isoformat(),
            "modified": datetime.now(timezone.utc).isoformat(),
            "description": description,
            "tags": tags or []
        }
        self._write(data)
    
    def get_project(self, name: str) -> Optional[str]:
        """Get project path (backward compatible)"""
        data = self._read()
        project = data["projects"].get(name)
        if isinstance(project, dict):
            return project["path"]
        return project
    
    def get_project_metadata(self, name: str) -> Optional[Dict]:
        """Get full project metadata"""
        data = self._read()
        project = data["projects"].get(name)
        if isinstance(project, dict):
            return project
        elif project:  # Old format (string path)
            return {"path": project, "created": None, "modified": None, "description": "", "tags": []}
        return None
    
    def list_projects(self) -> Dict[str, str]:
        """List all projects (backward compatible - returns name: path)"""
        data = self._read()
        result = {}
        for name, project in data["projects"].items():
            if isinstance(project, dict):
                result[name] = project["path"]
            else:
                result[name] = project
        return result
    
    def list_projects_with_metadata(self) -> Dict[str, Dict]:
        """List all projects with full metadata"""
        data = self._read()
        result = {}
        for name, project in data["projects"].items():
            if isinstance(project, dict):
                result[name] = project
            else:  # Old format
                result[name] = {"path": project, "created": None, "modified": None, "description": "", "tags": []}
        return result
    
    def set_active(self, name: str):
        """Set active project"""
        data = self._read()
        if name not in data["projects"]:
            raise ValueError(f"Project '{name}' not found")
        data["active_project"] = name
        self._write(data)
    
    def get_active(self) -> Optional[str]:
        """Get active project"""
        return self._read().get("active_project")
    
    def search_projects(self, query: str) -> Dict[str, Dict]:
        """Search projects by name, description, or tags"""
        query_lower = query.lower()
        projects = self.list_projects_with_metadata()
        results = {}
        
        for name, metadata in projects.items():
            if query_lower in name.lower():
                results[name] = metadata
            elif query_lower in metadata.get("description", "").lower():
                results[name] = metadata
            elif any(query_lower in tag.lower() for tag in metadata.get("tags", [])):
                results[name] = metadata
        
        return results
    
    def update_project_metadata(self, name: str, description: str = None, tags: List[str] = None):
        """Update project metadata"""
        data = self._read()
        if name not in data["projects"]:
            raise ValueError(f"Project '{name}' not found")
        
        project = data["projects"][name]
        if isinstance(project, str):  # Convert old format
            project = {"path": project, "created": None, "description": "", "tags": []}
        
        project["modified"] = datetime.now(timezone.utc).isoformat()
        if description is not None:
            project["description"] = description
        if tags is not None:
            project["tags"] = tags
        
        data["projects"][name] = project
        self._write(data)
