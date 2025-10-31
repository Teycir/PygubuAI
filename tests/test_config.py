#!/usr/bin/env python3
"""Tests for configuration management"""
import unittest
import tempfile
import pathlib
import json
import os
import sys
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))
from pygubuai.config import Config  # noqa: E402


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.config_path = pathlib.Path(self.temp_dir) / "config.json"

    def test_default_config(self):
        """Test default configuration values"""
        self.assertIsNotNone(self.config.config.get("registry_path"))
        self.assertIsNotNone(self.config.config.get("ai_context_dir"))

    def test_registry_path(self):
        """Test registry path property"""
        registry_path = self.config.registry_path
        self.assertIsInstance(registry_path, pathlib.Path)

    def test_config_load(self):
        """Test config loading"""
        config = self.config._load()
        self.assertIsInstance(config, dict)
        self.assertIn("registry_path", config)

    def test_config_get_method(self):
        """Test Config.get() method"""
        value = self.config.get("registry_path")
        self.assertIsNotNone(value)

        default_value = self.config.get("nonexistent", "default")
        self.assertEqual(default_value, "default")

    def test_config_save(self):
        """Test saving configuration"""
        self.config.config["test_key"] = "test_value"
        self.config.save()

        self.assertTrue(self.config.config_path.exists())
        saved_data = json.loads(self.config.config_path.read_text())
        self.assertEqual(saved_data["test_key"], "test_value")

    def test_env_override(self):
        """Test environment variable overrides"""
        with patch.dict(os.environ, {"PYGUBUAI_REGISTRY_PATH": "/tmp/test.json"}):
            config = Config()
            config.config_path = pathlib.Path(self.temp_dir) / "config.json"
            loaded = config._load()
            self.assertEqual(loaded["registry_path"], "/tmp/test.json")

    def test_config_file_merging(self):
        """Test user config file merges with defaults"""
        user_config = {"registry_path": "/custom/path.json"}
        self.config.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.config_path.write_text(json.dumps(user_config))

        loaded = self.config._load()
        self.assertEqual(loaded["registry_path"], "/custom/path.json")
        # Should still have defaults
        self.assertIn("ai_context_dir", loaded)

    def test_invalid_config_file(self):
        """Test handling of invalid config file"""
        self.config.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.config_path.write_text("invalid json{")

        loaded = self.config._load()
        # Should fall back to defaults
        self.assertIn("registry_path", loaded)


class TestConfigPriority(unittest.TestCase):
    """Test configuration priority: env > file > defaults"""

    def test_priority_env_over_file(self):
        """Test environment variables override config file"""
        temp_dir = tempfile.mkdtemp()
        config_path = pathlib.Path(temp_dir) / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Write config file
        config_path.write_text(json.dumps({"registry_path": "/file/path.json"}))

        # Override with env
        with patch.dict(os.environ, {"PYGUBUAI_REGISTRY_PATH": "/env/path.json"}):
            config = Config()
            config.config_path = config_path
            loaded = config._load()
            self.assertEqual(loaded["registry_path"], "/env/path.json")

    def test_priority_file_over_defaults(self):
        """Test config file overrides defaults"""
        temp_dir = tempfile.mkdtemp()
        config_path = pathlib.Path(temp_dir) / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        custom_path = "/custom/registry.json"
        config_path.write_text(json.dumps({"registry_path": custom_path}))

        config = Config()
        config.config_path = config_path
        loaded = config._load()

        self.assertEqual(loaded["registry_path"], custom_path)
        self.assertNotEqual(loaded["registry_path"], Config.DEFAULT["registry_path"])


if __name__ == "__main__":
    unittest.main()
