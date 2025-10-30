#!/usr/bin/env python3
"""Tests for template system"""
import unittest
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import pygubuai_templates

class TestTemplates(unittest.TestCase):
    def test_list_templates(self):
        """Test template listing"""
        templates = pygubuai_templates.list_templates()
        self.assertGreater(len(templates), 0)
        self.assertTrue(any(name == "login" for name, _ in templates))
    
    def test_get_template(self):
        """Test getting specific template"""
        template = pygubuai_templates.get_template("login")
        self.assertIsNotNone(template)
        self.assertIn("widgets", template)
        self.assertIn("callbacks", template)
    
    def test_generate_from_template(self):
        """Test XML generation from template"""
        xml = pygubuai_templates.generate_from_template("login")
        self.assertIsNotNone(xml)
        self.assertIn("<?xml", xml)
        self.assertIn("ttk.Entry", xml)
        self.assertIn("ttk.Button", xml)
    
    def test_generate_callbacks(self):
        """Test callback generation"""
        callbacks = pygubuai_templates.generate_callbacks("login")
        self.assertIn("on_login", callbacks)
    
    def test_crud_template(self):
        """Test CRUD template"""
        template = pygubuai_templates.get_template("crud")
        self.assertIsNotNone(template)
        self.assertTrue(len(template["callbacks"]) >= 3)

if __name__ == '__main__':
    unittest.main()
