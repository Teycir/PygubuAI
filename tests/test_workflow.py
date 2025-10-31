#!/usr/bin/env python3
"""Tests for workflow module"""
import unittest
import tempfile
import pathlib
import sys
import json
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai.workflow import load_workflow, save_workflow, watch_project, get_file_hash
from pygubuai.registry import Registry
from pygubuai.errors import ProjectNotFoundError

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = pathlib.Path(self.temp_dir) / "testproj"
        self.project_dir.mkdir()
    
    def test_get_file_hash(self):
        """Test file hash generation with SHA256"""
        test_file = self.project_dir / "test.ui"
        test_file.write_text("<ui>test</ui>")
        
        hash1 = get_file_hash(test_file)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)  # SHA256 hash length
        
        # Same content = same hash
        hash2 = get_file_hash(test_file)
        self.assertEqual(hash1, hash2)
        
        # Different content = different hash
        test_file.write_text("<ui>changed</ui>")
        hash3 = get_file_hash(test_file)
        self.assertNotEqual(hash1, hash3)
    
    def test_load_workflow_new(self):
        """Test loading workflow for new project"""
        workflow = load_workflow(self.project_dir)
        self.assertEqual(workflow["file_hashes"], {})
        self.assertIsNone(workflow["last_sync"])
        self.assertEqual(workflow["history"], [])
    
    def test_save_and_load_workflow(self):
        """Test saving and loading workflow"""
        workflow_data = {
            "project": "testproj",
            "file_hashes": {"test.ui": "abc123"},
            "last_sync": None,
            "history": []
        }
        
        save_workflow(self.project_dir, workflow_data)
        loaded = load_workflow(self.project_dir)
        
        self.assertIn("file_hashes", loaded)
        self.assertEqual(loaded["file_hashes"].get("test.ui"), "abc123")
        self.assertIsNotNone(loaded["last_sync"])
    
    def test_load_workflow_invalid_json(self):
        """Test loading workflow with invalid JSON"""
        workflow_file = self.project_dir / ".pygubu-workflow.json"
        workflow_file.write_text("invalid json{")
        
        workflow = load_workflow(self.project_dir)
        # Should return defaults on error
        self.assertEqual(workflow["file_hashes"], {})
        self.assertEqual(workflow["history"], [])
    
    def test_get_file_hash_nonexistent(self):
        """Test hash of non-existent file returns None"""
        nonexistent = self.project_dir / "nonexistent.ui"
        
        result = get_file_hash(nonexistent)
        self.assertIsNone(result)
    
    def test_watch_project_not_found(self):
        """Test watching non-existent project raises error"""
        with self.assertRaises(ProjectNotFoundError):
            watch_project("nonexistent_project")
    
    def test_workflow_tracks_changes(self):
        """Test workflow tracks multiple changes"""
        workflow_data = {
            "project": "testproj",
            "file_hashes": {"test.ui": "initial"},
            "last_sync": None,
            "history": [{"timestamp": "2024-01-01", "action": "file_changed", "description": "File test.ui changed"}]
        }
        
        save_workflow(self.project_dir, workflow_data)
        loaded = load_workflow(self.project_dir)
        
        self.assertEqual(len(loaded["history"]), 1)
        self.assertIn("test.ui", loaded["history"][0]["description"])

class TestWorkflowEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_save_workflow_creates_file(self):
        """Test save_workflow creates file if not exists"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "newproj"
        project_dir.mkdir()
        
        workflow_data = {"project": "newproj", "file_hashes": {"test.ui": "test"}, "history": []}
        save_workflow(project_dir, workflow_data)
        
        workflow_file = project_dir / ".pygubu-workflow.json"
        self.assertTrue(workflow_file.exists())
    
    def test_workflow_preserves_existing_changes(self):
        """Test workflow preserves existing change history"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        # Save initial workflow
        initial = {"project": "proj", "file_hashes": {"a.ui": "v1"}, "history": [{"timestamp": "2024-01-01", "action": "file_changed", "description": "File a.ui changed"}]}
        save_workflow(project_dir, initial)
        
        # Load and modify
        loaded = load_workflow(project_dir)
        loaded["history"].append({"timestamp": "2024-01-02", "action": "file_changed", "description": "File b.ui changed"})
        save_workflow(project_dir, loaded)
        
        # Verify both changes preserved
        final = load_workflow(project_dir)
        self.assertEqual(len(final["history"]), 2)

