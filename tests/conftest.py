"""Shared pytest fixtures and configuration."""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch


@pytest.fixture
def temp_project():
    """
    Create a temporary project directory.
    
    Yields:
        Path: Temporary project directory that's automatically cleaned up
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "testproj"
        project_dir.mkdir()
        yield project_dir


@pytest.fixture
def temp_registry(temp_project):
    """
    Create a temporary registry file.
    
    Yields:
        Path: Temporary registry file path
    """
    registry_file = temp_project.parent / "registry.json"
    yield registry_file


@pytest.fixture
def mock_registry(temp_project):
    """
    Mock Registry with test project.
    
    Yields:
        MagicMock: Mocked Registry instance
    """
    with patch('pygubuai.workflow.Registry') as MockRegistry:
        mock_instance = MagicMock()
        mock_instance.list_projects.return_value = {
            'test': str(temp_project)
        }
        MockRegistry.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def ui_file(temp_project):
    """
    Create a test UI file.
    
    Args:
        temp_project: Temporary project directory fixture
        
    Returns:
        Path: Path to created UI file
    """
    ui_file = temp_project / "test.ui"
    ui_file.write_text("<interface></interface>")
    return ui_file


@pytest.fixture
def workflow_file(temp_project):
    """
    Create a test workflow file.
    
    Args:
        temp_project: Temporary project directory fixture
        
    Returns:
        Path: Path to workflow file
    """
    workflow_file = temp_project / ".pygubu-workflow.json"
    return workflow_file


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (slower, multiple components)"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests (>1s runtime)"
    )
    config.addinivalue_line(
        "markers", "security: Security-critical tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance benchmarks"
    )
    config.addinivalue_line(
        "markers", "cli: CLI integration tests"
    )
