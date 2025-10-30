"""Tests for data export functionality"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.data_export import add_export_capability, _create_export_method, generate_treeview_export
from pygubuai.registry import Registry

class TestDataExport(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "test_export"
        self.project_dir = self.test_dir / self.project_name
        self.project_dir.mkdir()
        
        # Create minimal files
        ui_content = '''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <child>
      <object class="ttk.Frame" id="mainframe"/>
    </child>
  </object>
</interface>'''
        
        py_content = '''#!/usr/bin/env python3
class TestApp:
    def __init__(self):
        pass
    
    def run(self):
        pass
'''
        
        (self.project_dir / f"{self.project_name}.ui").write_text(ui_content)
        (self.project_dir / f"{self.project_name}.py").write_text(py_content)
        
        registry = Registry()
        registry.add_project(self.project_name, str(self.project_dir))
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        registry = Registry()
        try:
            registry.remove_project(self.project_name)
        except:
            pass
    
    def test_create_export_method(self):
        """Test export method generation"""
        method = _create_export_method(["csv", "json"])
        self.assertIn("def on_export(self):", method)
        self.assertIn("_export_csv", method)
        self.assertIn("_export_json", method)
    
    def test_generate_treeview_export(self):
        """Test Treeview export code generation"""
        code = generate_treeview_export("my_tree")
        self.assertIn("def _get_export_data(self):", code)
        self.assertIn("my_tree", code)
        self.assertIn("get_children", code)
    
    def test_add_export_capability(self):
        """Test adding export to project"""
        result = add_export_capability(self.project_name, ["csv", "json"])
        self.assertTrue(result)
        
        # Check Python file modified
        py_file = self.project_dir / f"{self.project_name}.py"
        content = py_file.read_text()
        self.assertIn("on_export", content)

if __name__ == '__main__':
    unittest.main()
