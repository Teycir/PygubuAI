"""Thread-safe project registry"""
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from contextlib import contextmanager

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
    
    def add_project(self, name: str, path: str):
        """Add project"""
        data = self._read()
        data["projects"][name] = str(Path(path).resolve())
        self._write(data)
    
    def get_project(self, name: str) -> Optional[str]:
        """Get project path"""
        data = self._read()
        return data["projects"].get(name)
    
    def list_projects(self) -> Dict[str, str]:
        """List all projects"""
        return self._read()["projects"]
    
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
