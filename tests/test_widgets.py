#!/usr/bin/env python3
"""Tests for enhanced widget detection"""
import unittest
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
import pygubuai_widgets

class TestWidgetDetection(unittest.TestCase):
    def test_basic_widgets(self):
        """Test basic widget detection"""
        widgets = pygubuai_widgets.detect_widgets("app with button and entry")
        widget_types = [w[0] for w in widgets]
        self.assertIn("button", widget_types)
        self.assertIn("entry", widget_types)
    
    def test_context_form(self):
        """Test form context detection"""
        widgets = pygubuai_widgets.detect_widgets("create a form")
        widget_types = [w[0] for w in widgets]
        self.assertIn("label", widget_types)
        self.assertIn("entry", widget_types)
        self.assertIn("button", widget_types)
    
    def test_context_login(self):
        """Test login context detection"""
        widgets = pygubuai_widgets.detect_widgets("login screen")
        widget_types = [w[0] for w in widgets]
        self.assertEqual(len(widgets), 5)  # 2 labels, 2 entries, 1 button
    
    def test_advanced_widgets(self):
        """Test advanced widget detection"""
        widgets = pygubuai_widgets.detect_widgets("app with dropdown and slider")
        widget_types = [w[0] for w in widgets]
        self.assertIn("combobox", widget_types)
        self.assertIn("scale", widget_types)
    
    def test_callback_extraction(self):
        """Test callback method extraction"""
        widgets = pygubuai_widgets.detect_widgets("app with button")
        callbacks = pygubuai_widgets.get_callbacks(widgets)
        self.assertIn("on_button_click", callbacks)
    
    def test_widget_xml_generation(self):
        """Test XML generation for widgets"""
        config = pygubuai_widgets.WIDGET_PATTERNS["button"]
        xml = pygubuai_widgets.generate_widget_xml("button", "btn1", config)
        xml_str = '\n'.join(xml)
        self.assertIn("ttk.Button", xml_str)
        self.assertIn("btn1", xml_str)

if __name__ == '__main__':
    unittest.main()
