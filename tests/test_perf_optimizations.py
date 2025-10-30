#!/usr/bin/env python3
"""Tests for performance optimizations in v0.4.2"""
import unittest
import tempfile
import time
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.registry import Registry
from pygubuai.workflow import get_file_hash_if_changed, load_workflow, save_workflow
from pygubuai.cache import cleanup_old_cache, CACHE_DIR


class TestRegistryCaching(unittest.TestCase):
    """Test lazy loading cache in registry"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = Path(self.temp_dir) / "registry.json"
        Registry.REGISTRY_FILE = self.registry_file
    
    def test_registry_caches_reads(self):
        """Registry should cache reads for TTL period"""
        registry = Registry()
        registry.add_project("test", "/tmp/test", "Test project")
        
        # First read
        start = time.time()
        projects1 = registry.list_projects()
        time1 = time.time() - start
        
        # Second read (should be cached)
        start = time.time()
        projects2 = registry.list_projects()
        time2 = time.time() - start
        
        self.assertEqual(projects1, projects2)
        # Cached read should be significantly faster
        self.assertLess(time2, time1 * 0.5)  # At least 2x faster
    
    def test_registry_invalidates_cache_on_write(self):
        """Cache should be invalidated after write"""
        registry = Registry()
        registry.add_project("test1", "/tmp/test1")
        
        # Read to populate cache
        projects1 = registry.list_projects()
        self.assertIn("test1", projects1)
        
        # Write should invalidate cache
        registry.add_project("test2", "/tmp/test2")
        
        # Next read should see new data
        projects2 = registry.list_projects()
        self.assertIn("test1", projects2)
        self.assertIn("test2", projects2)
    
    def test_registry_cache_expires(self):
        """Cache should expire after TTL"""
        registry = Registry()
        registry._cache_ttl = 0.1  # 100ms TTL for testing
        registry.add_project("test", "/tmp/test")
        
        # Read to populate cache
        projects1 = registry.list_projects()
        
        # Wait for cache to expire
        time.sleep(0.15)
        
        # Modify file directly (bypass cache)
        data = json.loads(self.registry_file.read_text())
        data["projects"]["test2"] = {"path": "/tmp/test2"}
        self.registry_file.write_text(json.dumps(data))
        
        # Should read fresh data
        projects2 = registry.list_projects()
        self.assertIn("test2", projects2)


class TestMtimeOptimization(unittest.TestCase):
    """Test mtime-based hash optimization"""
    
    def test_skips_hashing_if_mtime_unchanged(self):
        """Should return cached hash if mtime unchanged"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            filepath = Path(f.name)
        
        try:
            # First call - should hash
            hash1, mtime1 = get_file_hash_if_changed(filepath, None, None)
            self.assertIsNotNone(hash1)
            self.assertIsNotNone(mtime1)
            
            # Second call with same mtime - should skip hashing
            hash2, mtime2 = get_file_hash_if_changed(filepath, hash1, mtime1)
            self.assertEqual(hash1, hash2)
            self.assertEqual(mtime1, mtime2)
        finally:
            filepath.unlink()
    
    def test_rehashes_if_mtime_changed(self):
        """Should rehash if mtime changed"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("original")
            filepath = Path(f.name)
        
        try:
            # First hash
            hash1, mtime1 = get_file_hash_if_changed(filepath, None, None)
            
            # Modify file
            time.sleep(0.01)  # Ensure mtime changes
            filepath.write_text("modified")
            
            # Should detect change and rehash
            hash2, mtime2 = get_file_hash_if_changed(filepath, hash1, mtime1)
            self.assertNotEqual(hash1, hash2)
            self.assertNotEqual(mtime1, mtime2)
        finally:
            filepath.unlink()
    
    def test_workflow_stores_mtimes(self):
        """Workflow should store mtimes for optimization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            
            # Create workflow with mtime
            workflow = {
                "file_hashes": {"test.ui": "abc123"},
                "file_mtimes": {"test.ui": 1234567890.0},
                "changes": []
            }
            save_workflow(project_path, workflow)
            
            # Load and verify
            loaded = load_workflow(project_path)
            self.assertIn("file_mtimes", loaded)
            self.assertEqual(loaded["file_mtimes"]["test.ui"], 1234567890.0)


class TestCacheCleanup(unittest.TestCase):
    """Test cache cleanup functionality"""
    
    def setUp(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def test_removes_old_files(self):
        """Should remove files older than max_age_days"""
        # Create old file
        old_file = CACHE_DIR / "old_cache.json"
        old_file.write_text("{}")
        
        # Set mtime to 31 days ago
        old_time = time.time() - (31 * 86400)
        old_file.touch()
        import os
        os.utime(old_file, (old_time, old_time))
        
        # Run cleanup
        cleanup_old_cache(max_age_days=30, max_files=1000)
        
        # Old file should be removed
        self.assertFalse(old_file.exists())
    
    def test_limits_file_count(self):
        """Should limit total number of cache files"""
        # Create 105 files
        files = []
        for i in range(105):
            f = CACHE_DIR / f"cache_{i}.json"
            f.write_text("{}")
            files.append(f)
            time.sleep(0.001)  # Ensure different mtimes
        
        # Run cleanup with max 100 files
        cleanup_old_cache(max_age_days=365, max_files=100)
        
        # Should have at most 100 files
        remaining = list(CACHE_DIR.glob("*.json"))
        self.assertLessEqual(len(remaining), 100)
        
        # Cleanup
        for f in remaining:
            f.unlink()
    
    def test_handles_missing_cache_dir(self):
        """Should handle missing cache directory gracefully"""
        import shutil
        if CACHE_DIR.exists():
            shutil.rmtree(CACHE_DIR)
        
        # Should not raise
        cleanup_old_cache()


if __name__ == '__main__':
    unittest.main()
