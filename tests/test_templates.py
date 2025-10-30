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
    
    def test_invalid_template_name(self):
        """Test requesting non-existent template raises error"""
        with self.assertRaises(ValueError) as ctx:
            pygubuai_templates.get_template_widgets_and_callbacks("nonexistent")
        self.assertIn("not found", str(ctx.exception))
    
    def test_validate_widget_missing_type(self):
        """Test validation catches missing type field"""
        with self.assertRaises(ValueError) as ctx:
            pygubuai_templates.validate_widget({"id": "test"})
        self.assertIn("missing 'type'", str(ctx.exception))
    
    def test_validate_widget_invalid_type(self):
        """Test validation catches invalid widget type"""
        with self.assertRaises(ValueError) as ctx:
            pygubuai_templates.validate_widget({"type": "invalid_widget", "id": "test"})
        self.assertIn("Unknown widget type", str(ctx.exception))
    
    def test_validate_widget_missing_id(self):
        """Test validation catches missing id field"""
        with self.assertRaises(ValueError) as ctx:
            pygubuai_templates.validate_widget({"type": "label"})
        self.assertIn("missing 'id'", str(ctx.exception))
    
    def test_expanded_widget_map(self):
        """Test new widgets are in WIDGET_MAP"""
        new_widgets = ["radiobutton", "progressbar", "scale", "scrollbar", "separator", "spinbox"]
        for widget in new_widgets:
            self.assertIn(widget, pygubuai_templates.WIDGET_MAP)
    
    def test_widget_properties_preserved(self):
        """Test widget properties are correctly preserved"""
        widgets, _ = pygubuai_templates.get_template_widgets_and_callbacks("login")
        password_entry = next((w for w in widgets if w[1]["id"] == "password_entry"), None)
        self.assertIsNotNone(password_entry)
        self.assertEqual(password_entry[1]["properties"]["show"], "*")
    
    def test_callback_generation_format(self):
        """Test callback code has proper format"""
        _, callbacks = pygubuai_templates.get_template_widgets_and_callbacks("settings")
        self.assertIn('def on_save(self):', callbacks)
        self.assertIn('"""Handle on_save event."""', callbacks)
        self.assertIn('pass', callbacks)

if __name__ == '__main__':
    unittest.main()
