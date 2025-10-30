"""Tests for accessibility helpers."""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.accessibility import (
    check_color_contrast, generate_aria_labels,
    validate_keyboard_navigation, check_accessibility
)


class TestAccessibility(unittest.TestCase):
    """Test accessibility functionality."""
    
    def test_color_contrast_pass(self):
        """Test color contrast that passes WCAG AA."""
        passes, ratio = check_color_contrast("#000000", "#FFFFFF")
        self.assertTrue(passes)
        self.assertGreater(ratio, 4.5)
    
    def test_color_contrast_fail(self):
        """Test color contrast that fails WCAG AA."""
        passes, ratio = check_color_contrast("#888888", "#999999")
        self.assertFalse(passes)
        self.assertLess(ratio, 4.5)
    
    def test_aria_labels(self):
        """Test ARIA label generation."""
        labels = generate_aria_labels("Button", "submit_btn")
        self.assertIn("aria-label", labels)
        self.assertIn("Button", labels["aria-label"])
        self.assertIn("submit_btn", labels["aria-label"])
    
    def test_keyboard_navigation_no_focus(self):
        """Test keyboard navigation validation with no focus."""
        widgets = [
            {"class": "ttk.Button", "id": "btn1"},
            {"class": "ttk.Entry", "id": "entry1"}
        ]
        issues = validate_keyboard_navigation(widgets)
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("focus" in issue.lower() for issue in issues))
    
    def test_keyboard_navigation_with_focus(self):
        """Test keyboard navigation with proper focus."""
        widgets = [
            {"class": "ttk.Button", "id": "btn1", "takefocus": "1"},
            {"class": "ttk.Entry", "id": "entry1", "takefocus": "1"}
        ]
        issues = validate_keyboard_navigation(widgets)
        # Should still have issue about underline
        self.assertTrue(any("underline" in issue.lower() for issue in issues))
    
    def test_check_accessibility(self):
        """Test full accessibility check."""
        ui_data = {
            "widgets": [
                {"class": "ttk.Entry", "id": "username"},
                {"class": "ttk.Button", "id": "submit"}
            ]
        }
        issues = check_accessibility(ui_data)
        self.assertIn("keyboard", issues)
        self.assertIn("labels", issues)


if __name__ == "__main__":
    unittest.main()
