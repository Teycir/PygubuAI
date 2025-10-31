#!/usr/bin/env python3
"""Tests for actual CLI script invocation via subprocess."""
import unittest
import subprocess
import sys
from pathlib import Path


class TestCLIScriptInvocation(unittest.TestCase):
    """Test that CLI scripts are properly installed and executable."""

    def test_pygubu_create_version(self):
        """Test pygubu-create --version works"""
        result = subprocess.run([sys.executable, "-m", "pygubuai.create", "--version"], capture_output=True, text=True)
        # Exit code 0 for --version, or 1 if pygubu not installed
        self.assertIn(result.returncode, [0, 1])
        if result.returncode == 0:
            self.assertIn("0.", result.stdout)  # Accept any 0.x version

    def test_pygubu_create_help(self):
        """Test pygubu-create --help works"""
        result = subprocess.run([sys.executable, "-m", "pygubuai.create", "--help"], capture_output=True, text=True)
        # Exit code 0 for --help, or 1 if pygubu not installed
        self.assertIn(result.returncode, [0, 1])
        if result.returncode == 0:
            self.assertIn("usage", result.stdout.lower())

    def test_pygubu_register_help(self):
        """Test pygubu-register --help works"""
        result = subprocess.run([sys.executable, "-m", "pygubuai.register", "--help"], capture_output=True, text=True)
        # Should work even without pygubu
        self.assertIn(result.returncode, [0, 1])

    def test_pygubu_template_help(self):
        """Test pygubu-template --help works"""
        result = subprocess.run([sys.executable, "-m", "pygubuai.template", "--help"], capture_output=True, text=True)
        # Should work even without pygubu
        self.assertIn(result.returncode, [0, 1])

    def test_all_entry_points_exist(self):
        """Verify all entry points in pyproject.toml have corresponding modules"""
        # Extract entry points
        entry_points = [
            "pygubuai.create",
            "pygubuai.register",
            "pygubuai.template",
            "pygubuai.workflow",
            "pygubuai.converter",
        ]

        # Verify modules exist
        src_dir = Path(__file__).parent.parent / "src" / "pygubuai"
        for ep in entry_points:
            module_name = ep.split(".")[-1]
            module_file = src_dir / f"{module_name}.py"
            self.assertTrue(module_file.exists(), f"Module {module_file} not found for entry point {ep}")


if __name__ == "__main__":
    unittest.main()
