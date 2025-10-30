#!/usr/bin/env python3
"""Verify cross-platform compatibility improvements."""
import sys
import tempfile
from pathlib import Path

def test_registry_import():
    """Test that registry imports correctly on this platform."""
    try:
        from src.pygubuai.registry import Registry
        print(f"✅ Registry imports successfully on {sys.platform}")
        return True
    except ImportError as e:
        print(f"❌ Registry import failed: {e}")
        return False

def test_platform_detection():
    """Test platform-specific imports."""
    print(f"\n📋 Platform: {sys.platform}")
    
    if sys.platform == 'win32':
        try:
            import msvcrt
            print("✅ msvcrt available (Windows)")
            return True
        except ImportError:
            print("❌ msvcrt not available")
            return False
    else:
        try:
            import fcntl
            print("✅ fcntl available (Unix/Linux/macOS)")
            return True
        except ImportError:
            print("❌ fcntl not available")
            return False

def test_registry_operations():
    """Test basic registry operations."""
    try:
        from src.pygubuai.registry import Registry
        
        # Create temporary registry
        with tempfile.TemporaryDirectory() as tmpdir:
            registry_file = Path(tmpdir) / "test_registry.json"
            Registry.REGISTRY_FILE = registry_file
            
            # Test operations
            registry = Registry()
            registry.add_project("test_project", tmpdir)
            
            projects = registry.list_projects()
            assert "test_project" in projects
            
            path = registry.get_project("test_project")
            assert path is not None
            
            print("✅ Registry operations work correctly")
            return True
            
    except Exception as e:
        print(f"❌ Registry operations failed: {e}")
        return False
    finally:
        Registry.REGISTRY_FILE = None

def test_ci_workflow():
    """Verify CI workflow configuration."""
    try:
        import yaml
        
        with open('.github/workflows/ci.yml') as f:
            config = yaml.safe_load(f)
        
        # Check for multi-OS testing
        matrix = config['jobs']['test']['strategy']['matrix']
        
        expected_os = ['ubuntu-latest', 'windows-latest', 'macos-latest']
        actual_os = matrix.get('os', [])
        
        if set(expected_os) == set(actual_os):
            print(f"✅ CI tests on: {', '.join(actual_os)}")
        else:
            print(f"⚠️  CI OS mismatch. Expected: {expected_os}, Got: {actual_os}")
        
        # Check for Python versions
        python_versions = matrix.get('python-version', [])
        print(f"✅ CI tests Python: {', '.join(python_versions)}")
        
        # Check for quality checks
        steps = config['jobs']['test']['steps']
        step_names = [step.get('name', '') for step in steps]
        
        checks = {
            'linters': any('lint' in name.lower() for name in step_names),
            'type_check': any('type' in name.lower() for name in step_names),
            'tests': any('test' in name.lower() for name in step_names),
        }
        
        for check, present in checks.items():
            status = "✅" if present else "❌"
            print(f"{status} CI includes {check}")
        
        return all(checks.values())
        
    except Exception as e:
        print(f"❌ CI workflow check failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🔍 Verifying Cross-Platform Improvements\n")
    print("=" * 60)
    
    results = []
    
    print("\n1️⃣  Testing Registry Import")
    print("-" * 60)
    results.append(test_registry_import())
    
    print("\n2️⃣  Testing Platform Detection")
    print("-" * 60)
    results.append(test_platform_detection())
    
    print("\n3️⃣  Testing Registry Operations")
    print("-" * 60)
    results.append(test_registry_operations())
    
    print("\n4️⃣  Testing CI Configuration")
    print("-" * 60)
    results.append(test_ci_workflow())
    
    print("\n" + "=" * 60)
    print(f"\n📊 Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("\n✅ All cross-platform improvements verified!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
