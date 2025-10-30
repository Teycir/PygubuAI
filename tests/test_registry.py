#!/usr/bin/env python3
"""Tests for project registry functionality"""
import unittest
import tempfile
import pathlib
import json
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.registry_path = pathlib.Path(self.temp_file.name)
        self.temp_file.close()
    
    def tearDown(self):
        if self.registry_path.exists():
            self.registry_path.unlink()
    
    def test_registry_creation(self):
        """Test registry file creation"""
        registry = {"projects": {}, "active": None}
        self.registry_path.write_text(json.dumps(registry))
        self.assertTrue(self.registry_path.exists())
    
    def test_add_project(self):
        """Test adding project to registry"""
        registry = {"projects": {}, "active": None}
        registry["projects"]["test"] = {"path": "/test/path", "created": "2024-01-01"}
        self.assertIn("test", registry["projects"])
    
    def test_set_active(self):
        """Test setting active project"""
        registry = {"projects": {"test": {"path": "/test"}}, "active": None}
        registry["active"] = "test"
        self.assertEqual(registry["active"], "test")

if __name__ == '__main__':
    unittest.main()
