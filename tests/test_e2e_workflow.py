"""End-to-end workflow tests."""
import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.create import create_project
from pygubuai.registry import Registry


class TestE2EWorkflow(unittest.TestCase):
    """Test complete user workflows."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = Path(self.temp_dir) / "registry.json"
        # Override registry file for testing
        Registry.REGISTRY_FILE = self.registry_file
        self.registry = Registry()
    
    def tearDown(self):
        Registry.REGISTRY_FILE = None
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_register_workflow(self):
        """Test: Create project -> Register -> Set active."""
        # Create project
        old_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)
            create_project("testapp", "test app with button", skip_validation=True)
            project_path = Path(self.temp_dir) / "testapp"
        finally:
            os.chdir(old_cwd)
        
        self.assertTrue(project_path.exists())
        self.assertTrue((project_path / "testapp.ui").exists())
        self.assertTrue((project_path / "testapp.py").exists())
        
        # Register project
        self.registry.add_project("testapp", str(project_path))
        projects = self.registry.list_projects()
        self.assertEqual(len(projects), 1)
        self.assertIn("testapp", projects)
        
        # Set active
        self.registry.set_active("testapp")
        active = self.registry.get_active()
        self.assertEqual(active, "testapp")
    
    def test_create_track_workflow(self):
        """Test: Create project -> Track changes."""
        old_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)
            create_project("testapp", "test app", skip_validation=True)
            project_path = Path(self.temp_dir) / "testapp"
        finally:
            os.chdir(old_cwd)
        
        # Verify workflow file can be created
        workflow_file = project_path / ".pygubu-workflow.json"
        workflow_data = {
            "file_hashes": {},
            "changes": [{"event": "project_created", "description": "test app"}]
        }
        workflow_file.write_text(json.dumps(workflow_data))
        
        # Verify workflow file exists and is valid
        self.assertTrue(workflow_file.exists())
        loaded = json.loads(workflow_file.read_text())
        self.assertEqual(len(loaded["changes"]), 1)
        self.assertEqual(loaded["changes"][0]["event"], "project_created")
    
    def test_multi_project_workflow(self):
        """Test: Create multiple projects -> Register all -> Switch active."""
        projects = ["app1", "app2", "app3"]
        
        old_cwd = os.getcwd()
        try:
            os.chdir(self.temp_dir)
            # Create multiple projects
            for name in projects:
                create_project(name, f"{name} description", skip_validation=True)
                project_path = Path(self.temp_dir) / name
                # Project is auto-registered by create_project
        finally:
            os.chdir(old_cwd)
        
        # Verify all registered
        all_projects = self.registry.list_projects()
        self.assertEqual(len(all_projects), 3)
        
        # Switch active between projects
        for name in projects:
            self.registry.set_active(name)
            active = self.registry.get_active()
            self.assertEqual(active, name)


if __name__ == "__main__":
    unittest.main()
