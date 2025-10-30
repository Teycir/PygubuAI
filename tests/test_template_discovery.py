#!/usr/bin/env python3
"""Tests for template discovery system."""
import unittest
import tempfile
import pathlib
import json
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.template_discovery import TemplateRegistry, get_template_registry

class TestTemplateDiscovery(unittest.TestCase):
    """Test template discovery and validation."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = pathlib.Path(self.temp_dir) / "templates"
        self.template_dir.mkdir()
    
    def test_registry_initialization(self):
        """Test template registry initializes with built-in templates."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        
        self.assertGreater(len(templates), 0)
        template_names = [t[0] for t in templates]
        self.assertIn("login", template_names)
    
    def test_get_template(self):
        """Test getting template by name."""
        registry = TemplateRegistry()
        template = registry.get_template("login")
        
        self.assertIsNotNone(template)
        self.assertIn("description", template)
        self.assertIn("widgets", template)
    
    def test_get_nonexistent_template(self):
        """Test getting non-existent template returns None."""
        registry = TemplateRegistry()
        template = registry.get_template("nonexistent")
        
        self.assertIsNone(template)
    
    def test_validate_template_valid(self):
        """Test validation of valid template."""
        registry = TemplateRegistry()
        valid_template = {
            "description": "Test template",
            "widgets": [
                {"type": "label", "text": "Test", "id": "test_label"}
            ],
            "callbacks": []
        }
        
        self.assertTrue(registry._validate_template(valid_template))
    
    def test_validate_template_missing_description(self):
        """Test validation fails for missing description."""
        registry = TemplateRegistry()
        invalid_template = {
            "widgets": [
                {"type": "label", "text": "Test", "id": "test_label"}
            ]
        }
        
        self.assertFalse(registry._validate_template(invalid_template))
    
    def test_validate_template_missing_widgets(self):
        """Test validation fails for missing widgets."""
        registry = TemplateRegistry()
        invalid_template = {
            "description": "Test template"
        }
        
        self.assertFalse(registry._validate_template(invalid_template))
    
    def test_validate_template_invalid_widget(self):
        """Test validation fails for invalid widget."""
        registry = TemplateRegistry()
        invalid_template = {
            "description": "Test template",
            "widgets": [
                {"type": "invalid_type", "text": "Test", "id": "test"}
            ]
        }
        
        self.assertFalse(registry._validate_template(invalid_template))
    
    def test_register_template(self):
        """Test programmatic template registration."""
        registry = TemplateRegistry()
        new_template = {
            "description": "Custom template",
            "widgets": [
                {"type": "button", "text": "Click", "id": "btn1"}
            ],
            "callbacks": ["on_click"]
        }
        
        result = registry.register_template("custom", new_template)
        self.assertTrue(result)
        
        retrieved = registry.get_template("custom")
        self.assertEqual(retrieved["description"], "Custom template")
    
    def test_register_invalid_template(self):
        """Test registering invalid template fails."""
        registry = TemplateRegistry()
        invalid_template = {
            "description": "Invalid"
        }
        
        result = registry.register_template("invalid", invalid_template)
        self.assertFalse(result)
    
    def test_list_templates_includes_source(self):
        """Test list_templates includes source information."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        
        # Check tuple structure (name, description, source)
        for template in templates:
            self.assertEqual(len(template), 3)
            self.assertIn(template[2], ["built-in", "user"])
    
    def test_global_registry_singleton(self):
        """Test global registry is singleton."""
        registry1 = get_template_registry()
        registry2 = get_template_registry()
        
        self.assertIs(registry1, registry2)

if __name__ == '__main__':
    unittest.main()
