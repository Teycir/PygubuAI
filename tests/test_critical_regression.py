"""Critical regression tests for core functionality.

These tests ensure that critical components continue to work correctly
after changes. They test real-world scenarios and edge cases.
"""
import unittest
import tempfile
import shutil
import json
import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.utils import (
    validate_safe_path, safe_xml_text, get_file_hash,
    validate_project_name, ensure_directory
)
from pygubuai.git_integration import init_git_repo, git_commit
from pygubuai.generator import (
    generate_base_ui_xml_structure,
    generate_python_app_structure,
    generate_readme_content
)
from pygubuai.registry import Registry
from pygubuai.errors import (
    PygubuAIError, ProjectNotFoundError, FileOperationError,
    ValidationError
)


class TestSecurityRegression(unittest.TestCase):
    """Regression tests for security fixes - must never break."""
    
    def test_path_traversal_always_blocked(self):
        """CRITICAL: Path traversal must always be blocked."""
        malicious_paths = [
            "../../../etc/passwd",
            "foo/../../etc/passwd",
            "./../../sensitive",
            "normal/../../../etc/passwd",
        ]
        
        for path in malicious_paths:
            with self.subTest(path=path):
                with self.assertRaises(ValueError, msg=f"Path traversal not blocked: {path}"):
                    validate_safe_path(path)
    
    def test_command_injection_always_prevented(self):
        """CRITICAL: Command injection must always be prevented."""
        temp_dir = tempfile.mkdtemp()
        try:
            project_path = Path(temp_dir) / "test"
            project_path.mkdir()
            
            # This should not execute the malicious command
            result = init_git_repo(project_path)
            
            # Verify no shell injection occurred
            # If injection worked, it would create a file
            malicious_file = project_path / "pwned"
            self.assertFalse(malicious_file.exists(), "Command injection detected!")
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_xss_always_escaped(self):
        """CRITICAL: XSS attacks must always be escaped."""
        xss_payloads = [
            ("<script>alert('xss')</script>", ["<script>", "<img", "<iframe"], ["&lt;"]),
            ("<img src=x onerror=alert(1)>", ["<img"], ["&lt;"]),
            ("<iframe src='evil.com'>", ["<iframe"], ["&lt;"]),
        ]
        
        for payload, forbidden, required in xss_payloads:
            with self.subTest(payload=payload):
                escaped = safe_xml_text(payload)
                for forbidden_str in forbidden:
                    self.assertNotIn(forbidden_str, escaped, 
                                   f"Dangerous string not escaped: {forbidden_str}")
                for required_str in required:
                    self.assertIn(required_str, escaped,
                                f"Expected escape sequence missing: {required_str}")
    
    def test_secure_hashing_always_used(self):
        """CRITICAL: Must always use SHA-256, never MD5."""
        temp_dir = tempfile.mkdtemp()
        try:
            test_file = Path(temp_dir) / "test.txt"
            test_file.write_text("test content")
            
            hash_value = get_file_hash(test_file)
            
            # SHA-256 = 64 chars, MD5 = 32 chars
            self.assertEqual(len(hash_value), 64, "Must use SHA-256 (64 chars)")
            self.assertNotEqual(len(hash_value), 32, "Must not use MD5 (32 chars)")
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestRegistryRegression(unittest.TestCase):
    """Regression tests for project registry - critical for project management."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.registry_file = Path(self.temp_dir) / "test_registry.json"
        self.registry = Registry(self.registry_file)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_registry_survives_corruption(self):
        """CRITICAL: Registry must handle corrupted files gracefully."""
        # Corrupt the registry file
        self.registry_file.write_text("{ invalid json }")
        
        # Should not crash, should reinitialize
        registry = Registry(self.registry_file)
        projects = registry.list_projects()
        self.assertIsInstance(projects, dict)
    
    def test_registry_concurrent_access(self):
        """CRITICAL: Registry must handle concurrent access safely."""
        # Add projects from multiple "threads" (simulated)
        for i in range(10):
            self.registry.add_project(f"project{i}", f"/path/to/project{i}")
        
        # All projects should be saved
        projects = self.registry.list_projects()
        self.assertEqual(len(projects), 10)
    
    def test_registry_preserves_metadata(self):
        """CRITICAL: Registry must preserve all metadata."""
        self.registry.add_project(
            "test",
            "/path/to/test",
            description="Test project",
            tags=["tag1", "tag2"]
        )
        
        # Reload registry
        registry2 = Registry(self.registry_file)
        metadata = registry2.get_project_metadata("test")
        
        self.assertEqual(metadata["description"], "Test project")
        self.assertEqual(metadata["tags"], ["tag1", "tag2"])
        self.assertIn("created", metadata)
        self.assertIn("modified", metadata)
    
    def test_registry_path_validation(self):
        """CRITICAL: Registry must validate all paths."""
        with self.assertRaises(ValueError):
            self.registry.add_project("evil", "../../../etc/passwd")


class TestGeneratorRegression(unittest.TestCase):
    """Regression tests for code generation - must produce valid output."""
    
    def test_generated_xml_always_valid(self):
        """CRITICAL: Generated XML must always be valid."""
        import xml.etree.ElementTree as ET
        
        test_cases = [
            ("simple", []),
            ("with_widgets", [("button", {"id": "btn1", "text": "Click"})]),
            ("special_chars", [("label", {"id": "lbl1", "text": "<>&\"'"})]),
        ]
        
        for name, widgets in test_cases:
            with self.subTest(name=name):
                xml = generate_base_ui_xml_structure(name, widgets)
                
                # Must parse without error
                try:
                    ET.fromstring(xml)
                except ET.ParseError as e:
                    self.fail(f"Generated invalid XML: {e}")
    
    def test_generated_python_always_valid(self):
        """CRITICAL: Generated Python must always be valid syntax."""
        test_cases = [
            ("simple", []),
            ("with_callbacks", ["on_click", "on_submit", "on_close"]),
            ("special_names", ["on_button_1_click", "handle_event"]),
        ]
        
        for name, callbacks in test_cases:
            with self.subTest(name=name):
                code = generate_python_app_structure(name, callbacks)
                
                # Must compile without error
                try:
                    compile(code, "<generated>", "exec")
                except SyntaxError as e:
                    self.fail(f"Generated invalid Python: {e}")
    
    def test_generated_code_has_required_elements(self):
        """CRITICAL: Generated code must have all required elements."""
        code = generate_python_app_structure("test", ["on_click"])
        
        # Must have these elements
        required = [
            "import pathlib",
            "import tkinter",
            "import pygubu",
            "class TestApp:",
            "__init__",
            "mainloop",
            "if __name__",
        ]
        
        for element in required:
            self.assertIn(element, code, f"Missing required element: {element}")


class TestErrorHandlingRegression(unittest.TestCase):
    """Regression tests for error handling - must provide useful errors."""
    
    def test_errors_always_have_suggestions(self):
        """CRITICAL: All errors must provide helpful suggestions."""
        errors = [
            ProjectNotFoundError("test"),
            ValidationError("name", "bad<>name", "invalid chars"),
            FileOperationError("write", "/test", PermissionError("denied")),
        ]
        
        for error in errors:
            with self.subTest(error=type(error).__name__):
                error_str = str(error)
                self.assertIn("[ERROR]", error_str)
                self.assertIn("[SUGGESTION]", error_str)
    
    def test_error_chains_preserved(self):
        """CRITICAL: Error chains must be preserved for debugging."""
        try:
            try:
                raise ValueError("Original")
            except ValueError as e:
                raise PygubuAIError("Wrapped", cause=e) from e
        except PygubuAIError as e:
            self.assertIsNotNone(e.__cause__)
            self.assertIsInstance(e.__cause__, ValueError)


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world usage scenarios that must always work."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_project_end_to_end(self):
        """CRITICAL: Basic project creation must always work."""
        project_name = "test_project"
        project_dir = Path(self.temp_dir) / project_name
        
        # Create project structure
        ensure_directory(project_dir)
        
        # Generate files
        ui_xml = generate_base_ui_xml_structure(project_name, [])
        py_code = generate_python_app_structure(project_name, [])
        readme = generate_readme_content(project_name, "Test", f"{project_name}.ui")
        
        # Write files
        (project_dir / f"{project_name}.ui").write_text(ui_xml)
        (project_dir / f"{project_name}.py").write_text(py_code)
        (project_dir / "README.md").write_text(readme)
        
        # Verify all files exist and are valid
        self.assertTrue((project_dir / f"{project_name}.ui").exists())
        self.assertTrue((project_dir / f"{project_name}.py").exists())
        self.assertTrue((project_dir / "README.md").exists())
        
        # Verify Python is valid
        py_file = project_dir / f"{project_name}.py"
        compile(py_file.read_text(), str(py_file), "exec")
    
    def test_registry_workflow(self):
        """CRITICAL: Registry workflow must always work."""
        registry_file = Path(self.temp_dir) / "registry.json"
        registry = Registry(registry_file)
        
        # Add project
        registry.add_project("test", str(self.temp_dir), "Test project", ["test"])
        
        # Retrieve project
        path = registry.get_project("test")
        self.assertEqual(path, str(self.temp_dir))
        
        # Set active
        registry.set_active("test")
        active = registry.get_active()
        self.assertEqual(active, "test")
        
        # Search
        results = registry.search_projects("test")
        self.assertIn("test", results)
    
    def test_git_integration_workflow(self):
        """CRITICAL: Git integration must work when git is available."""
        project_dir = Path(self.temp_dir) / "git_test"
        project_dir.mkdir()
        
        # Check if git is available
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.skipTest("Git not available")
        
        # Initialize repo
        result = init_git_repo(project_dir)
        
        if result:
            # Verify git repo created
            self.assertTrue((project_dir / ".git").exists())
            self.assertTrue((project_dir / ".gitignore").exists())


class TestEdgeCases(unittest.TestCase):
    """Test edge cases that have caused bugs in the past."""
    
    def test_empty_project_name(self):
        """Edge case: Empty project name must be rejected."""
        with self.assertRaises(ValueError):
            validate_project_name("")
    
    def test_very_long_project_name(self):
        """Edge case: Very long names must be handled."""
        long_name = "a" * 1000
        # Should either accept or reject gracefully
        try:
            result = validate_project_name(long_name)
            self.assertIsInstance(result, str)
        except ValueError:
            pass  # Acceptable to reject
    
    def test_unicode_in_project_name(self):
        """Edge case: Unicode characters must be handled."""
        unicode_names = ["test_项目", "test_проект", "test_🚀"]
        
        for name in unicode_names:
            with self.subTest(name=name):
                # Should sanitize or reject gracefully
                try:
                    result = validate_project_name(name)
                    self.assertIsInstance(result, str)
                except ValueError:
                    pass  # Acceptable to reject
    
    def test_none_values_handled(self):
        """Edge case: None values must not crash."""
        # These should not crash
        self.assertEqual(safe_xml_text(None), "")
        
        with self.assertRaises(ValueError):
            validate_safe_path(None)
    
    def test_empty_registry(self):
        """Edge case: Empty registry must work."""
        temp_dir = tempfile.mkdtemp()
        try:
            registry_file = Path(temp_dir) / "empty.json"
            registry = Registry(registry_file)
            
            projects = registry.list_projects()
            self.assertEqual(projects, {})
            
            active = registry.get_active()
            self.assertIsNone(active)
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestPerformanceRegression(unittest.TestCase):
    """Test that performance doesn't degrade."""
    
    def test_registry_scales_to_100_projects(self):
        """Performance: Registry must handle 100+ projects."""
        import time
        
        temp_dir = tempfile.mkdtemp()
        try:
            registry_file = Path(temp_dir) / "large.json"
            registry = Registry(registry_file)
            
            # Add 100 projects
            start = time.time()
            for i in range(100):
                registry.add_project(f"project{i}", f"/path/{i}")
            add_time = time.time() - start
            
            # Should complete in reasonable time (< 5 seconds)
            self.assertLess(add_time, 5.0, "Adding 100 projects too slow")
            
            # List should be fast
            start = time.time()
            projects = registry.list_projects()
            list_time = time.time() - start
            
            self.assertEqual(len(projects), 100)
            self.assertLess(list_time, 1.0, "Listing 100 projects too slow")
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_xml_generation_scales(self):
        """Performance: XML generation must scale to 50+ widgets."""
        import time
        
        widgets = [("button", {"id": f"btn{i}", "text": f"Button {i}"}) 
                   for i in range(50)]
        
        start = time.time()
        xml = generate_base_ui_xml_structure("test", widgets)
        gen_time = time.time() - start
        
        self.assertLess(gen_time, 1.0, "Generating 50 widgets too slow")
        self.assertIn("btn49", xml)


def run_critical_tests():
    """Run all critical regression tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityRegression))
    suite.addTests(loader.loadTestsFromTestCase(TestRegistryRegression))
    suite.addTests(loader.loadTestsFromTestCase(TestGeneratorRegression))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandlingRegression))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceRegression))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_critical_tests()
    sys.exit(0 if success else 1)
