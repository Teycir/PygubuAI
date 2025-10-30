#!/usr/bin/env python3
"""Tests for error handling"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from pygubuai_errors import ProjectNotFoundError, InvalidProjectError, validate_project_structure

class TestErrors(unittest.TestCase):
    def test_project_not_found_error(self):
        """Test ProjectNotFoundError message"""
        error = ProjectNotFoundError("test_project")
        self.assertIn("test_project", str(error))
        self.assertIn("Suggestion", str(error))
    
    def test_validate_nonexistent_project(self):
        """Test validation of nonexistent project"""
        with self.assertRaises(InvalidProjectError):
            validate_project_structure("/nonexistent/path")
    
    def test_validate_empty_project(self):
        """Test validation of project without .ui files"""
        temp_dir = tempfile.mkdtemp()
        with self.assertRaises(InvalidProjectError):
            validate_project_structure(temp_dir)
    
    def test_validate_valid_project(self):
        """Test validation of valid project"""
        temp_dir = pathlib.Path(tempfile.mkdtemp())
        (temp_dir / "test.ui").write_text("<?xml version='1.0'?>")
        
        self.assertTrue(validate_project_structure(temp_dir))

if __name__ == '__main__':
    unittest.main()
