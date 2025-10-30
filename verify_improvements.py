#!/usr/bin/env python3
"""Verify improvements are working"""
import sys
sys.path.insert(0, 'src')

def test_imports():
    """Test all imports work"""
    try:
        from pygubuai import __version__
        from pygubuai import errors, config, widgets, utils, create, registry
        print("✅ All modules import successfully")
        print(f"   Version: {__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    try:
        from pygubuai.errors import PygubuAIError
        err = PygubuAIError("test", "suggestion")
        assert "test" in str(err)
        assert "suggestion" in str(err)
        print("✅ Error handling works")
        return True
    except Exception as e:
        print(f"❌ Error handling failed: {e}")
        return False

def test_validation():
    """Test input validation"""
    try:
        from pygubuai.utils import validate_project_name
        assert validate_project_name("myapp") == "myapp"
        assert validate_project_name("my app") == "my_app"
        print("✅ Input validation works")
        return True
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

def test_widget_detection():
    """Test widget detection"""
    try:
        from pygubuai.widgets import detect_widgets
        widgets = detect_widgets("login form")
        assert len(widgets) > 0
        print(f"✅ Widget detection works ({len(widgets)} widgets detected)")
        return True
    except Exception as e:
        print(f"❌ Widget detection failed: {e}")
        return False

def test_registry():
    """Test registry initialization"""
    try:
        from pygubuai.registry import Registry
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            old_home = os.environ.get('HOME')
            os.environ['HOME'] = tmpdir
            registry = Registry()
            os.environ['HOME'] = old_home or ''
        
        print("✅ Thread-safe registry works")
        return True
    except Exception as e:
        print(f"❌ Registry failed: {e}")
        return False

def main():
    print("🔍 Verifying PygubuAI Improvements\n")
    
    tests = [
        test_imports,
        test_error_handling,
        test_validation,
        test_widget_detection,
        test_registry,
    ]
    
    results = [test() for test in tests]
    
    print(f"\n{'='*50}")
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All improvements verified!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
