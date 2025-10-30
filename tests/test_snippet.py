#!/usr/bin/env python3
"""Tests for snippet module"""
import unittest
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'src'))

from pygubuai.snippet import generate_snippet, SNIPPET_TEMPLATES

class TestSnippet(unittest.TestCase):
    def test_generate_button(self):
        """Test button snippet generation"""
        snippet = generate_snippet("button", text="Submit", command="on_submit")
        self.assertIn("ttk.Button", snippet)
        self.assertIn("Submit", snippet)
        self.assertIn("on_submit", snippet)
    
    def test_generate_entry(self):
        """Test entry snippet generation"""
        snippet = generate_snippet("entry", variable="email_var")
        self.assertIn("ttk.Entry", snippet)
        self.assertIn("email_var", snippet)
    
    def test_generate_frame(self):
        """Test frame snippet generation"""
        snippet = generate_snippet("frame", layout="grid")
        self.assertIn("ttk.Frame", snippet)
        self.assertIn("grid", snippet)
    
    def test_all_templates_valid(self):
        """Test all templates can be generated"""
        for widget_type in SNIPPET_TEMPLATES.keys():
            snippet = generate_snippet(widget_type)
            self.assertIsInstance(snippet, str)
            self.assertGreater(len(snippet), 0)

if __name__ == '__main__':
    unittest.main()
