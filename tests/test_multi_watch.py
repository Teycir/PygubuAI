"""Tests for multi-project watch"""
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from pygubuai.multi_watch import watch_multiple_projects, watch_all_projects
from pygubuai.errors import ProjectNotFoundError


class TestMultiWatch(unittest.TestCase):
    """Test multi-project watch functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.proj1 = Path(self.temp_dir) / "proj1"
        self.proj2 = Path(self.temp_dir) / "proj2"
        self.proj1.mkdir()
        self.proj2.mkdir()
        (self.proj1 / "test.ui").write_text("<ui>1</ui>")
        (self.proj2 / "test.ui").write_text("<ui>2</ui>")
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    @patch('pygubuai.multi_watch.Registry')
    def test_watch_multiple_projects(self, mock_registry_class):
        """Test watching multiple projects"""
        mock_registry = MagicMock()
        mock_registry.list_projects.return_value = {
            'proj1': str(self.proj1),
            'proj2': str(self.proj2)
        }
        mock_registry_class.return_value = mock_registry
        
        with patch('time.sleep', side_effect=KeyboardInterrupt):
            try:
                watch_multiple_projects(['proj1', 'proj2'])
            except KeyboardInterrupt:
                pass
    
    @patch('pygubuai.multi_watch.Registry')
    def test_watch_nonexistent_project(self, mock_registry_class):
        """Test watching nonexistent project raises error"""
        mock_registry = MagicMock()
        mock_registry.list_projects.return_value = {}
        mock_registry_class.return_value = mock_registry
        
        with self.assertRaises(ProjectNotFoundError):
            watch_multiple_projects(['nonexistent'])
    
    @patch('pygubuai.multi_watch.Registry')
    def test_watch_all_projects(self, mock_registry_class):
        """Test watching all projects"""
        mock_registry = MagicMock()
        mock_registry.list_projects.return_value = {
            'proj1': str(self.proj1)
        }
        mock_registry_class.return_value = mock_registry
        
        with patch('time.sleep', side_effect=KeyboardInterrupt):
            try:
                watch_all_projects()
            except KeyboardInterrupt:
                pass


if __name__ == '__main__':
    unittest.main()
