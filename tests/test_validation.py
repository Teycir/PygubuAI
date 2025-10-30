"""Tests for validation module"""
import unittest
from pygubuai.validation import (
    validate_project_name, sanitize_project_name,
    validate_path, validate_tags, validate_description
)


class TestProjectNameValidation(unittest.TestCase):
    """Test project name validation"""
    
    def test_valid_name(self):
        valid, error = validate_project_name("myapp")
        self.assertTrue(valid)
        self.assertIsNone(error)
    
    def test_empty_name(self):
        valid, error = validate_project_name("")
        self.assertFalse(valid)
        self.assertIn("empty", error)
    
    def test_too_short(self):
        valid, error = validate_project_name("a")
        self.assertFalse(valid)
        self.assertIn("at least", error)
    
    def test_too_long(self):
        valid, error = validate_project_name("a" * 51)
        self.assertFalse(valid)
        self.assertIn("at most", error)
    
    def test_reserved_name(self):
        valid, error = validate_project_name("test")
        self.assertFalse(valid)
        self.assertIn("reserved", error)
    
    def test_invalid_characters(self):
        valid, error = validate_project_name("my app!")
        self.assertFalse(valid)
        self.assertIn("letters, numbers", error)
    
    def test_starts_with_number(self):
        valid, error = validate_project_name("123app")
        self.assertFalse(valid)
        self.assertIn("start with letter", error)


class TestSanitization(unittest.TestCase):
    """Test name sanitization"""
    
    def test_sanitize_spaces(self):
        result = sanitize_project_name("my app")
        self.assertEqual(result, "my_app")
    
    def test_sanitize_special_chars(self):
        result = sanitize_project_name("my@app!")
        self.assertEqual(result, "my_app_")
    
    def test_sanitize_starts_with_number(self):
        result = sanitize_project_name("123app")
        self.assertTrue(result.startswith("project_"))
    
    def test_sanitize_too_long(self):
        result = sanitize_project_name("a" * 100)
        self.assertLessEqual(len(result), 50)


class TestPathValidation(unittest.TestCase):
    """Test path validation"""
    
    def test_path_traversal(self):
        valid, error = validate_path("../../../etc/passwd")
        self.assertFalse(valid)
        self.assertIn("traversal", error)
    
    def test_valid_relative_path(self):
        valid, error = validate_path("./myproject")
        self.assertTrue(valid)


class TestTagsValidation(unittest.TestCase):
    """Test tags validation"""
    
    def test_valid_tags(self):
        valid, error = validate_tags(["web", "production"])
        self.assertTrue(valid)
    
    def test_too_many_tags(self):
        valid, error = validate_tags(["tag"] * 11)
        self.assertFalse(valid)
        self.assertIn("Maximum 10", error)
    
    def test_tag_too_long(self):
        valid, error = validate_tags(["a" * 21])
        self.assertFalse(valid)
        self.assertIn("1-20 characters", error)
    
    def test_invalid_tag_characters(self):
        valid, error = validate_tags(["tag with spaces"])
        self.assertFalse(valid)


class TestDescriptionValidation(unittest.TestCase):
    """Test description validation"""
    
    def test_valid_description(self):
        valid, error = validate_description("My application")
        self.assertTrue(valid)
    
    def test_empty_description(self):
        valid, error = validate_description("")
        self.assertTrue(valid)
    
    def test_too_long_description(self):
        valid, error = validate_description("a" * 501)
        self.assertFalse(valid)
        self.assertIn("at most 500", error)


if __name__ == '__main__':
    unittest.main()
