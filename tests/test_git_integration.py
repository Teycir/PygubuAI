"""Tests for git integration module"""
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from pygubuai.git_integration import is_git_available, init_git_repo, generate_gitignore, git_commit


class TestGitIntegration(unittest.TestCase):
    """Test git integration functions"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "testproject"
        self.project_path.mkdir()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    @patch('subprocess.run')
    def test_is_git_available_true(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(is_git_available())
    
    @patch('subprocess.run', side_effect=FileNotFoundError)
    def test_is_git_available_false(self, mock_run):
        self.assertFalse(is_git_available())
    
    def test_generate_gitignore(self):
        content = generate_gitignore()
        self.assertIn('__pycache__/', content)
        self.assertIn('.pygubu-workflow.json', content)
        self.assertIn('.DS_Store', content)
    
    @patch('pygubuai.git_integration.is_git_available', return_value=False)
    def test_init_git_repo_no_git(self, mock_available):
        result = init_git_repo(self.project_path)
        self.assertFalse(result)
    
    @patch('pygubuai.git_integration.is_git_available', return_value=True)
    @patch('subprocess.run')
    def test_init_git_repo_success(self, mock_run, mock_available):
        mock_run.return_value = MagicMock(returncode=0)
        result = init_git_repo(self.project_path, initial_commit=False)
        self.assertTrue(result)
        self.assertTrue((self.project_path / '.gitignore').exists())
    
    @patch('pygubuai.git_integration.is_git_available', return_value=True)
    @patch('subprocess.run')
    def test_init_git_repo_with_commit(self, mock_run, mock_available):
        mock_run.return_value = MagicMock(returncode=0)
        result = init_git_repo(self.project_path, initial_commit=True)
        self.assertTrue(result)
        # Verify git commands were called
        self.assertGreaterEqual(mock_run.call_count, 3)  # init, add, commit
    
    @patch('pygubuai.git_integration.is_git_available', return_value=False)
    def test_git_commit_no_git(self, mock_available):
        result = git_commit(self.project_path, "test commit")
        self.assertFalse(result)
    
    @patch('pygubuai.git_integration.is_git_available', return_value=True)
    @patch('subprocess.run')
    def test_git_commit_success(self, mock_run, mock_available):
        mock_run.return_value = MagicMock(returncode=0)
        result = git_commit(self.project_path, "test commit")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
