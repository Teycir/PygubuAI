"""Tests for backup module"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.backup import create_backup, restore_backup, list_backups


class TestBackup(unittest.TestCase):
    """Test backup functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = Path(self.temp_dir) / "testproject"
        self.project_dir.mkdir()
        (self.project_dir / "test.ui").write_text("<ui>test</ui>")
        (self.project_dir / "test.py").write_text("print('test')")
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_backup(self):
        """Test creating backup"""
        backup_path = create_backup(self.project_dir)
        self.assertIsNotNone(backup_path)
        self.assertTrue(backup_path.exists())
        self.assertTrue((backup_path / "test.ui").exists())
        self.assertTrue((backup_path / "test.py").exists())
    
    def test_create_backup_nonexistent(self):
        """Test backup of nonexistent project"""
        result = create_backup(Path("/nonexistent"))
        self.assertIsNone(result)
    
    def test_restore_backup(self):
        """Test restoring from backup"""
        backup_path = create_backup(self.project_dir)
        
        # Modify original
        (self.project_dir / "test.ui").write_text("<ui>modified</ui>")
        
        # Restore
        success = restore_backup(backup_path, self.project_dir)
        self.assertTrue(success)
        
        # Verify restored
        content = (self.project_dir / "test.ui").read_text()
        self.assertEqual(content, "<ui>test</ui>")
    
    def test_list_backups(self):
        """Test listing backups"""
        import time
        create_backup(self.project_dir)
        time.sleep(0.01)  # Ensure different timestamps
        create_backup(self.project_dir)
        
        backups = list_backups("testproject", Path(self.temp_dir) / ".pygubuai_backups")
        self.assertGreaterEqual(len(backups), 1)  # At least one backup created


if __name__ == '__main__':
    unittest.main()
