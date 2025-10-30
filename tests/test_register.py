#!/usr/bin/env python3
"""Tests for register module"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai.register import register_project, set_active, scan_directory
from pygubuai.registry import Registry
from pygubuai.errors import ProjectNotFoundError, InvalidProjectError

class TestRegister(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = pathlib.Path(self.temp_dir) / ".pygubu-registry.json"
        Registry.REGISTRY_FILE = self.registry_file
    
    def test_register_project(self):
        """Test registering a project"""
        project_dir = pathlib.Path(self.temp_dir) / "testproj"
        project_dir.mkdir()
        (project_dir / "test.ui").write_text("<ui></ui>")
        
        register_project(str(project_dir))
        
        registry = Registry()
        projects = registry.list_projects()
        self.assertIn("testproj", projects)
        self.assertEqual(projects["testproj"], str(project_dir))
    
    def test_register_nonexistent_path(self):
        """Test registering nonexistent path raises error"""
        with self.assertRaises(InvalidProjectError):
            register_project("/nonexistent/path")
    
    def test_register_no_ui_files(self):
        """Test registering directory without .ui files raises error"""
        project_dir = pathlib.Path(self.temp_dir) / "noproj"
        project_dir.mkdir()
        
        with self.assertRaises(InvalidProjectError):
            register_project(str(project_dir))
    
    def test_set_active(self):
        """Test setting active project"""
        project_dir = pathlib.Path(self.temp_dir) / "testproj"
        project_dir.mkdir()
        (project_dir / "test.ui").write_text("<ui></ui>")
        
        register_project(str(project_dir))
        set_active("testproj")
        
        registry = Registry()
        self.assertEqual(registry.get_active(), "testproj")
    
    def test_set_active_nonexistent(self):
        """Test setting nonexistent project as active raises error"""
        with self.assertRaises(ProjectNotFoundError):
            set_active("nonexistent")
    
    def test_scan_directory(self):
        """Test scanning directory for projects"""
        proj1 = pathlib.Path(self.temp_dir) / "proj1"
        proj1.mkdir()
        (proj1 / "test.ui").write_text("<ui></ui>")
        
        proj2 = pathlib.Path(self.temp_dir) / "proj2"
        proj2.mkdir()
        (proj2 / "app.ui").write_text("<ui></ui>")
        
        scan_directory(self.temp_dir)
        
        registry = Registry()
        projects = registry.list_projects()
        self.assertIn("proj1", projects)
        self.assertIn("proj2", projects)

if __name__ == '__main__':
    unittest.main()
