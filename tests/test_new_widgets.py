#!/usr/bin/env python3
"""Tests for enhanced widgets module"""
import unittest
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.widgets import list_widgets, search_widgets, get_widget_info
from pygubuai.widget_data import WIDGET_LIBRARY, CATEGORIES

class TestWidgetBrowser(unittest.TestCase):
    def test_list_all_widgets(self):
        """Test listing all widgets"""
        widgets = list_widgets()
        self.assertGreater(len(widgets), 0)
        self.assertIn("ttk.Button", widgets)
    
    def test_list_by_category(self):
        """Test filtering by category"""
        input_widgets = list_widgets("input")
        self.assertGreater(len(input_widgets), 0)
        for widget, info in input_widgets.items():
            self.assertEqual(info["category"], "input")
    
    def test_search_widgets(self):
        """Test widget search"""
        results = search_widgets("button")
        self.assertGreater(len(results), 0)
        self.assertIn("ttk.Button", results)
    
    def test_get_widget_info(self):
        """Test getting widget details"""
        info = get_widget_info("ttk.Button")
        self.assertIsNotNone(info)
        self.assertEqual(info["category"], "action")
        self.assertIn("properties", info)
        self.assertIn("use_cases", info)
    
    def test_widget_library_structure(self):
        """Test widget library has required fields"""
        for widget, info in WIDGET_LIBRARY.items():
            self.assertIn("category", info)
            self.assertIn("description", info)
            self.assertIn("properties", info)
            self.assertIn("use_cases", info)

if __name__ == '__main__':
    unittest.main()
