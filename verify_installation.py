#!/usr/bin/env python3
"""Verify PygubuAI installation and functionality"""
import sys
import subprocess
from pathlib import Path

def run_cmd(cmd):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_imports():
    """Test all module imports"""
    print("Testing imports...")
    try:
        sys.path.insert(0, 'src')
        import pygubuai
        from pygubuai import create, register, template, workflow
        from pygubuai import config, errors, registry, templates, utils, widgets
        print("  ✓ All imports successful")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_version_flags():
    """Test --version flags"""
    print("\nTesting --version flags...")
    commands = [
        'python3 -c "import sys; sys.path.insert(0, \'src\'); from pygubuai.create import main; sys.argv = [\'pygubu-create\', \'--version\']; main()"',
        'python3 -c "import sys; sys.path.insert(0, \'src\'); from pygubuai.register import main; sys.argv = [\'pygubu-register\', \'--version\']; main()"',
        'python3 -c "import sys; sys.path.insert(0, \'src\'); from pygubuai.template import main; sys.argv = [\'pygubu-template\', \'--version\']; main()"',
        'python3 -c "import sys; sys.path.insert(0, \'src\'); from pygubuai.workflow import main; sys.argv = [\'pygubu-ai-workflow\', \'--version\']; main()"',
    ]
    
    all_ok = True
    for cmd in commands:
        success, stdout, stderr = run_cmd(cmd)
        tool = cmd.split("'")[5]
        if success and "0.1.0" in stdout:
            print(f"  ✓ {tool}")
        else:
            print(f"  ✗ {tool}")
            all_ok = False
    
    return all_ok

def test_unit_tests():
    """Run unit tests"""
    print("\nRunning unit tests...")
    success, stdout, stderr = run_cmd("python3 run_tests.py 2>&1")
    output = stdout + stderr
    
    if success and "OK" in output:
        lines = output.split('\n')
        for line in lines:
            if "Ran" in line:
                print(f"  ✓ {line.strip()}")
                break
        return True
    else:
        print("  ✗ Tests failed")
        return False

def test_file_structure():
    """Verify file structure"""
    print("\nVerifying file structure...")
    required_files = [
        "src/pygubuai/__init__.py",
        "src/pygubuai/create.py",
        "src/pygubuai/register.py",
        "src/pygubuai/template.py",
        "src/pygubuai/workflow.py",
        "src/pygubuai/config.py",
        "src/pygubuai/errors.py",
        "src/pygubuai/registry.py",
        "pyproject.toml",
        "README.md",
        "CONTRIBUTING.md",
        ".editorconfig",
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            all_ok = False
    
    return all_ok

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("PygubuAI Installation Verification")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Version Flags", test_version_flags()))
    results.append(("Unit Tests", test_unit_tests()))
    results.append(("File Structure", test_file_structure()))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status:8} {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All verification tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
