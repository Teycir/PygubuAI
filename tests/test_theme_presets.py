"""Tests for theme presets"""
import unittest
from pygubuai.theme_presets import (
    THEME_PRESETS, get_preset, list_presets, validate_preset
)

class TestThemePresets(unittest.TestCase):
    
    def test_all_presets_exist(self):
        """Test all 8 presets are defined"""
        expected = ["modern-dark", "modern-light", "material", "nord",
                   "solarized-dark", "solarized-light", "high-contrast", "dracula"]
        self.assertEqual(set(list_presets()), set(expected))
    
    def test_preset_structure(self):
        """Test each preset has required fields"""
        for name in list_presets():
            preset = get_preset(name)
            self.assertIn("name", preset)
            self.assertIn("description", preset)
            self.assertIn("base", preset)
            self.assertIn("colors", preset)
    
    def test_color_format(self):
        """Test all colors are valid hex"""
        for name in list_presets():
            preset = get_preset(name)
            for color_key, color_value in preset["colors"].items():
                self.assertTrue(color_value.startswith("#"))
                self.assertEqual(len(color_value), 7)
                # Validate hex
                int(color_value[1:], 16)
    
    def test_required_colors(self):
        """Test presets have required colors"""
        required = ["bg", "fg", "accent"]
        for name in list_presets():
            preset = get_preset(name)
            for color in required:
                self.assertIn(color, preset["colors"])
    
    def test_validate_preset(self):
        """Test preset validation"""
        valid = {
            "name": "test",
            "description": "Test theme",
            "base": "clam",
            "colors": {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
        }
        self.assertTrue(validate_preset(valid))
        
        # Missing field
        invalid = valid.copy()
        del invalid["base"]
        self.assertFalse(validate_preset(invalid))
        
        # Invalid color
        invalid = valid.copy()
        invalid["colors"]["bg"] = "white"
        self.assertFalse(validate_preset(invalid))
    
    def test_get_preset(self):
        """Test getting preset by name"""
        preset = get_preset("modern-dark")
        self.assertIsNotNone(preset)
        self.assertEqual(preset["name"], "Modern Dark")
        
        # Non-existent
        self.assertIsNone(get_preset("nonexistent"))

if __name__ == '__main__':
    unittest.main()
