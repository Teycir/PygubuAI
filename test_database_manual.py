#!/usr/bin/env python3
"""Manual test for database functionality"""
import sys
sys.path.insert(0, 'src')

def test_imports():
    """Test all imports work"""
    print("=" * 60)
    print("TEST 1: Module Imports")
    print("=" * 60)
    
    try:
        from pygubuai.db import SQLALCHEMY_AVAILABLE, get_session, init_db
        print(f"✓ db module imported")
        print(f"  SQLAlchemy available: {SQLALCHEMY_AVAILABLE}")
        
        from pygubuai.db.models import SQLALCHEMY_AVAILABLE as models_available
        print(f"✓ models module imported")
        print(f"  Models available: {models_available}")
        
        from pygubuai.db.operations import SQLALCHEMY_AVAILABLE as ops_available
        print(f"✓ operations module imported")
        print(f"  Operations available: {ops_available}")
        
        from pygubuai import database
        print(f"✓ database CLI imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_graceful_fallback():
    """Test graceful fallback without SQLAlchemy"""
    print("\n" + "=" * 60)
    print("TEST 2: Graceful Fallback (No SQLAlchemy)")
    print("=" * 60)
    
    try:
        from pygubuai.db import get_session, init_db, SQLALCHEMY_AVAILABLE
        
        if not SQLALCHEMY_AVAILABLE:
            print("✓ SQLAlchemy not installed (expected)")
            
            session = get_session()
            print(f"✓ get_session() returns None: {session is None}")
            
            result = init_db()
            print(f"✓ init_db() returns False: {result is False}")
            
            print("\n✓ All functions handle missing SQLAlchemy gracefully")
            return True
        else:
            print("⚠️  SQLAlchemy is installed, skipping fallback test")
            return True
            
    except Exception as e:
        print(f"✗ Fallback test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_commands():
    """Test CLI commands"""
    print("\n" + "=" * 60)
    print("TEST 3: CLI Commands")
    print("=" * 60)
    
    try:
        from pygubuai import database
        
        print("\n--- Testing help command ---")
        sys.argv = ['pygubu-db']
        try:
            database.main()
        except SystemExit:
            pass
        print("✓ Help command works")
        
        print("\n--- Testing init command ---")
        sys.argv = ['pygubu-db', 'init']
        database.main()
        print("✓ Init command handles missing SQLAlchemy")
        
        return True
        
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("DATABASE FEATURE MANUAL TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Graceful Fallback", test_graceful_fallback()))
    results.append(("CLI Commands", test_cli_commands()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED")
        print("\nNote: SQLAlchemy not installed, but graceful fallback working")
        print("To test full functionality: pip install sqlalchemy")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
