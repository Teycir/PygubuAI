"""Configuration management with environment variable support and config merging."""

import json
import os
import pathlib
import threading
from typing import Dict, Any


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
    _lock = threading.Lock()

    def __init__(self):
        """Initialize configuration with merged sources."""
        self.config_path = pathlib.Path.home() / ".pygubuai" / "config.json"
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        """Load and merge configuration from all sources with error reporting.

        Returns:
            Merged configuration dictionary
        """
        import logging

        logger = logging.getLogger(__name__)

        with self._lock:
            config = self.DEFAULT.copy()

            # Load user config file if exists
            if self.config_path.exists():
                try:
                    user_config = json.loads(self.config_path.read_text())
                    if not isinstance(user_config, dict):
                        logger.warning(f"Invalid config format in {self.config_path}, using defaults")
                    else:
                        config.update(user_config)
                        logger.debug(f"Loaded user config from {self.config_path}")

                except json.JSONDecodeError as e:
                    logger.warning(
                        f"Config file corrupted at line {e.lineno}: {e.msg}. "
                        f"Using defaults. Fix or delete: {self.config_path}"
                    )
                except OSError as e:
                    logger.warning(f"Cannot read config file: {e}. Using defaults.")

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
        """Get registry file path with validation.

        Returns:
            Validated and expanded path to registry file
        """
        import logging

        logger = logging.getLogger(__name__)

        path_str = self.config["registry_path"]
        try:
            # Expand user home directory
            expanded = pathlib.Path(path_str).expanduser()

            # Basic validation: no directory traversal in unexpanded path
            if ".." in pathlib.Path(path_str).parts:
                logger.warning(f"Suspicious path in config: {path_str}, using default")
                return pathlib.Path.home() / ".pygubu-registry.json"

            return expanded

        except (ValueError, RuntimeError) as e:
            logger.warning(f"Invalid registry path '{path_str}': {e}, using default")
            return pathlib.Path.home() / ".pygubu-registry.json"

    def save(self) -> None:
        """Save current configuration to user config file.

        Raises:
            OSError: If unable to write config file
        """
        with self._lock:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(json.dumps(self.config, indent=2))
