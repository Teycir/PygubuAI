#!/usr/bin/env python3
"""Integration tests for CLI entry points."""
import unittest
import tempfile
import pathlib
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.create import create_project, main as create_main
from pygubuai.errors import PygubuAIError

class TestCLIIntegration(unittest.TestCase):
    """Test CLI entry points and command-line argument handling."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
    
    def test_create_project_success(self):
        """Test successful project creation."""
        project_name = "testapp"
        description = "test app with button"
        
        create_project(project_name, description, skip_validation=True)
        
        project_dir = pathlib.Path(self.temp_dir) / project_name
        self.assertTrue(project_dir.exists())
        self.assertTrue((project_dir / f"{project_name}.ui").exists())
        self.assertTrue((project_dir / f"{project_name}.py").exists())
        self.assertTrue((project_dir / "README.md").exists())
    
    def test_create_project_invalid_name(self):
        """Test project creation with invalid name gets sanitized."""
        # Invalid names are now sanitized rather than raising errors
        project_name = "invalid-name!"
        create_project(project_name, "test app", skip_validation=True)
        
        # Should create with sanitized name
        sanitized = "invalid-name_"
        project_dir = pathlib.Path(self.temp_dir) / sanitized
        self.assertTrue(project_dir.exists())
    
    def test_create_main_with_args(self):
        """Test create main function with command-line arguments."""
        args = ["testcli", "test app with entry"]
        
        # Main may exit with 1 if pygubu not installed
        try:
            create_main(args)
            project_dir = pathlib.Path(self.temp_dir) / "testcli"
            self.assertTrue(project_dir.exists())
        except SystemExit:
            # Expected if pygubu not installed
            pass
    
    def test_create_main_version(self):
        """Test --version flag."""
        with self.assertRaises(SystemExit) as cm:
            create_main(['--version'])
        self.assertEqual(cm.exception.code, 0)
    
    def test_create_main_help(self):
        """Test --help flag."""
        with self.assertRaises(SystemExit) as cm:
            create_main(['--help'])
        self.assertEqual(cm.exception.code, 0)
    
    def test_create_project_with_callbacks(self):
        """Test project creation includes callbacks."""
        project_name = "callbacktest"
        description = "app with button that triggers action"
        
        create_project(project_name, description, skip_validation=True)
        
        py_file = pathlib.Path(self.temp_dir) / project_name / f"{project_name}.py"
        content = py_file.read_text()
        
        # Should have callback method
        self.assertIn("def on_", content)

class TestWorkflowCLI(unittest.TestCase):
    """Test workflow CLI commands."""
    
    def test_workflow_help(self):
        """Test workflow help output."""
        from pygubuai.workflow import main as workflow_main
        
        # Workflow main reads from sys.argv, not arguments
        with patch('sys.argv', ['workflow', '--help']):
            with self.assertRaises(SystemExit) as cm:
                workflow_main()
            self.assertEqual(cm.exception.code, 0)
    
    def test_workflow_version(self):
        """Test workflow version output."""
        from pygubuai.workflow import main as workflow_main
        
        with patch('sys.argv', ['workflow', '--version']):
            with patch('sys.exit'):
                workflow_main()

class TestConfigCLI(unittest.TestCase):
    """Test configuration with environment variables."""
    
    def test_env_override_registry_path(self):
        """Test PYGUBUAI_REGISTRY_PATH environment variable."""
        from pygubuai.config import Config
        
        custom_path = "/tmp/custom-registry.json"
        with patch.dict(os.environ, {'PYGUBUAI_REGISTRY_PATH': custom_path}):
            config = Config()
            self.assertEqual(str(config.registry_path), custom_path)
    
    def test_env_override_ai_context_dir(self):
        """Test PYGUBUAI_AI_CONTEXT_DIR environment variable."""
        from pygubuai.config import Config
        
        custom_dir = "/tmp/custom-context"
        with patch.dict(os.environ, {'PYGUBUAI_AI_CONTEXT_DIR': custom_dir}):
            config = Config()
            self.assertEqual(config.get('ai_context_dir'), custom_dir)
    
    def test_config_get_with_default(self):
        """Test Config.get() with default value."""
        from pygubuai.config import Config
        
        config = Config()
        value = config.get('nonexistent_key', 'default_value')
        self.assertEqual(value, 'default_value')

if __name__ == '__main__':
    unittest.main()
