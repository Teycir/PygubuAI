#!/usr/bin/env python3
"""Verify v0.5.0 installation and features"""
import subprocess
import sys
from pathlib import Path

COMMANDS = [
    # Core commands
    ("pygubu-create", "Core: Project creation"),
    ("pygubu-register", "Core: Project registry"),
    ("pygubu-template", "Core: Templates"),
    ("pygubu-ai-workflow", "Core: Workflow"),
    ("tkinter-to-pygubu", "Core: Converter"),
    # New v0.5.0 commands
    ("pygubu-status", "v0.5.0: Status checker"),
    ("pygubu-widgets", "v0.5.0: Widget browser"),
    ("pygubu-theme", "v0.5.0: Theme switcher"),
    ("pygubu-preview", "v0.5.0: Quick preview"),
    ("pygubu-validate", "v0.5.0: Validator"),
    ("pygubu-inspect", "v0.5.0: Inspector"),
    ("pygubu-snippet", "v0.5.0: Snippet generator"),
    ("pygubu-prompt", "v0.5.0: AI prompts"),
    ("pygubu-batch", "v0.5.0: Batch operations"),
    ("pygubu-export", "v0.5.0: Standalone export"),
]

MODULES = [
    "pygubuai.status",
    "pygubuai.widgets",
    "pygubuai.widget_data",
    "pygubuai.theme",
    "pygubuai.preview",
    "pygubuai.validate_project",
    "pygubuai.inspect",
    "pygubuai.snippet",
    "pygubuai.prompt",
    "pygubuai.batch",
    "pygubuai.export",
]


def check_command(cmd, description):
    """Check if command is available"""
    try:
        result = subprocess.run([cmd, "--help"], capture_output=True, timeout=5)
        if result.returncode == 0 or "Usage:" in result.stdout.decode() or "Usage:" in result.stderr.decode():
            print(f"  ✓ {description:30} ({cmd})")
            return True
        else:
            print(f"  ✗ {description:30} ({cmd}) - Exit code: {result.returncode}")
            return False
    except FileNotFoundError:
        print(f"  ✗ {description:30} ({cmd}) - Not found")
        return False
    except Exception as e:
        print(f"  ✗ {description:30} ({cmd}) - Error: {e}")
        return False


def check_module(module_name):
    """Check if module can be imported"""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name}")
        return True
    except ImportError as e:
        print(f"  ✗ {module_name} - {e}")
        return False


def main():
    print("=" * 60)
    print("PygubuAI v0.5.0 Installation Verification")
    print("=" * 60)

    # Check commands
    print("\n1. Checking CLI Commands:\n")
    cmd_results = [check_command(cmd, desc) for cmd, desc in COMMANDS]
    cmd_success = sum(cmd_results)
    cmd_total = len(cmd_results)

    # Check modules
    print("\n2. Checking Python Modules:\n")
    mod_results = [check_module(mod) for mod in MODULES]
    mod_success = sum(mod_results)
    mod_total = len(mod_results)

    # Check documentation
    print("\n3. Checking Documentation:\n")
    docs = [
        ("ROADMAP.md", "Implementation roadmap"),
        ("FEATURE_SHOWCASE.md", "Feature showcase"),
        ("CHANGELOG.md", "Changelog"),
    ]

    doc_results = []
    for doc, desc in docs:
        path = Path(__file__).parent / doc
        if path.exists():
            print(f"  ✓ {desc:30} ({doc})")
            doc_results.append(True)
        else:
            print(f"  ✗ {desc:30} ({doc}) - Not found")
            doc_results.append(False)

    doc_success = sum(doc_results)
    doc_total = len(doc_results)

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"CLI Commands:  {cmd_success}/{cmd_total} available")
    print(f"Python Modules: {mod_success}/{mod_total} importable")
    print(f"Documentation:  {doc_success}/{doc_total} present")

    total_success = cmd_success + mod_success + doc_success
    total_checks = cmd_total + mod_total + doc_total

    print(f"\nOverall: {total_success}/{total_checks} checks passed")

    if total_success == total_checks:
        print("\n✓ All checks passed! PygubuAI v0.5.0 is ready to use.")
        print("\nTry these commands:")
        print("  pygubu-widgets list")
        print("  pygubu-status")
        print("  pygubu-prompt list")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please reinstall:")
        print("  pip install -e .")
        return 1


if __name__ == "__main__":
    sys.exit(main())
