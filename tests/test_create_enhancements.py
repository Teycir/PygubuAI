"""Tests for create command enhancements"""
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import pygubuai.template
from pygubuai.create import create_project


class TestCreateEnhancements(unittest.TestCase):
    """Test enhanced create functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    @patch('pygubuai.create.validate_pygubu')
    def test_dry_run_mode(self, mock_validate):
        """Test dry-run mode doesn't create files"""
        create_project("testapp", "test app", dry_run=True)
        
        # Verify no files created
        project_dir = Path(self.temp_dir) / "testapp"
        self.assertFalse(project_dir.exists())
    
    @patch('pygubuai.create.validate_pygubu')
    @patch('pygubuai.create.init_git_repo', return_value=True)
    def test_git_integration(self, mock_git, mock_validate):
        """Test git initialization during project creation"""
        create_project("testapp", "test app", init_git=True)
        
        # Verify git was called
        mock_git.assert_called_once()
        
        # Verify project created
        project_dir = Path(self.temp_dir) / "testapp"
        self.assertTrue(project_dir.exists())
    
    @patch('pygubuai.create.validate_pygubu')
    @patch('pygubuai.create.Registry')
    def test_auto_registration(self, mock_registry_class, mock_validate):
        """Test project is automatically registered"""
        mock_registry = MagicMock()
        mock_registry_class.return_value = mock_registry
        
        create_project("testapp", "test app", tags=["test"])
        
        # Verify registry.add_project was called
        mock_registry.add_project.assert_called_once()
        call_args = mock_registry.add_project.call_args
        self.assertEqual(call_args[0][0], "testapp")
        self.assertEqual(call_args[1]['description'], "test app")
        self.assertEqual(call_args[1]['tags'], ["test"])
    
    @patch('pygubuai.create.validate_pygubu')
    def test_template_usage(self, mock_validate):
        """Test using template during creation with dry-run"""
        # Just test that template parameter is accepted
        create_project("testapp", "test app", template="login", dry_run=True)
        # No exception means success
    
    @patch('pygubuai.create.validate_pygubu')
    def test_tags_support(self, mock_validate):
        """Test creating project with tags"""
        with patch('pygubuai.create.Registry') as mock_registry_class:
            mock_registry = MagicMock()
            mock_registry_class.return_value = mock_registry
            
            create_project("testapp", "test app", tags=["web", "production"])
            
            call_args = mock_registry.add_project.call_args
            self.assertEqual(call_args[1]['tags'], ["web", "production"])


class TestCreateCLI(unittest.TestCase):
    """Test create CLI argument parsing"""
    
    @patch('pygubuai.create.create_project')
    def test_interactive_flag(self, mock_create):
        """Test --interactive flag"""
        from pygubuai.create import main
        
        with patch('pygubuai.create.interactive_create', return_value={
            'name': 'myapp',
            'description': 'test',
            'template': None,
            'git': False
        }):
            main(['--interactive'])
            mock_create.assert_called_once()
    
    @patch('pygubuai.create.create_project')
    def test_dry_run_flag(self, mock_create):
        """Test --dry-run flag"""
        from pygubuai.create import main
        
        main(['testapp', 'test app', '--dry-run'])
        
        call_args = mock_create.call_args
        self.assertTrue(call_args[1]['dry_run'])
    
    @patch('pygubuai.create.create_project')
    def test_git_flag(self, mock_create):
        """Test --git flag"""
        from pygubuai.create import main
        
        main(['testapp', 'test app', '--git'])
        
        call_args = mock_create.call_args
        self.assertTrue(call_args[1]['init_git'])
    
    @patch('pygubuai.create.create_project')
    def test_template_flag(self, mock_create):
        """Test --template flag"""
        from pygubuai.create import main
        
        main(['testapp', 'test app', '--template', 'login'])
        
        call_args = mock_create.call_args
        self.assertEqual(call_args[1]['template'], 'login')
    
    @patch('pygubuai.create.create_project')
    def test_tags_flag(self, mock_create):
        """Test --tags flag"""
        from pygubuai.create import main
        
        main(['testapp', 'test app', '--tags', 'web,production'])
        
        call_args = mock_create.call_args
        self.assertEqual(call_args[1]['tags'], ['web', 'production'])


if __name__ == '__main__':
    unittest.main()
