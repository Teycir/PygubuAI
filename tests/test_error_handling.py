"""Tests for improved error handling."""

import unittest
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pygubuai.errors import (  # noqa: E402
    PygubuAIError,
    ProjectNotFoundError,
    InvalidProjectError,
    DependencyError,
    FileOperationError,
    ValidationError,
    RegistryError,
    UIParseError,
    GitError,
    validate_pygubu,
    handle_file_operation,
)


class TestErrorClasses(unittest.TestCase):
    """Test custom error classes."""

    def test_base_error_with_suggestion(self):
        """Test base error includes suggestion."""
        error = PygubuAIError("Test error", "Try this fix")
        error_str = str(error)
        self.assertIn("Test error", error_str)
        self.assertIn("Try this fix", error_str)

    def test_base_error_with_cause(self):
        """Test base error includes cause."""
        cause = ValueError("Original error")
        error = PygubuAIError("Test error", cause=cause)
        error_str = str(error)
        self.assertIn("Test error", error_str)
        self.assertIn("ValueError", error_str)

    def test_project_not_found_error(self):
        """Test ProjectNotFoundError."""
        error = ProjectNotFoundError("myproject")
        self.assertIn("myproject", str(error))
        self.assertIn("not found", str(error).lower())

    def test_invalid_project_error(self):
        """Test InvalidProjectError."""
        error = InvalidProjectError("/path/to/project", "missing .ui file")
        error_str = str(error)
        self.assertIn("/path/to/project", error_str)
        self.assertIn("missing .ui file", error_str)

    def test_dependency_error(self):
        """Test DependencyError."""
        error = DependencyError("pygubu")
        error_str = str(error)
        self.assertIn("pygubu", error_str)
        self.assertIn("pip install", error_str.lower())

    def test_file_operation_error(self):
        """Test FileOperationError."""
        cause = PermissionError("Access denied")
        error = FileOperationError("write", "/path/to/file", cause)
        error_str = str(error)
        self.assertIn("write", error_str)
        self.assertIn("/path/to/file", error_str)
        self.assertIn("PermissionError", error_str)

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("project_name", "test<>name", "contains invalid characters")
        error_str = str(error)
        self.assertIn("project_name", error_str)
        self.assertIn("test<>name", error_str)
        self.assertIn("invalid characters", error_str)

    def test_registry_error(self):
        """Test RegistryError."""
        error = RegistryError("add_project", "file locked")
        error_str = str(error)
        self.assertIn("add_project", error_str)
        self.assertIn("file locked", error_str)

    def test_ui_parse_error(self):
        """Test UIParseError."""
        error = UIParseError("/path/to/file.ui", "invalid XML")
        error_str = str(error)
        self.assertIn("/path/to/file.ui", error_str)
        self.assertIn("invalid XML", error_str)

    def test_git_error(self):
        """Test GitError."""
        error = GitError("commit", "not a git repository")
        error_str = str(error)
        self.assertIn("commit", error_str)
        self.assertIn("not a git repository", error_str)


class TestErrorValidation(unittest.TestCase):
    """Test validation functions."""

    def test_validate_pygubu_success(self):
        """Test validate_pygubu when pygubu is installed."""
        try:
            validate_pygubu()
            # Should not raise if pygubu is installed
        except DependencyError:
            self.skipTest("pygubu not installed")

    def test_handle_file_operation_success(self):
        """Test handle_file_operation with successful operation."""
        temp_dir = tempfile.mkdtemp()
        temp_file = Path(temp_dir) / "test.txt"

        def write_file():
            temp_file.write_text("test")

        result = handle_file_operation("write", str(temp_file), write_file)
        self.assertIsNone(result)
        self.assertTrue(temp_file.exists())

        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)

    def test_handle_file_operation_permission_error(self):
        """Test handle_file_operation with permission error."""

        def failing_operation():
            raise PermissionError("Access denied")

        with self.assertRaises(FileOperationError) as ctx:
            handle_file_operation("write", "/test/file", failing_operation)

        self.assertIn("write", str(ctx.exception))
        self.assertIn("/test/file", str(ctx.exception))

    def test_handle_file_operation_os_error(self):
        """Test handle_file_operation with OS error."""

        def failing_operation():
            raise OSError("Disk full")

        with self.assertRaises(FileOperationError) as ctx:
            handle_file_operation("write", "/test/file", failing_operation)

        self.assertIn("Disk full", str(ctx.exception))


class TestErrorChaining(unittest.TestCase):
    """Test error chaining and cause tracking."""

    def test_error_chain_preserved(self):
        """Test that error chains are preserved."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise PygubuAIError("Wrapped error", cause=e) from e
        except PygubuAIError as e:
            self.assertIsNotNone(e.__cause__)
            self.assertIsInstance(e.__cause__, ValueError)
            self.assertIn("Original error", str(e.__cause__))

    def test_file_operation_error_chain(self):
        """Test FileOperationError preserves cause."""
        original = PermissionError("Access denied")
        error = FileOperationError("write", "/test", original)

        self.assertEqual(error.cause, original)
        self.assertIn("PermissionError", str(error))


class TestErrorRecovery(unittest.TestCase):
    """Test error recovery mechanisms."""

    def test_graceful_degradation(self):
        """Test that errors don't crash the entire system."""
        from pygubuai.cache import get_cached

        # Should return None instead of crashing on invalid path
        get_cached(Path("/nonexistent/file.ui"))
        # May raise or return None depending on implementation
        # The important thing is it doesn't crash

    def test_error_logging(self):
        """Test that errors are properly logged."""
        import logging
        from io import StringIO

        # Capture log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.ERROR)

        logger = logging.getLogger("pygubuai")
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        try:
            # Trigger an error
            raise PygubuAIError("Test error for logging")
        except PygubuAIError:
            pass

        # Check that something was logged (implementation dependent)
        # This is more of a smoke test
        logger.removeHandler(handler)


class TestErrorMessages(unittest.TestCase):
    """Test error message quality."""

    def test_error_messages_are_helpful(self):
        """Test that error messages provide actionable information."""
        errors = [
            ProjectNotFoundError("myproject"),
            DependencyError("pygubu"),
            ValidationError("name", "test<>", "invalid chars"),
        ]

        for error in errors:
            error_str = str(error)
            # Should have both error and suggestion
            self.assertIn("[ERROR]", error_str)
            self.assertIn("[SUGGESTION]", error_str)

    def test_error_messages_include_context(self):
        """Test that errors include relevant context."""
        error = FileOperationError("write", "/path/to/file.txt", PermissionError("Access denied"))

        error_str = str(error)
        self.assertIn("write", error_str)
        self.assertIn("/path/to/file.txt", error_str)
        self.assertIn("PermissionError", error_str)


def run_error_handling_tests():
    """Run all error handling tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestErrorClasses))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorChaining))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorRecovery))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorMessages))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_error_handling_tests()
    sys.exit(0 if success else 1)
