#!/usr/bin/env python3
"""Verify architecture migration is complete"""
import sys
from pathlib import Path


def check_imports():
    """Verify all package imports work"""
    print("Checking imports...")
    try:
        from pygubuai.create import main as create_main  # noqa: F401
        from pygubuai.register import main as register_main  # noqa: F401
        from pygubuai.template import main as template_main  # noqa: F401
        from pygubuai.workflow import main as workflow_main  # noqa: F401
        from pygubuai.converter import main as converter_main  # noqa: F401
        from pygubuai.widgets import detect_widgets, get_callbacks  # noqa: F401
        from pygubuai.generator import generate_base_ui_xml_structure  # noqa: F401
        from pygubuai.registry import Registry  # noqa: F401

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def check_cli_wrappers():
    """Verify CLI wrappers exist and are minimal"""
    print("\nChecking CLI wrappers...")
    wrappers = ["pygubu-create", "pygubu-register", "pygubu-template", "pygubu-ai-workflow", "tkinter-to-pygubu"]

    all_good = True
    for wrapper in wrappers:
        path = Path(wrapper)
        if not path.exists():
            print(f"✗ {wrapper} not found")
            all_good = False
            continue

        content = path.read_text()
        code_lines = [line for line in content.split("\n") if line.strip() and not line.strip().startswith("#")]

        # Should be minimal: import + if __name__ + main()
        if len(code_lines) <= 4:
            print(f"✓ {wrapper} is minimal wrapper ({len(code_lines)} lines)")
        else:
            print(f"⚠ {wrapper} has {len(code_lines)} lines (expected ≤4)")
            all_good = False

    return all_good


def check_no_standalone_modules():
    """Verify no standalone pygubuai_*.py files exist"""
    print("\nChecking for deprecated standalone modules...")
    deprecated = [
        "pygubuai_widgets.py",
        "pygubuai_config.py",
        "pygubuai_errors.py",
        "pygubuai_interactive.py",
        "pygubuai_templates.py",
    ]

    all_good = True
    for module in deprecated:
        if Path(module).exists():
            print(f"✗ Deprecated module found: {module}")
            all_good = False

    if all_good:
        print("✓ No deprecated standalone modules found")

    return all_good


def check_package_structure():
    """Verify package structure is correct"""
    print("\nChecking package structure...")
    required_modules = [
        "src/pygubuai/__init__.py",
        "src/pygubuai/create.py",
        "src/pygubuai/register.py",
        "src/pygubuai/template.py",
        "src/pygubuai/workflow.py",
        "src/pygubuai/converter.py",
        "src/pygubuai/widgets.py",
        "src/pygubuai/generator.py",
        "src/pygubuai/registry.py",
    ]

    all_good = True
    for module in required_modules:
        if Path(module).exists():
            print(f"✓ {module}")
        else:
            print(f"✗ Missing: {module}")
            all_good = False

    return all_good


def check_documentation():
    """Verify documentation exists"""
    print("\nChecking documentation...")
    docs = ["ARCHITECTURE.md", "MIGRATION_SUMMARY.md", "DEVELOPER_QUICK_REF.md"]

    all_good = True
    for doc in docs:
        if Path(doc).exists():
            print(f"✓ {doc}")
        else:
            print(f"✗ Missing: {doc}")
            all_good = False

    return all_good


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("PygubuAI Architecture Verification")
    print("=" * 60)

    checks = [
        check_imports,
        check_cli_wrappers,
        check_no_standalone_modules,
        check_package_structure,
        check_documentation,
    ]

    results = [check() for check in checks]

    print("\n" + "=" * 60)
    if all(results):
        print("✓ All checks passed! Architecture migration complete.")
        print("=" * 60)
        return 0
    else:
        print("✗ Some checks failed. Review output above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
