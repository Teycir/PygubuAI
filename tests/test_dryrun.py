"""Tests for dry-run mode."""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.dryrun import (
    enable_dryrun, disable_dryrun, is_dryrun,
    record_operation, get_preview, clear_operations
)


class TestDryRun(unittest.TestCase):
    """Test dry-run functionality."""
    
    def setUp(self):
        clear_operations()
        disable_dryrun()
    
    def test_enable_disable(self):
        """Test enabling/disabling dry-run."""
        self.assertFalse(is_dryrun())
        
        enable_dryrun()
        self.assertTrue(is_dryrun())
        
        disable_dryrun()
        self.assertFalse(is_dryrun())
    
    def test_record_operation(self):
        """Test recording operations."""
        enable_dryrun()
        record_operation("CREATE", "test.py", size="100 bytes")
        
        preview = get_preview()
        self.assertIn("CREATE", preview)
        self.assertIn("test.py", preview)
        self.assertIn("size", preview)
    
    def test_multiple_operations(self):
        """Test recording multiple operations."""
        enable_dryrun()
        record_operation("CREATE", "file1.py")
        record_operation("MODIFY", "file2.py")
        record_operation("DELETE", "file3.py")
        
        preview = get_preview()
        self.assertIn("CREATE", preview)
        self.assertIn("MODIFY", preview)
        self.assertIn("DELETE", preview)
    
    def test_no_operations(self):
        """Test preview with no operations."""
        preview = get_preview()
        self.assertIn("No operations", preview)


if __name__ == "__main__":
    unittest.main()
