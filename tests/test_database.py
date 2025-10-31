"""Tests for database functionality"""
import pytest
from pathlib import Path

try:
    from pygubuai.db import init_db, get_session, SQLALCHEMY_AVAILABLE
    from pygubuai.db.operations import (
        create_project, get_project, list_projects,
        add_workflow_event, get_workflow_events,
        create_template, search_templates,
        record_analytics
    )
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    pytestmark = pytest.mark.skip("SQLAlchemy not installed")

@pytest.fixture
def db_session(tmp_path):
    """Create test database session"""
    if not SQLALCHEMY_AVAILABLE:
        pytest.skip("SQLAlchemy not installed")
    
    db_path = tmp_path / "test.db"
    init_db(db_path)
    session = get_session()
    yield session
    session.close()

@pytest.mark.skipif(not SQLALCHEMY_AVAILABLE, reason="SQLAlchemy not installed")
class TestDatabase:
    def test_create_project(self, db_session):
        project = create_project(db_session, "test", "/path/to/test", "Test project")
        assert project is not None
        assert project.name == "test"
        assert project.path == "/path/to/test"
    
    def test_get_project(self, db_session):
        create_project(db_session, "test", "/path/to/test")
        project = get_project(db_session, "test")
        assert project is not None
        assert project.name == "test"
    
    def test_list_projects(self, db_session):
        create_project(db_session, "test1", "/path/1")
        create_project(db_session, "test2", "/path/2")
        projects = list_projects(db_session)
        assert len(projects) == 2
    
    def test_workflow_events(self, db_session):
        create_project(db_session, "test", "/path/to/test")
        add_workflow_event(db_session, "test", "create", "Created project")
        events = get_workflow_events(db_session, "test")
        assert len(events) == 1
        assert events[0].action == "create"
    
    def test_create_template(self, db_session):
        template = create_template(
            db_session,
            "login",
            "<ui>...</ui>",
            description="Login form",
            author="test"
        )
        assert template is not None
        assert template.name == "login"
    
    def test_search_templates(self, db_session):
        create_template(db_session, "login", "<ui>...</ui>", description="Login form")
        create_template(db_session, "signup", "<ui>...</ui>", description="Signup form")
        results = search_templates(db_session, "login")
        assert len(results) >= 1
        assert results[0].name == "login"
    
    def test_analytics(self, db_session):
        create_project(db_session, "test", "/path/to/test")
        success = record_analytics(db_session, "widget_count", 10.0, "test")
        assert success is True
