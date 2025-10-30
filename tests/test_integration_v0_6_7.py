"""Integration tests for v0.6-0.7 features"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.create import create_project
from pygubuai.theme_advanced import apply_preset
from pygubuai.data_export import add_export_capability
from pygubuai.database import init_database, add_table
from pygubuai.registry import Registry

class TestFeatureIntegration(unittest.TestCase):
    """Test all new features working together"""
    
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "integration_test"
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        registry = Registry()
        try:
            registry.remove_project(self.project_name)
        except:
            pass
    
    def test_complete_workflow(self):
        """Test: Create project -> Apply theme -> Add DB -> Add export"""
        
        # 1. Create project manually for testing
        project_path = self.test_dir / self.project_name
        project_path.mkdir()
        
        # Create minimal UI file
        ui_content = '''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <child>
      <object class="ttk.Frame" id="mainframe"/>
    </child>
  </object>
</interface>'''
        (project_path / f"{self.project_name}.ui").write_text(ui_content)
        
        # Create minimal Python file
        py_content = '''#!/usr/bin/env python3
class TestApp:
    def run(self):
        pass
'''
        (project_path / f"{self.project_name}.py").write_text(py_content)
        
        # Register project
        registry = Registry()
        registry.add_project(self.project_name, str(project_path))
        
        self.assertTrue(project_path.exists())
        self.assertTrue((project_path / f"{self.project_name}.ui").exists())
        self.assertTrue((project_path / f"{self.project_name}.py").exists())
        
        # 2. Apply theme
        apply_preset(self.project_name, "modern-dark")
        
        ui_content = (project_path / f"{self.project_name}.ui").read_text()
        self.assertIn("clam", ui_content)  # Base theme
        
        # 3. Initialize database
        db_path = init_database(self.project_name)
        self.assertTrue(Path(db_path).exists())
        
        # 4. Add table
        schema = {"name": "str", "email": "str"}
        add_table(self.project_name, "users", schema)
        
        py_content = (project_path / f"{self.project_name}.py").read_text()
        self.assertIn("load_users", py_content)
        self.assertIn("add_users", py_content)
        
        # 5. Add export capability
        add_export_capability(self.project_name, ["csv", "json"])
        
        py_content = (project_path / f"{self.project_name}.py").read_text()
        self.assertIn("on_export", py_content)
        self.assertIn("_export_csv", py_content)
    
    def test_theme_with_crud_template(self):
        """Test: CRUD template -> Theme -> Database"""
        
        # Create project manually
        project_path = self.test_dir / self.project_name
        project_path.mkdir()
        
        ui_content = '''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <child>
      <object class="ttk.Frame" id="mainframe"/>
    </child>
  </object>
</interface>'''
        (project_path / f"{self.project_name}.ui").write_text(ui_content)
        
        py_content = '''#!/usr/bin/env python3
class TestApp:
    def on_add(self):
        pass
    def on_update(self):
        pass
    def on_delete(self):
        pass
    def run(self):
        pass
'''
        (project_path / f"{self.project_name}.py").write_text(py_content)
        
        registry = Registry()
        registry.add_project(self.project_name, str(project_path))
        
        self.assertTrue(project_path.exists())
        
        # Apply theme
        apply_preset(self.project_name, "material")
        
        # Add database
        init_database(self.project_name)
        add_table(self.project_name, "items", {"name": "str", "value": "int"})
        
        # Verify all components
        py_file = project_path / f"{self.project_name}.py"
        content = py_file.read_text()
        
        # Has CRUD callbacks
        self.assertIn("on_add", content)
        self.assertIn("on_update", content)
        self.assertIn("on_delete", content)
        
        # Has database methods
        self.assertIn("load_items", content)
        self.assertIn("add_items", content)
    
    def test_multiple_themes(self):
        """Test: Apply multiple themes to same project"""
        project_path = self.test_dir / self.project_name
        project_path.mkdir()
        
        ui_content = '''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <child>
      <object class="ttk.Frame" id="mainframe"/>
    </child>
  </object>
</interface>'''
        (project_path / f"{self.project_name}.ui").write_text(ui_content)
        
        py_content = '''#!/usr/bin/env python3
class TestApp:
    def run(self):
        pass
'''
        (project_path / f"{self.project_name}.py").write_text(py_content)
        
        registry = Registry()
        registry.add_project(self.project_name, str(project_path))
        
        # Apply different themes
        themes = ["modern-dark", "modern-light", "material", "nord"]
        
        for theme in themes:
            apply_preset(self.project_name, theme, backup=True)
            
            # Verify backup exists
            backup = project_path / f"{self.project_name}.ui.bak"
            self.assertTrue(backup.exists())
    
    def test_export_with_database(self):
        """Test: Database + Export integration"""
        project_path = self.test_dir / self.project_name
        project_path.mkdir()
        
        ui_content = '''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <child>
      <object class="ttk.Frame" id="mainframe"/>
    </child>
  </object>
</interface>'''
        (project_path / f"{self.project_name}.ui").write_text(ui_content)
        
        py_content = '''#!/usr/bin/env python3
class TestApp:
    def run(self):
        pass
'''
        (project_path / f"{self.project_name}.py").write_text(py_content)
        
        registry = Registry()
        registry.add_project(self.project_name, str(project_path))
        
        # Add database
        init_database(self.project_name)
        add_table(self.project_name, "records", {"field1": "str", "field2": "int"})
        
        # Add export
        add_export_capability(self.project_name, ["csv", "json"])
        
        py_file = project_path / f"{self.project_name}.py"
        content = py_file.read_text()
        
        # Has both DB and export methods
        self.assertIn("load_records", content)
        self.assertIn("on_export", content)
        self.assertIn("_export_csv", content)

class TestThemePresetQuality(unittest.TestCase):
    """Test theme preset quality and consistency"""
    
    def test_all_presets_have_consistent_colors(self):
        """Test all presets have required color keys"""
        from pygubuai.theme_presets import list_presets, get_preset
        
        required_keys = ["bg", "fg", "accent"]
        
        for preset_name in list_presets():
            preset = get_preset(preset_name)
            colors = preset["colors"]
            
            for key in required_keys:
                self.assertIn(key, colors, f"{preset_name} missing {key}")
    
    def test_contrast_ratios(self):
        """Test basic contrast between bg and fg"""
        from pygubuai.theme_presets import list_presets, get_preset
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def luminance(rgb):
            r, g, b = [x / 255.0 for x in rgb]
            return 0.299 * r + 0.587 * g + 0.114 * b
        
        for preset_name in list_presets():
            preset = get_preset(preset_name)
            colors = preset["colors"]
            
            bg_rgb = hex_to_rgb(colors["bg"])
            fg_rgb = hex_to_rgb(colors["fg"])
            
            bg_lum = luminance(bg_rgb)
            fg_lum = luminance(fg_rgb)
            
            # Basic contrast check (not WCAG, just sanity)
            contrast = abs(bg_lum - fg_lum)
            self.assertGreater(contrast, 0.3, f"{preset_name} has poor contrast")

class TestDatabaseOperations(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.db_path = self.test_dir / "test.db"
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_crud_operations(self):
        """Test basic CRUD operations"""
        from pygubuai.database import DatabaseHelper
        
        helper = DatabaseHelper(str(self.db_path))
        
        # Create table
        schema = {"name": "str", "age": "int"}
        helper.create_table("users", schema)
        
        # Insert data
        conn = helper.connect()
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
        conn.commit()
        
        # Read data
        cursor = conn.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 2)
        
        # Update data
        conn.execute("UPDATE users SET age = ? WHERE name = ?", (31, "Alice"))
        conn.commit()
        
        cursor = conn.execute("SELECT age FROM users WHERE name = ?", ("Alice",))
        age = cursor.fetchone()[0]
        self.assertEqual(age, 31)
        
        # Delete data
        conn.execute("DELETE FROM users WHERE name = ?", ("Bob",))
        conn.commit()
        
        cursor = conn.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
