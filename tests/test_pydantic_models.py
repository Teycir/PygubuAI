"""Tests for Pydantic models"""
import pytest
from pathlib import Path

try:
    from pydantic import ValidationError
    from pygubuai.models import ProjectConfig, RegistryData, WorkflowData, WorkflowHistory
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    pytestmark = pytest.mark.skip("Pydantic not installed")

@pytest.mark.skipif(not PYDANTIC_AVAILABLE, reason="Pydantic not installed")
class TestProjectConfig:
    def test_valid_project(self, tmp_path):
        config = ProjectConfig(name="test", path=str(tmp_path))
        assert config.name == "test"
        assert Path(config.path).exists()
    
    def test_invalid_path(self):
        with pytest.raises(ValidationError):
            ProjectConfig(name="test", path="/nonexistent/path")
    
    def test_metadata_defaults(self, tmp_path):
        config = ProjectConfig(name="test", path=str(tmp_path))
        assert config.metadata == {}
        assert config.created > 0
        assert config.last_modified > 0

@pytest.mark.skipif(not PYDANTIC_AVAILABLE, reason="Pydantic not installed")
class TestRegistryData:
    def test_empty_registry(self):
        registry = RegistryData()
        assert registry.projects == {}
        assert registry.active is None
        assert registry.version == "1.0"
    
    def test_with_projects(self):
        registry = RegistryData(
            projects={"test": "/path/to/test"},
            active="test"
        )
        assert "test" in registry.projects
        assert registry.active == "test"
    
    def test_invalid_active(self):
        with pytest.raises(ValidationError):
            RegistryData(
                projects={"test": "/path"},
                active="nonexistent"
            )

@pytest.mark.skipif(not PYDANTIC_AVAILABLE, reason="Pydantic not installed")
class TestWorkflowData:
    def test_empty_workflow(self):
        workflow = WorkflowData(project="test")
        assert workflow.project == "test"
        assert workflow.history == []
        assert workflow.last_sync is None
    
    def test_with_history(self):
        history = WorkflowHistory(
            timestamp="2024-01-01T00:00:00",
            action="create",
            description="Created project"
        )
        workflow = WorkflowData(
            project="test",
            history=[history]
        )
        assert len(workflow.history) == 1
        assert workflow.history[0].action == "create"
    
    def test_serialization(self):
        workflow = WorkflowData(project="test")
        data = workflow.model_dump()
        assert data["project"] == "test"
        assert "history" in data
        assert "version" in data
