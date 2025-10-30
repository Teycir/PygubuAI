"""Configuration management"""
import json
import pathlib
from typing import Dict, Any

class Config:
    DEFAULT = {
        "registry_path": "~/.pygubu-registry.json",
        "ai_context_dir": "~/.amazonq/prompts",
        "default_window_size": {"width": 600, "height": 400},
        "default_padding": 20,
    }
    
    def __init__(self):
        self.config_path = pathlib.Path.home() / ".pygubuai" / "config.json"
        self.config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text())
            except (json.JSONDecodeError, OSError):
                return self.DEFAULT.copy()
        return self.DEFAULT.copy()
    
    @property
    def registry_path(self) -> pathlib.Path:
        return pathlib.Path(self.config["registry_path"]).expanduser()
