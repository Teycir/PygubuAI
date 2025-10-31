#!/usr/bin/env python3
"""
Verification script for test improvements implementation.
"""
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists."""
    path = Path(filepath)
    if path.exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False


def check_file_content(filepath, search_text, description):
    """Check if file contains specific text."""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ {description}: File not found")
        return False

    content = path.read_text()
    if search_text in content:
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}: Content not found")
        return False


def main():
    print("=" * 60)
    print("PygubuAI Test Improvements Verification")
    print("=" * 60)
    print()

    checks = []

    # 1. Check pytest.ini
    print("1. Pytest Configuration")
    print("-" * 40)
    checks.append(check_file_exists("pytest.ini", "pytest.ini exists"))
    checks.append(check_file_content("pytest.ini", "markers =", "Contains markers"))
    checks.append(check_file_content("pytest.ini", "unit:", "Has unit marker"))
    checks.append(check_file_content("pytest.ini", "security:", "Has security marker"))
    print()

    # 2. Check conftest.py
    print("2. Shared Fixtures")
    print("-" * 40)
    checks.append(check_file_exists("tests/conftest.py", "conftest.py exists"))
    checks.append(check_file_content("tests/conftest.py", "@pytest.fixture", "Has fixtures"))
    checks.append(check_file_content("tests/conftest.py", "def temp_project", "Has temp_project fixture"))
    checks.append(check_file_content("tests/conftest.py", "def mock_registry", "Has mock_registry fixture"))
    print()

    # 3. Check example pytest test
    print("3. Example Pytest Tests")
    print("-" * 40)
    checks.append(check_file_exists("tests/test_workflow_pytest.py", "test_workflow_pytest.py exists"))
    checks.append(check_file_content("tests/test_workflow_pytest.py", "@pytest.mark.unit", "Has unit markers"))
    checks.append(check_file_content("tests/test_workflow_pytest.py", "Given:", "Has Given-When-Then"))
    checks.append(check_file_content("tests/test_workflow_pytest.py", "@pytest.mark.security", "Has security markers"))
    print()

    # 4. Check CI workflow
    print("4. Enhanced CI Pipeline")
    print("-" * 40)
    checks.append(check_file_exists(".github/workflows/test-enhanced.yml", "CI workflow exists"))
    checks.append(check_file_content(".github/workflows/test-enhanced.yml", "fast-tests:", "Has fast-tests job"))
    checks.append(
        check_file_content(".github/workflows/test-enhanced.yml", "security-tests:", "Has security-tests job")
    )
    print()

    # 5. Check Makefile
    print("5. Makefile Commands")
    print("-" * 40)
    checks.append(check_file_exists("Makefile", "Makefile exists"))
    checks.append(check_file_content("Makefile", "test-fast:", "Has test-fast target"))
    checks.append(check_file_content("Makefile", "test-security:", "Has test-security target"))
    print()

    # 6. Check documentation
    print("6. Documentation")
    print("-" * 40)
    checks.append(check_file_exists("TEST_IMPROVEMENT_PLAN.md", "Improvement plan exists"))
    checks.append(check_file_exists("TEST_IMPLEMENTATION_SUMMARY.md", "Implementation summary exists"))
    print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100

    print(f"Passed: {passed}/{total} ({percentage:.1f}%)")
    print()

    if passed == total:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Next steps:")
        print("1. Install dev dependencies: pip install -e '.[dev]'")
        print("2. Run fast tests: make test-fast")
        print("3. Run all tests: make test")
        print("4. View coverage: make test-coverage")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print(f"   {total - passed} checks need attention")
        return 1


if __name__ == "__main__":
    sys.exit(main())
