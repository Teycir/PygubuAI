#!/usr/bin/env python3
"""Tests for project registry functionality"""
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))
from pygubuai.registry import Registry  # noqa: E402


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.old_home = os.environ.get("HOME")
        os.environ["HOME"] = self.temp_dir

    def tearDown(self):
        if self.old_home:
            os.environ["HOME"] = self.old_home

    def test_registry_creation(self):
        """Test registry initialization"""
        registry = Registry()
        self.assertTrue(registry.registry_path.parent.exists())

    def test_add_project(self):
        """Test adding project"""
        registry = Registry()
        registry.add_project("test", "/test/path")
        self.assertIn("test", registry.list_projects())

    def test_set_active(self):
        """Test setting active project"""
        registry = Registry()
        registry.add_project("test", "/test/path")
        registry.set_active("test")
        self.assertEqual(registry.get_active(), "test")


if __name__ == "__main__":
    unittest.main()
