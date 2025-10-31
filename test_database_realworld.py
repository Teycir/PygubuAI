#!/usr/bin/env python3
"""Real-world test with SQLAlchemy installed"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, 'src')

def test_database_init():
    """Test database initialization"""
    print("=" * 60)
    print("TEST 1: Database Initialization")
    print("=" * 60)
    
    try:
        from pygubuai.db import init_db, get_session, SQLALCHEMY_AVAILABLE
        
        print(f"SQLAlchemy available: {SQLALCHEMY_AVAILABLE}")
        
        if not SQLALCHEMY_AVAILABLE:
            print("SKIP: SQLAlchemy not installed")
            return False
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            
            result = init_db(db_path)
            print(f"init_db() returned: {result}")
            print(f"Database file exists: {db_path.exists()}")
            
            session = get_session()
            print(f"Session created: {session is not None}")
            
            if session:
                session.close()
            
            return result and db_path.exists()
            
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_crud_operations():
    """Test CRUD operations"""
    print("\n" + "=" * 60)
    print("TEST 2: CRUD Operations")
    print("=" * 60)
    
    try:
        from pygubuai.db import init_db, get_session, SQLALCHEMY_AVAILABLE
        from pygubuai.db.operations import (
            create_project, get_project, list_projects,
            update_project, delete_project
        )
        
        if not SQLALCHEMY_AVAILABLE:
            print("SKIP: SQLAlchemy not installed")
            return False
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            init_db(db_path)
            session = get_session()
            
            # Create
            project = create_project(session, "test1", "/path/to/test1", "Test project")
            print(f"Created project: {project.name if project else None}")
            
            # Read
            found = get_project(session, "test1")
            print(f"Found project: {found.name if found else None}")
            
            # List
            projects = list_projects(session)
            print(f"Total projects: {len(projects)}")
            
            # Update
            updated = update_project(session, "test1", description="Updated")
            print(f"Updated project: {updated}")
            
            # Delete
            deleted = delete_project(session, "test1")
            print(f"Deleted project: {deleted}")
            
            session.close()
            
            return project and found and len(projects) == 1 and updated and deleted
            
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_events():
    """Test workflow event tracking"""
    print("\n" + "=" * 60)
    print("TEST 3: Workflow Events")
    print("=" * 60)
    
    try:
        from pygubuai.db import init_db, get_session, SQLALCHEMY_AVAILABLE
        from pygubuai.db.operations import (
            create_project, add_workflow_event, get_workflow_events
        )
        
        if not SQLALCHEMY_AVAILABLE:
            print("SKIP: SQLAlchemy not installed")
            return False
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            init_db(db_path)
            session = get_session()
            
            create_project(session, "test1", "/path/to/test1")
            
            # Add events
            add_workflow_event(session, "test1", "create", "Created project")
            add_workflow_event(session, "test1", "update", "Updated UI")
            
            # Get events
            events = get_workflow_events(session, "test1")
            print(f"Total events: {len(events)}")
            
            for event in events:
                print(f"  - {event.action}: {event.description}")
            
            session.close()
            
            return len(events) == 2
            
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """Test template operations"""
    print("\n" + "=" * 60)
    print("TEST 4: Template Operations")
    print("=" * 60)
    
    try:
        from pygubuai.db import init_db, get_session, SQLALCHEMY_AVAILABLE
        from pygubuai.db.operations import create_template, search_templates
        
        if not SQLALCHEMY_AVAILABLE:
            print("SKIP: SQLAlchemy not installed")
            return False
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            init_db(db_path)
            session = get_session()
            
            # Create templates
            t1 = create_template(session, "login", "<ui>login</ui>", 
                                description="Login form", author="test")
            t2 = create_template(session, "signup", "<ui>signup</ui>",
                                description="Signup form", author="test")
            
            print(f"Created templates: {t1.name if t1 else None}, {t2.name if t2 else None}")
            
            # Search
            results = search_templates(session, "login")
            print(f"Search results for 'login': {len(results)}")
            
            session.close()
            
            return t1 and t2 and len(results) >= 1
            
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_analytics():
    """Test analytics recording"""
    print("\n" + "=" * 60)
    print("TEST 5: Analytics")
    print("=" * 60)
    
    try:
        from pygubuai.db import init_db, get_session, SQLALCHEMY_AVAILABLE
        from pygubuai.db.operations import create_project, record_analytics
        
        if not SQLALCHEMY_AVAILABLE:
            print("SKIP: SQLAlchemy not installed")
            return False
        
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            init_db(db_path)
            session = get_session()
            
            create_project(session, "test1", "/path/to/test1")
            
            # Record metrics
            r1 = record_analytics(session, "widget_count", 10.0, "test1")
            r2 = record_analytics(session, "complexity", 5.5, "test1")
            
            print(f"Recorded analytics: {r1}, {r2}")
            
            session.close()
            
            return r1 and r2
            
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all real-world tests"""
    print("\n" + "=" * 60)
    print("DATABASE REAL-WORLD TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Database Init", test_database_init()))
    results.append(("CRUD Operations", test_crud_operations()))
    results.append(("Workflow Events", test_workflow_events()))
    results.append(("Templates", test_templates()))
    results.append(("Analytics", test_analytics()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nALL TESTS PASSED - Database fully functional")
        return 0
    else:
        print("\nSOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
