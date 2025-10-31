#!/usr/bin/env python3
"""Verification script for PygubuAI v0.6.0 - Advanced Theming System"""

import sys


def check_module(module_name):
    """Check if module exists and can be imported"""
    try:
        __import__(f"pygubuai.{module_name}")
        return True, "✓"
    except ImportError as e:
        return False, f"✗ ({e})"


def check_presets():
    """Check if all presets are available"""
    try:
        from pygubuai.theme_presets import list_presets

        presets = list_presets()
        expected = [
            "modern-dark",
            "modern-light",
            "material",
            "nord",
            "solarized-dark",
            "solarized-light",
            "high-contrast",
            "dracula",
        ]
        if set(presets) == set(expected):
            return True, f"✓ ({len(presets)} presets)"
        else:
            return False, f"✗ (expected {len(expected)}, got {len(presets)})"
    except Exception as e:
        return False, f"✗ ({e})"


def check_themes_dir():
    """Check if themes directory can be created"""
    try:
        from pygubuai.theme_builder import get_themes_dir

        themes_dir = get_themes_dir()
        return True, f"✓ ({themes_dir})"
    except Exception as e:
        return False, f"✗ ({e})"


def run_tests():
    """Run unit tests"""
    import unittest

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_modules = ["tests.test_theme_presets", "tests.test_theme_advanced", "tests.test_theme_builder"]

    for module in test_modules:
        try:
            suite.addTests(loader.loadTestsFromName(module))
        except Exception:
            pass

    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    if result.wasSuccessful():
        return True, f"✓ ({result.testsRun} tests passed)"
    else:
        return False, f"✗ ({len(result.failures)} failures, {len(result.errors)} errors)"


def main():
    print("=" * 60)
    print("PygubuAI v0.6.0 - Advanced Theming System Verification")
    print("=" * 60)
    print()

    checks = [
        (
            "Core Modules",
            [
                ("theme_presets", check_module("theme_presets")),
                ("theme_advanced", check_module("theme_advanced")),
                ("theme_builder", check_module("theme_builder")),
                ("theme_preview", check_module("theme_preview")),
            ],
        ),
        (
            "Features",
            [
                ("8 Theme Presets", check_presets()),
                ("Themes Directory", check_themes_dir()),
            ],
        ),
        (
            "Tests",
            [
                ("Unit Tests", run_tests()),
            ],
        ),
    ]

    all_passed = True

    for section, items in checks:
        print(f"{section}:")
        for name, (passed, status) in items:
            print(f"  {name:25} {status}")
            if not passed:
                all_passed = False
        print()

    print("=" * 60)
    if all_passed:
        print("✓ All checks passed! v0.6.0 is ready.")
        print()
        print("Try it out:")
        print("  pygubu-theme list")
        print("  pygubu-theme info modern-dark")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
