#!/usr/bin/env python3
"""Tests for status module"""
import unittest
import tempfile
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.status import get_project_status
from pygubuai.registry import Registry

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = pathlib.Path(self.temp_dir) / ".pygubu-registry.json"
        Registry.REGISTRY_FILE = self.registry_file
        
        # Create test project
        self.project_dir = pathlib.Path(self.temp_dir) / "testapp"
        self.project_dir.mkdir()
        
        self.ui_file = self.project_dir / "testapp.ui"
        self.py_file = self.project_dir / "testapp.py"
        
        self.ui_file.write_text("<interface></interface>")
        self.py_file.write_text("# Test")
        
        registry = Registry()
        registry.add_project("testapp", str(self.project_dir))
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        Registry.REGISTRY_FILE = None
    
    def test_in_sync(self):
        """Test files in sync"""
        status = get_project_status("testapp")
        self.assertEqual(status["sync_status"], "In Sync")
    
    def test_ui_ahead(self):
        """Test UI file modified after code"""
        time.sleep(0.1)
        self.ui_file.write_text("<interface>modified</interface>")
        
        status = get_project_status("testapp")
        self.assertEqual(status["sync_status"], "UI Ahead")
    
    def test_code_ahead(self):
        """Test code modified after UI"""
        time.sleep(0.1)
        self.py_file.write_text("# Modified")
        
        status = get_project_status("testapp")
        self.assertEqual(status["sync_status"], "Code Ahead")

if __name__ == '__main__':
    unittest.main()
