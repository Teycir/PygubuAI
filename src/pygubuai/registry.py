"""Thread-safe project registry"""
import json
import logging
import time
from pathlib import Path
from typing import Dict, Optional, List
from contextlib import contextmanager
from datetime import datetime, timezone

try:
    from filelock import FileLock
except ImportError:
    FileLock = None

try:
    from pydantic import ValidationError
    from .models import RegistryData, ProjectConfig
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    ValidationError = Exception

from .config import Config

logger = logging.getLogger(__name__)

class Registry:
    """Thread-safe registry with file locking"""
    REGISTRY_FILE = None  # For testing override
    
    def __init__(self, registry_path: Optional[Path] = None):
        from .utils import validate_safe_path
        if registry_path:
            self.registry_path = validate_safe_path(str(registry_path))
        elif self.REGISTRY_FILE:
            self.registry_path = self.REGISTRY_FILE
        else:
            self.config = Config()
            self.registry_path = self.config.registry_path
        self._ensure_registry()
        # Lazy loading cache
        self._cache = None
        self._cache_time = None
        self._cache_ttl = 5.0  # seconds
    
    def _ensure_registry(self):
        """Initialize registry if missing"""
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            self._write({"projects": {}, "active": None})
    
    @contextmanager
    def _lock(self, mode='r'):
        """Cross-platform file locking with proper cleanup order"""
        lock_file = None
        file_handle = None
        
        try:
            if FileLock:
                lock_file = FileLock(str(self.registry_path) + '.lock', timeout=10)
                lock_file.acquire()
            else:
                logger.warning("filelock not installed, registry operations not thread-safe")
            
            # Open file after acquiring lock
            file_handle = open(self.registry_path, mode)
            yield file_handle
            
        finally:
            # Ensure file is closed before releasing lock (proper order)
            if file_handle:
                try:
                    file_handle.close()
                except Exception as e:
                    logger.debug(f"Error closing file: {e}")
            
            # Release lock last
            if lock_file:
                try:
                    lock_file.release()
                except Exception as e:
                    logger.debug(f"Error releasing lock: {e}")
    
    def _read(self) -> Dict:
        """Read with lock, caching, and validation"""
        # Return cached data if still valid
        now = time.time()
        if self._cache and self._cache_time and (now - self._cache_time) < self._cache_ttl:
            return self._cache
        
        try:
            with self._lock('r') as f:
                data = json.load(f)
                
                # Validate with Pydantic if available
                if PYDANTIC_AVAILABLE:
                    try:
                        # Convert old format to new
                        if 'active_project' in data:
                            data['active'] = data.pop('active_project')
                        
                        registry_model = RegistryData(**data)
                        data = registry_model.model_dump()
                    except ValidationError as e:
                        logger.warning(f"Registry validation failed: {e}, using raw data")
                
                self._cache = data
                self._cache_time = now
                return data
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Registry read error: {e}, reinitializing")
            return {"projects": {}, "active": None}
    
    def _write(self, data: Dict):
        """Write with lock, validation, and invalidate cache"""
        # Validate with Pydantic if available
        if PYDANTIC_AVAILABLE:
            try:
                # Ensure correct field names
                if 'active_project' in data:
                    data['active'] = data.pop('active_project')
                
                registry_model = RegistryData(**data)
                data = registry_model.model_dump()
            except ValidationError as e:
                logger.error(f"Registry validation failed before write: {e}")
                raise ValueError(f"Invalid registry data: {e}")
        
        with self._lock('w') as f:
            json.dump(data, f, indent=2)
        # Invalidate cache on write
        self._cache = None
        self._cache_time = None
    
    def add_project(self, name: str, path: str, description: str = "", tags: List[str] = None):
        """Add project with metadata"""
        from .utils import validate_safe_path
        data = self._read()
        safe_path = validate_safe_path(path)
        data["projects"][name] = {
            "path": str(safe_path),
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
        data["active"] = name
        self._write(data)
    
    def get_active(self) -> Optional[str]:
        """Get active project"""
        data = self._read()
        # Support both old and new field names
        return data.get("active") or data.get("active_project")
    
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
