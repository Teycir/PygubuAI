"""Configuration management with environment variable support and config merging."""
import json
import os
import pathlib
from typing import Dict, Any, Optional

class Config:
    """Configuration manager with multiple source support.
    
    Configuration priority (highest to lowest):
    1. Environment variables (PYGUBUAI_*)
    2. User config file (~/.pygubuai/config.json)
    3. Default values
    
    Environment variables:
        PYGUBUAI_REGISTRY_PATH: Override registry file location
        PYGUBUAI_AI_CONTEXT_DIR: Override AI context directory
        PYGUBUAI_LOG_LEVEL: Set logging level (DEBUG, INFO, WARNING, ERROR)
    """
    
    DEFAULT = {
        "registry_path": "~/.pygubu-registry.json",
        "ai_context_dir": "~/.amazonq/prompts",
        "default_window_size": {"width": 600, "height": 400},
        "default_padding": 20,
    }
    
    ENV_PREFIX = "PYGUBUAI_"
    
    def __init__(self):
        """Initialize configuration with merged sources."""
        self.config_path = pathlib.Path.home() / ".pygubuai" / "config.json"
        self.config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load and merge configuration from all sources.
        
        Returns:
            Merged configuration dictionary
        """
        config = self.DEFAULT.copy()
        
        # Load user config file if exists
        if self.config_path.exists():
            try:
                user_config = json.loads(self.config_path.read_text())
                config.update(user_config)
            except (json.JSONDecodeError, OSError):
                pass
        
        # Override with environment variables
        config = self._apply_env_overrides(config)
        return config
    
    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to config.
        
        Args:
            config: Base configuration dictionary
            
        Returns:
            Configuration with environment overrides applied
        """
        env_map = {
            "PYGUBUAI_REGISTRY_PATH": "registry_path",
            "PYGUBUAI_AI_CONTEXT_DIR": "ai_context_dir",
        }
        
        for env_var, config_key in env_map.items():
            value = os.environ.get(env_var)
            if value:
                config[config_key] = value
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with optional default.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    @property
    def registry_path(self) -> pathlib.Path:
        """Get registry file path.
        
        Returns:
            Expanded path to registry file
        """
        return pathlib.Path(self.config["registry_path"]).expanduser()
    
    def save(self) -> None:
        """Save current configuration to user config file.
        
        Raises:
            OSError: If unable to write config file
        """
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2))
