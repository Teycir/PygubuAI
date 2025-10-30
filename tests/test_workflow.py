#!/usr/bin/env python3
"""Tests for workflow module"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai.workflow import get_file_hash, load_workflow, save_workflow
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

if __name__ == '__main__':
    unittest.main()
