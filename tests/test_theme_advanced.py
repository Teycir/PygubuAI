"""Tests for advanced theme engine"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.theme_advanced import apply_preset, apply_colors_to_widget
from pygubuai.registry import Registry
import xml.etree.ElementTree as ET

class TestThemeAdvanced(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "test_theme_project"
        self.project_dir = self.test_dir / self.project_name
        self.project_dir.mkdir()
        
        # Create minimal UI file
        ui_content = '''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Test</property>
    <child>
      <object class="ttk.Frame" id="frame1">
        <child>
          <object class="ttk.Button" id="button1">
            <property name="text">Click</property>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>'''
        
        ui_file = self.project_dir / f"{self.project_name}.ui"
        ui_file.write_text(ui_content)
        
        # Register project
        registry = Registry()
        registry.add_project(self.project_name, str(self.project_dir))
    
    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        registry = Registry()
        try:
            registry.remove_project(self.project_name)
        except:
            pass
    
    def test_apply_preset(self):
        """Test applying preset to project"""
        result = apply_preset(self.project_name, "modern-dark", backup=True)
        self.assertTrue(result)
        
        # Check backup created
        backup = self.project_dir / f"{self.project_name}.ui.bak"
        self.assertTrue(backup.exists())
        
        # Check theme applied
        ui_file = self.project_dir / f"{self.project_name}.ui"
        tree = ET.parse(ui_file)
        root = tree.getroot()
        theme_prop = root.find(".//property[@name='theme']")
        self.assertIsNotNone(theme_prop)
        self.assertEqual(theme_prop.text, "clam")
    
    def test_apply_preset_invalid(self):
        """Test applying invalid preset"""
        with self.assertRaises(ValueError):
            apply_preset(self.project_name, "nonexistent")
    
    def test_apply_preset_no_project(self):
        """Test applying to non-existent project"""
        with self.assertRaises(ValueError):
            apply_preset("nonexistent", "modern-dark")
    
    def test_apply_colors_to_widget(self):
        """Test color application to widget"""
        widget = ET.Element("object", {"class": "ttk.Button"})
        colors = {"button_bg": "#0e639c", "button_fg": "#ffffff"}
        
        apply_colors_to_widget(widget, colors, "ttk.Button")
        
        bg_prop = widget.find("property[@name='background']")
        self.assertIsNotNone(bg_prop)
        self.assertEqual(bg_prop.text, "#0e639c")

if __name__ == '__main__':
    unittest.main()
