#!/usr/bin/env python3
"""Tests for pygubu-create functionality"""
import unittest
import tempfile
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))


class TestProjectCreation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_description(self):
        """Test widget detection from description"""
        from pygubuai import widgets as pygubuai_widgets

        widgets = pygubuai_widgets.detect_widgets("login form with username and password")
        self.assertTrue(any(w[0] == "entry" for w in widgets))

        widgets = pygubuai_widgets.detect_widgets("app with button and list")
        self.assertTrue(any(w[0] == "button" for w in widgets))
        self.assertTrue(any(w[0] == "treeview" for w in widgets))

    def test_project_structure(self):
        """Test complete project creation"""
        from pygubuai import widgets as pygubuai_widgets

        # Test that we can detect widgets and generate structure
        widgets = pygubuai_widgets.detect_widgets("simple app with button")
        self.assertTrue(len(widgets) > 0)
        self.assertTrue(any(w[0] == "button" for w in widgets))

        # Test XML generation
        config = pygubuai_widgets.WIDGET_PATTERNS["button"]
        xml = pygubuai_widgets.generate_widget_xml("button", "btn1", config)
        self.assertTrue(len(xml) > 0)


if __name__ == "__main__":
    unittest.main()
