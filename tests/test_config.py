#!/usr/bin/env python3
"""Tests for configuration management"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai.config import Config

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

if __name__ == '__main__':
    unittest.main()
