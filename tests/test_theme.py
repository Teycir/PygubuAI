#!/usr/bin/env python3
"""Tests for theme module"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.theme import apply_theme, get_current_theme, list_themes
from pygubuai.registry import Registry

class TestTheme(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = pathlib.Path(self.temp_dir) / ".pygubu-registry.json"
        Registry.REGISTRY_FILE = self.registry_file
        
        # Create test project
        self.project_dir = pathlib.Path(self.temp_dir) / "testapp"
        self.project_dir.mkdir()
        
        self.ui_file = self.project_dir / "testapp.ui"
        self.ui_file.write_text("""<?xml version='1.0' encoding='utf-8'?>
<interface>
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Test</property>
  </object>
</interface>""")
        
        registry = Registry()
        registry.add_project("testapp", str(self.project_dir))
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        Registry.REGISTRY_FILE = None
    
    def test_list_themes(self):
        """Test listing available themes"""
        themes = list_themes()
        self.assertIn("clam", themes)
        self.assertIn("default", themes)
    
    def test_apply_theme(self):
        """Test applying theme"""
        result = apply_theme("testapp", "clam")
        self.assertTrue(result)
        
        # Verify backup created
        backup = self.ui_file.with_suffix('.ui.bak')
        self.assertTrue(backup.exists())
    
    def test_get_current_theme(self):
        """Test getting current theme"""
        apply_theme("testapp", "clam", backup=False)
        theme = get_current_theme("testapp")
        self.assertEqual(theme, "clam")

if __name__ == '__main__':
    unittest.main()
