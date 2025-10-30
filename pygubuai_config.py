#!/usr/bin/env python3
"""Centralized configuration for PygubuAI"""
import json
import pathlib
from typing import Dict, Any

class Config:
    DEFAULT_CONFIG = {
        "registry_path": "~/.pygubu-registry.json",
        "ai_context_dir": "~/.amazonq/prompts",
        "default_window_size": {"width": 600, "height": 400},
        "default_padding": 20,
        "auto_backup": True,
        "verbose": False
    }
    
    def __init__(self):
        self.config_path = pathlib.Path.home() / ".pygubuai" / "config.json"
        self.config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return self.DEFAULT_CONFIG.copy()
    
    def save(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2))
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        self.config[key] = value
        self.save()
    
    @property
    def registry_path(self) -> pathlib.Path:
        return pathlib.Path(self.config["registry_path"]).expanduser()
    
    @property
    def ai_context_dir(self) -> pathlib.Path:
        return pathlib.Path(self.config["ai_context_dir"]).expanduser()

def get_config() -> Config:
    return Config()
