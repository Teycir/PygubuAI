#!/usr/bin/env python3
"""Tests for configuration management"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from pygubuai_config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.config_path = pathlib.Path(self.temp_dir) / "config.json"
    
    def test_default_config(self):
        """Test default configuration values"""
        self.assertIsNotNone(self.config.get("registry_path"))
        self.assertIsNotNone(self.config.get("ai_context_dir"))
    
    def test_set_and_get(self):
        """Test setting and getting config values"""
        self.config.set("test_key", "test_value")
        self.assertEqual(self.config.get("test_key"), "test_value")
    
    def test_save_and_load(self):
        """Test config persistence"""
        self.config.set("custom", "value")
        self.config.save()
        
        new_config = Config()
        new_config.config_path = self.config.config_path
        new_config.config = new_config._load()
        
        self.assertEqual(new_config.get("custom"), "value")

if __name__ == '__main__':
    unittest.main()