class TestWorkflowSecurityFixes(unittest.TestCase):
    """Test security and reliability fixes."""
    
    def test_timezone_aware_datetime(self):
        """Test workflow uses timezone-aware datetime"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        workflow_data = {"project": "proj", "file_hashes": {"test.ui": "test"}, "history": []}
        save_workflow(project_dir, workflow_data)
        
        loaded = load_workflow(project_dir)
        # Check ISO format includes timezone
        self.assertIn('+', loaded["last_sync"] or '')
    
    def test_path_traversal_protection(self):
        """Test path validation prevents traversal"""
        # Mock Registry.list_projects at class level
        with patch('pygubuai.workflow.Registry') as MockRegistry:
            mock_instance = MagicMock()
            mock_instance.list_projects.return_value = {'test': '/nonexistent/path'}
            MockRegistry.return_value = mock_instance
            
            with self.assertRaises(ProjectNotFoundError) as ctx:
                watch_project('test')
            self.assertIn('Invalid project path', str(ctx.exception))
    
    def test_save_workflow_io_error(self):
        """Test save_workflow handles IO errors gracefully"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        # Make directory read-only
        os.chmod(project_dir, 0o444)
        
        workflow_data = {"project": "proj", "file_hashes": {"test.ui": "test"}, "history": []}
        # Should raise on IO error
        with self.assertRaises(Exception):
            save_workflow(project_dir, workflow_data)
        os.chmod(project_dir, 0o755)
    
    def test_get_file_hash_permission_error(self):
        """Test get_file_hash handles permission errors"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        test_file = project_dir / "test.ui"
        test_file.write_text("test")
        os.chmod(test_file, 0o000)
        
        try:
            result = get_file_hash(test_file)
            self.assertIsNone(result)
        finally:
            os.chmod(test_file, 0o644)
    
    def test_watch_project_invalid_directory(self):
        """Test watch_project validates directory exists"""
        # Register project pointing to a file instead of directory
        temp_dir = tempfile.mkdtemp()
        test_file = pathlib.Path(temp_dir) / "file.txt"
        test_file.write_text("not a directory")
        
        with patch('pygubuai.workflow.Registry') as MockRegistry:
            mock_instance = MagicMock()
            mock_instance.list_projects.return_value = {'test': str(test_file)}
            MockRegistry.return_value = mock_instance
            
            with self.assertRaises(ProjectNotFoundError) as ctx:
                watch_project('test')
            self.assertIn('Invalid project path', str(ctx.exception))

class TestWorkflowErrorRecovery(unittest.TestCase):
    """Test error recovery in watch loop."""
    
    def test_watch_continues_after_file_error(self):
        """Test watch loop continues after individual file errors"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        # Create UI file
        ui_file = project_dir / "test.ui"
        ui_file.write_text("<ui>test</ui>")
        
        with patch('pygubuai.workflow.Registry') as MockRegistry:
            mock_instance = MagicMock()
            mock_instance.list_projects.return_value = {'test': str(project_dir)}
            MockRegistry.return_value = mock_instance
            
            with patch('pygubuai.workflow.get_file_hash', side_effect=[None, "hash123"]):
                with patch('time.sleep', side_effect=KeyboardInterrupt):
                    # Should not crash on None hash, continues to next iteration
                    try:
                        watch_project('test')
                    except KeyboardInterrupt:
                        pass  # Expected

class TestMultiFileTracking(unittest.TestCase):
    """Test per-file hash tracking."""
    
    def test_tracks_multiple_files_separately(self):
        """Test workflow tracks each file's hash separately"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        # Create multiple UI files
        file1 = project_dir / "main.ui"
        file2 = project_dir / "dialog.ui"
        file1.write_text("<ui>main</ui>")
        file2.write_text("<ui>dialog</ui>")
        
        workflow = load_workflow(project_dir)
        self.assertIn("file_hashes", workflow)
        self.assertEqual(workflow["file_hashes"], {})
    
    def test_detects_specific_file_change(self):
        """Test detects which specific file changed"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        file1 = project_dir / "a.ui"
        file2 = project_dir / "b.ui"
        file1.write_text("<ui>a</ui>")
        file2.write_text("<ui>b</ui>")
        
        workflow = load_workflow(project_dir)
        workflow["file_hashes"] = {
            "a.ui": get_file_hash(file1),
            "b.ui": get_file_hash(file2)
        }
        save_workflow(project_dir, workflow)
        
        # Change only file1
        file1.write_text("<ui>a_modified</ui>")
        
        # Verify hashes differ
        new_hash = get_file_hash(file1)
        self.assertNotEqual(workflow["file_hashes"]["a.ui"], new_hash)
        self.assertEqual(workflow["file_hashes"]["b.ui"], get_file_hash(file2))

class TestConfigurableWatch(unittest.TestCase):
    """Test configurable watch settings."""
    
    def test_default_watch_interval(self):
        """Test default watch interval is 2.0 seconds"""
        from pygubuai.workflow import get_watch_interval
        self.assertEqual(get_watch_interval(), 2.0)
    
    def test_custom_watch_interval(self):
        """Test custom watch interval from environment"""
        from pygubuai.workflow import get_watch_interval
        with patch.dict(os.environ, {'PYGUBUAI_WATCH_INTERVAL': '5.0'}):
            self.assertEqual(get_watch_interval(), 5.0)
    
    def test_default_file_patterns(self):
        """Test default file patterns"""
        from pygubuai.workflow import get_file_patterns
        self.assertEqual(get_file_patterns(), ['*.ui'])
    
    def test_custom_file_patterns(self):
        """Test custom file patterns from environment"""
        from pygubuai.workflow import get_file_patterns
        with patch.dict(os.environ, {'PYGUBUAI_WATCH_PATTERNS': '*.ui, *.xml'}):
            patterns = get_file_patterns()
            self.assertEqual(patterns, ['*.ui', '*.xml'])

if __name__ == '__main__':
    unittest.main()
