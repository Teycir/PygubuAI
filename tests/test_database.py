"""Tests for database integration"""
import unittest
import tempfile
import shutil
from pathlib import Path
from pygubuai.database import DatabaseHelper, init_database, add_table
from pygubuai.registry import Registry

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.db_path = self.test_dir / "test.db"
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_database_helper_init(self):
        """Test DatabaseHelper initialization"""
        helper = DatabaseHelper(str(self.db_path))
        self.assertEqual(helper.db_type, 'sqlite')
        self.assertEqual(helper.db_path, str(self.db_path))
    
    def test_create_table(self):
        """Test table creation"""
        helper = DatabaseHelper(str(self.db_path))
        schema = {"name": "str", "age": "int"}
        helper.create_table("users", schema)
        
        # Verify table exists
        conn = helper.connect()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
    
    def test_type_mapping(self):
        """Test Python to SQL type mapping"""
        helper = DatabaseHelper(str(self.db_path))
        self.assertEqual(helper._map_type("str"), "TEXT")
        self.assertEqual(helper._map_type("int"), "INTEGER")
        self.assertEqual(helper._map_type("float"), "REAL")
        self.assertEqual(helper._map_type("bool"), "INTEGER")
    
    def test_generate_crud_code(self):
        """Test CRUD code generation"""
        helper = DatabaseHelper(str(self.db_path))
        schema = {"name": "str", "email": "str"}
        code = helper.generate_crud_code("users", schema)
        
        self.assertIn("def load_users(self):", code)
        self.assertIn("def add_users(self, name, email):", code)
        self.assertIn("def update_users(self, id, name, email):", code)
        self.assertIn("def delete_users(self, id):", code)

class TestDatabaseIntegration(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_name = "test_db_project"
        self.project_dir = self.test_dir / self.project_name
        self.project_dir.mkdir()
        
        py_content = '''#!/usr/bin/env python3
class TestApp:
    def run(self):
        pass
'''
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
    
    def test_init_database(self):
        """Test database initialization"""
        db_path = init_database(self.project_name)
        self.assertTrue(Path(db_path).exists())
    
    def test_add_table_to_project(self):
        """Test adding table to project"""
        init_database(self.project_name)
        schema = {"title": "str", "done": "bool"}
        add_table(self.project_name, "tasks", schema)
        
        # Check database
        db_path = self.project_dir / f"{self.project_name}.db"
        helper = DatabaseHelper(str(db_path))
        conn = helper.connect()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        
        # Check Python file
        py_file = self.project_dir / f"{self.project_name}.py"
        content = py_file.read_text()
        self.assertIn("load_tasks", content)

if __name__ == '__main__':
    unittest.main()
