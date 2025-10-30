#!/usr/bin/env python3
"""Tests for template system"""
import unittest
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))
from pygubuai import templates as pygubuai_templates

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
    
    def test_get_template_widgets_and_callbacks(self):
        """Test extracting widgets and callbacks from template"""
        widgets, callbacks = pygubuai_templates.get_template_widgets_and_callbacks("login")
        self.assertGreater(len(widgets), 0)
        self.assertIn("on_login", callbacks)
    
    def test_crud_template(self):
        """Test CRUD template"""
        template = pygubuai_templates.get_template("crud")
        self.assertIsNotNone(template)
        self.assertTrue(len(template["callbacks"]) >= 3)

if __name__ == '__main__':
    unittest.main()
