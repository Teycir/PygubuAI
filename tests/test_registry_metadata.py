"""Tests for registry metadata features"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.registry import Registry


class TestRegistryMetadata(unittest.TestCase):
    """Test registry metadata functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = Path(self.temp_dir) / "test_registry.json"
        Registry.REGISTRY_FILE = self.registry_file
        self.registry = Registry()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        Registry.REGISTRY_FILE = None
    
    def test_add_project_with_metadata(self):
        """Test adding project with description and tags"""
        self.registry.add_project(
            "testapp",
            "/path/to/testapp",
            description="Test application",
            tags=["test", "demo"]
        )
        
        metadata = self.registry.get_project_metadata("testapp")
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['path'], "/path/to/testapp")
        self.assertEqual(metadata['description'], "Test application")
        self.assertEqual(metadata['tags'], ["test", "demo"])
        self.assertIsNotNone(metadata['created'])
        self.assertIsNotNone(metadata['modified'])
    
    def test_get_project_backward_compatible(self):
        """Test get_project returns path for backward compatibility"""
        self.registry.add_project(
            "testapp",
            "/path/to/testapp",
            description="Test app"
        )
        
        path = self.registry.get_project("testapp")
        self.assertEqual(path, "/path/to/testapp")
    
    def test_list_projects_with_metadata(self):
        """Test listing projects with full metadata"""
        self.registry.add_project("app1", "/path/1", description="App 1", tags=["tag1"])
        self.registry.add_project("app2", "/path/2", description="App 2", tags=["tag2"])
        
        projects = self.registry.list_projects_with_metadata()
        self.assertEqual(len(projects), 2)
        self.assertIn("app1", projects)
        self.assertIn("app2", projects)
        self.assertEqual(projects["app1"]["description"], "App 1")
        self.assertEqual(projects["app2"]["tags"], ["tag2"])
    
    def test_search_projects_by_name(self):
        """Test searching projects by name"""
        self.registry.add_project("loginapp", "/path/1", description="Login form")
        self.registry.add_project("todoapp", "/path/2", description="Todo list")
        
        results = self.registry.search_projects("login")
        self.assertEqual(len(results), 1)
        self.assertIn("loginapp", results)
    
    def test_search_projects_by_description(self):
        """Test searching projects by description"""
        self.registry.add_project("app1", "/path/1", description="Login form")
        self.registry.add_project("app2", "/path/2", description="Todo list")
        
        results = self.registry.search_projects("form")
        self.assertEqual(len(results), 1)
        self.assertIn("app1", results)
    
    def test_search_projects_by_tags(self):
        """Test searching projects by tags"""
        self.registry.add_project("app1", "/path/1", tags=["production", "web"])
        self.registry.add_project("app2", "/path/2", tags=["development", "cli"])
        
        results = self.registry.search_projects("production")
        self.assertEqual(len(results), 1)
        self.assertIn("app1", results)
    
    def test_search_projects_case_insensitive(self):
        """Test search is case insensitive"""
        self.registry.add_project("MyApp", "/path/1", description="Test App")
        
        results = self.registry.search_projects("myapp")
        self.assertEqual(len(results), 1)
        
        results = self.registry.search_projects("TEST")
        self.assertEqual(len(results), 1)
    
    def test_update_project_metadata(self):
        """Test updating project metadata"""
        self.registry.add_project("app", "/path", description="Old desc", tags=["old"])
        
        self.registry.update_project_metadata("app", description="New desc", tags=["new"])
        
        metadata = self.registry.get_project_metadata("app")
        self.assertEqual(metadata['description'], "New desc")
        self.assertEqual(metadata['tags'], ["new"])
    
    def test_update_nonexistent_project(self):
        """Test updating nonexistent project raises error"""
        with self.assertRaises(ValueError):
            self.registry.update_project_metadata("nonexistent", description="test")
    
    def test_backward_compatibility_old_format(self):
        """Test backward compatibility with old registry format"""
        # Manually create old format registry
        import json
        old_data = {
            "projects": {
                "oldapp": "/path/to/oldapp"
            },
            "active_project": None
        }
        self.registry_file.write_text(json.dumps(old_data))
        
        # Create new registry instance
        registry = Registry()
        
        # Should still work
        path = registry.get_project("oldapp")
        self.assertEqual(path, "/path/to/oldapp")
        
        # Metadata should return defaults
        metadata = registry.get_project_metadata("oldapp")
        self.assertEqual(metadata['path'], "/path/to/oldapp")
        self.assertEqual(metadata['description'], "")
        self.assertEqual(metadata['tags'], [])


if __name__ == '__main__':
    unittest.main()
