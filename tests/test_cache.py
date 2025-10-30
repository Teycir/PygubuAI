"""Tests for caching system."""
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.cache import get_cached, set_cached, clear_cache, CACHE_DIR


class TestCache(unittest.TestCase):
    """Test caching functionality."""
    
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test.ui"
        self.test_file.write_text("<interface><object class='tk.Frame'/></interface>")
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        clear_cache()
    
    def test_cache_miss(self):
        """Test cache miss returns None."""
        result = get_cached(self.test_file)
        self.assertIsNone(result)
    
    def test_cache_hit(self):
        """Test cache hit returns data."""
        data = {"widgets": ["Button", "Entry"]}
        set_cached(self.test_file, data)
        
        result = get_cached(self.test_file)
        self.assertEqual(result, data)
    
    def test_cache_invalidation(self):
        """Test cache invalidates on file change."""
        data = {"widgets": ["Button"]}
        set_cached(self.test_file, data)
        
        # Modify file
        self.test_file.write_text("<interface><object class='tk.Button'/></interface>")
        
        # Cache should miss
        result = get_cached(self.test_file)
        self.assertIsNone(result)
    
    def test_clear_cache(self):
        """Test clearing cache."""
        set_cached(self.test_file, {"test": "data"})
        clear_cache(self.test_file)
        
        result = get_cached(self.test_file)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
