#!/usr/bin/env python3
"""Tests for error handling"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai.errors import ProjectNotFoundError, InvalidProjectError

class TestErrors(unittest.TestCase):
    def test_project_not_found_error(self):
        """Test ProjectNotFoundError message"""
        error = ProjectNotFoundError("test_project", "use pygubu-register")
        self.assertIn("test_project", str(error))
    
    def test_invalid_project_error(self):
        """Test InvalidProjectError message"""
        error = InvalidProjectError("/test/path", "no .ui files")
        self.assertIn("/test/path", str(error))
        self.assertIn("no .ui files", str(error))

if __name__ == '__main__':
    unittest.main()
