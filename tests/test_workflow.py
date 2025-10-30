#!/usr/bin/env python3
"""Tests for workflow module"""
import unittest
import tempfile
import pathlib
import sys
import json
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai.workflow import get_file_hash, load_workflow, save_workflow, watch_project
from pygubuai.registry import Registry
from pygubuai.errors import ProjectNotFoundError

class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = pathlib.Path(self.temp_dir) / "testproj"
        self.project_dir.mkdir()
    
    def test_get_file_hash(self):
        """Test file hash generation"""
        test_file = self.project_dir / "test.ui"
        test_file.write_text("<ui>test</ui>")
        
        hash1 = get_file_hash(test_file)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 32)  # MD5 hash length
        
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
        self.assertIsNone(workflow["ui_hash"])
        self.assertIsNone(workflow["last_sync"])
        self.assertEqual(workflow["changes"], [])
    
    def test_save_and_load_workflow(self):
        """Test saving and loading workflow"""
        workflow_data = {
            "ui_hash": "abc123",
            "last_sync": None,
            "changes": []
        }
        
        save_workflow(self.project_dir, workflow_data)
        loaded = load_workflow(self.project_dir)
        
        self.assertEqual(loaded["ui_hash"], "abc123")
        self.assertIsNotNone(loaded["last_sync"])
    
    def test_load_workflow_invalid_json(self):
        """Test loading workflow with invalid JSON"""
        workflow_file = self.project_dir / ".pygubu-workflow.json"
        workflow_file.write_text("invalid json{")
        
        workflow = load_workflow(self.project_dir)
        # Should return defaults on error
        self.assertIsNone(workflow["ui_hash"])
        self.assertEqual(workflow["changes"], [])
    
    def test_get_file_hash_nonexistent(self):
        """Test hash of non-existent file raises error"""
        nonexistent = self.project_dir / "nonexistent.ui"
        
        with self.assertRaises(OSError):
            get_file_hash(nonexistent)
    
    def test_watch_project_not_found(self):
        """Test watching non-existent project raises error"""
        with self.assertRaises(ProjectNotFoundError):
            watch_project("nonexistent_project")
    
    def test_workflow_tracks_changes(self):
        """Test workflow tracks multiple changes"""
        workflow_data = {
            "ui_hash": "initial",
            "last_sync": None,
            "changes": [{"file": "test.ui", "timestamp": "2024-01-01"}]
        }
        
        save_workflow(self.project_dir, workflow_data)
        loaded = load_workflow(self.project_dir)
        
        self.assertEqual(len(loaded["changes"]), 1)
        self.assertEqual(loaded["changes"][0]["file"], "test.ui")

class TestWorkflowEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_save_workflow_creates_file(self):
        """Test save_workflow creates file if not exists"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "newproj"
        project_dir.mkdir()
        
        workflow_data = {"ui_hash": "test", "changes": []}
        save_workflow(project_dir, workflow_data)
        
        workflow_file = project_dir / ".pygubu-workflow.json"
        self.assertTrue(workflow_file.exists())
    
    def test_workflow_preserves_existing_changes(self):
        """Test workflow preserves existing change history"""
        temp_dir = tempfile.mkdtemp()
        project_dir = pathlib.Path(temp_dir) / "proj"
        project_dir.mkdir()
        
        # Save initial workflow
        initial = {"ui_hash": "v1", "changes": [{"file": "a.ui"}]}
        save_workflow(project_dir, initial)
        
        # Load and modify
        loaded = load_workflow(project_dir)
        loaded["changes"].append({"file": "b.ui"})
        save_workflow(project_dir, loaded)
        
        # Verify both changes preserved
        final = load_workflow(project_dir)
        self.assertEqual(len(final["changes"]), 2)

if __name__ == '__main__':
    unittest.main()
