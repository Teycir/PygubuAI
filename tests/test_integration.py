#!/usr/bin/env python3
"""Integration tests for PygubuAI workflows"""
import unittest
import tempfile
import pathlib
import sys
import json
import subprocess

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete project creation and registration workflow"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = pathlib.Path.cwd()
        import os
        os.chdir(self.temp_dir)
        
        # Create temporary registry
        self.registry_file = pathlib.Path(self.temp_dir) / ".pygubu-registry.json"
        self.original_registry = pathlib.Path.home() / ".pygubu-registry.json"
        
    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_and_register_workflow(self):
        """Test creating a project and registering it"""
        from pygubuai.create import create_project
        from pygubuai.registry import Registry
        
        # Create project
        create_project("testapp", "simple app with button", skip_validation=True)
        
        # Verify files exist
        project_dir = pathlib.Path(self.temp_dir) / "testapp"
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / "testapp.ui").exists())
        self.assertTrue((project_dir / "testapp.py").exists())
        self.assertTrue((project_dir / "README.md").exists())
        
        # Register project
        Registry.REGISTRY_FILE = self.registry_file
        registry = Registry()
        registry.add_project("testapp", str(project_dir))
        
        # Verify registration
        projects = registry.list_projects()
        self.assertEqual(len(projects), 1)
        self.assertIn("testapp", projects)
    
    def test_template_creation_workflow(self):
        """Test creating project from template"""
        from pygubuai.template import create_from_template
        from pygubuai.template_data import TEMPLATES
        
        # Create from login template
        create_from_template("loginapp", "login", skip_validation=True)
        
        # Verify files
        project_dir = pathlib.Path(self.temp_dir) / "loginapp"
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / "loginapp.ui").exists())
        self.assertTrue((project_dir / "loginapp.py").exists())
        
        # Verify UI contains expected widgets
        ui_content = (project_dir / "loginapp.ui").read_text()
        self.assertIn("ttk.Entry", ui_content)
        self.assertIn("ttk.Button", ui_content)


class TestCLIIntegration(unittest.TestCase):
    """Test CLI commands work end-to-end"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = pathlib.Path.cwd()
        import os
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_cli_command(self):
        """Test pygubu-create CLI works"""
        # Skip this test if pygubu is not installed
        try:
            import pygubu
        except ImportError:
            self.skipTest("pygubu not installed")
        
        result = subprocess.run(
            [sys.executable, "-m", "pygubuai.create", "cliapp", "test app"],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )
        
        # Should succeed
        self.assertEqual(result.returncode, 0)
        
        # Files should exist
        project_dir = pathlib.Path(self.temp_dir) / "cliapp"
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / "cliapp.ui").exists())


if __name__ == '__main__':
    unittest.main()
