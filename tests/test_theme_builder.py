"""Tests for custom theme builder"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.theme_builder import (
    create_custom_theme, save_theme, load_theme, 
    list_custom_themes, export_theme, import_theme, get_themes_dir
)

class TestThemeBuilder(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.original_home = Path.home()
        self.test_dir = Path(tempfile.mkdtemp())
        # Mock themes directory
        self.themes_dir = self.test_dir / ".pygubuai" / "themes"
        self.themes_dir.mkdir(parents=True)
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_create_custom_theme(self):
        """Test creating custom theme"""
        colors = {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
        theme = create_custom_theme("test-theme", colors=colors)
        
        self.assertEqual(theme["name"], "test-theme")
        self.assertEqual(theme["colors"], colors)
    
    def test_save_and_load_theme(self):
        """Test saving and loading theme"""
        theme_data = {
            "name": "test",
            "description": "Test theme",
            "base": "clam",
            "colors": {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
        }
        
        save_theme("test", theme_data)
        loaded = load_theme("test")
        
        self.assertEqual(loaded["name"], "test")
        self.assertEqual(loaded["colors"], theme_data["colors"])
    
    def test_list_custom_themes(self):
        """Test listing custom themes"""
        # Create some themes
        for name in ["theme1", "theme2", "theme3"]:
            theme_data = {
                "name": name,
                "description": f"Theme {name}",
                "base": "clam",
                "colors": {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
            }
            save_theme(name, theme_data)
        
        themes = list_custom_themes()
        self.assertGreaterEqual(len(themes), 3)
        self.assertIn("theme1", themes)
    
    def test_export_theme(self):
        """Test exporting theme"""
        theme_data = {
            "name": "export-test",
            "description": "Export test",
            "base": "clam",
            "colors": {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
        }
        save_theme("export-test", theme_data)
        
        output_file = self.test_dir / "exported.json"
        export_theme("export-test", str(output_file))
        
        self.assertTrue(output_file.exists())
    
    def test_import_theme(self):
        """Test importing theme"""
        import json
        
        theme_data = {
            "name": "imported",
            "description": "Imported theme",
            "base": "clam",
            "colors": {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
        }
        
        import_file = self.test_dir / "import.json"
        with open(import_file, 'w') as f:
            json.dump(theme_data, f)
        
        name = import_theme(str(import_file))
        self.assertEqual(name, "imported")
        
        loaded = load_theme("imported")
        self.assertIsNotNone(loaded)

if __name__ == '__main__':
    unittest.main()
