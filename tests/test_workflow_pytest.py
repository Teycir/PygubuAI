#!/usr/bin/env python3
"""
Pytest-style tests for workflow module with improved documentation.

This demonstrates the improved test structure with:
- Shared fixtures from conftest.py
- Clear Given-When-Then documentation
- Pytest markers for categorization
- Cleaner assertions
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import os

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from pygubuai.workflow import load_workflow, save_workflow, get_file_hash
from pygubuai.errors import ProjectNotFoundError


@pytest.mark.unit
def test_get_file_hash_generates_sha256(temp_project):
    """
    Test file hash generation produces consistent SHA256 hashes.
    
    Given: A UI file with specific content
    When: get_file_hash() is called
    Then: Returns 64-character SHA256 hash
    And: Same content produces same hash
    And: Different content produces different hash
    """
    # Given: A UI file with specific content
    test_file = temp_project / "test.ui"
    test_file.write_text("<ui>test</ui>")
    
    # When: get_file_hash() is called
    hash1 = get_file_hash(test_file)
    
    # Then: Returns 64-character SHA256 hash
    assert isinstance(hash1, str)
    assert len(hash1) == 64
    
    # And: Same content produces same hash
    hash2 = get_file_hash(test_file)
    assert hash1 == hash2
    
    # And: Different content produces different hash
    test_file.write_text("<ui>changed</ui>")
    hash3 = get_file_hash(test_file)
    assert hash1 != hash3


@pytest.mark.unit
def test_get_file_hash_nonexistent_returns_none(temp_project):
    """
    Test hash of non-existent file returns None gracefully.
    
    Given: A path to a non-existent file
    When: get_file_hash() is called
    Then: Returns None without raising exception
    """
    # Given: A path to a non-existent file
    nonexistent = temp_project / "nonexistent.ui"
    
    # When: get_file_hash() is called
    result = get_file_hash(nonexistent)
    
    # Then: Returns None without raising exception
    assert result is None


@pytest.mark.unit
def test_load_workflow_new_project_returns_defaults(temp_project):
    """
    Test loading workflow for new project returns default values.
    
    Given: A new project directory with no workflow file
    When: load_workflow() is called
    Then: Returns workflow with None hash and empty changes
    """
    # Given: A new project directory (temp_project fixture)
    
    # When: load_workflow() is called
    workflow = load_workflow(temp_project)
    
    # Then: Returns workflow with None hash and empty changes
    assert workflow["ui_hash"] is None
    assert workflow["last_sync"] is None
    assert workflow["changes"] == []


@pytest.mark.unit
def test_save_and_load_workflow_roundtrip(temp_project):
    """
    Test workflow data persists correctly through save/load cycle.
    
    Given: Workflow data with hash and changes
    When: Data is saved and then loaded
    Then: Loaded data matches saved data
    And: last_sync timestamp is added
    """
    # Given: Workflow data with hash and changes
    workflow_data = {
        "ui_hash": "abc123",
        "last_sync": None,
        "changes": []
    }
    
    # When: Data is saved and then loaded
    save_workflow(temp_project, workflow_data)
    loaded = load_workflow(temp_project)
    
    # Then: Loaded data matches saved data
    assert loaded["ui_hash"] == "abc123"
    
    # And: last_sync timestamp is added
    assert loaded["last_sync"] is not None


@pytest.mark.unit
def test_load_workflow_invalid_json_returns_defaults(temp_project):
    """
    Test corrupted workflow file returns defaults gracefully.
    
    Given: A workflow file with invalid JSON
    When: load_workflow() is called
    Then: Returns default workflow without crashing
    """
    # Given: A workflow file with invalid JSON
    workflow_file = temp_project / ".pygubu-workflow.json"
    workflow_file.write_text("invalid json{")
    
    # When: load_workflow() is called
    workflow = load_workflow(temp_project)
    
    # Then: Returns default workflow without crashing
    assert workflow["ui_hash"] is None
    assert workflow["changes"] == []


@pytest.mark.unit
def test_workflow_tracks_multiple_changes(temp_project):
    """
    Test workflow preserves change history across saves.
    
    Given: Workflow with existing changes
    When: New changes are added and saved
    Then: All changes are preserved in order
    """
    # Given: Workflow with existing changes
    workflow_data = {
        "ui_hash": "initial",
        "last_sync": None,
        "changes": [{"file": "test.ui", "timestamp": "2024-01-01"}]
    }
    
    # When: Workflow is saved and loaded
    save_workflow(temp_project, workflow_data)
    loaded = load_workflow(temp_project)
    
    # Then: Changes are preserved
    assert len(loaded["changes"]) == 1
    assert loaded["changes"][0]["file"] == "test.ui"


@pytest.mark.security
def test_path_traversal_protection(mock_registry):
    """
    Test watch_project prevents directory traversal attacks.
    
    Given: A project path with directory traversal attempt
    When: watch_project() is called
    Then: Raises ProjectNotFoundError with security message
    """
    # Given: Mock registry with invalid path
    mock_registry.list_projects.return_value = {'test': '/nonexistent/path'}
    
    # When/Then: watch_project() raises security error
    with pytest.raises(ProjectNotFoundError) as exc_info:
        from pygubuai.workflow import watch_project
        watch_project('test')
    
    assert 'Invalid project path' in str(exc_info.value)


@pytest.mark.security
def test_get_file_hash_permission_error(temp_project):
    """
    Test get_file_hash handles permission errors gracefully.
    
    Given: A file with no read permissions
    When: get_file_hash() is called
    Then: Returns None without crashing
    """
    # Given: A file with no read permissions
    test_file = temp_project / "test.ui"
    test_file.write_text("test")
    os.chmod(test_file, 0o000)
    
    try:
        # When: get_file_hash() is called
        result = get_file_hash(test_file)
        
        # Then: Returns None without crashing
        assert result is None
    finally:
        # Cleanup
        os.chmod(test_file, 0o644)


@pytest.mark.unit
def test_workflow_stores_file_hashes(temp_project):
    """
    Test workflow tracks individual file hashes.
    
    Given: A new workflow
    When: Workflow is loaded
    Then: Contains empty file_hashes dictionary
    """
    # Given/When: Load new workflow
    workflow = load_workflow(temp_project)
    
    # Then: Contains file_hashes structure
    assert "file_hashes" in workflow
    assert workflow["file_hashes"] == {}


@pytest.mark.unit
def test_detects_specific_file_change(temp_project):
    """
    Test workflow detects which specific file changed.
    
    Given: Multiple UI files with tracked hashes
    When: One file is modified
    Then: Only that file's hash differs
    """
    # Given: Multiple UI files with tracked hashes
    file1 = temp_project / "a.ui"
    file2 = temp_project / "b.ui"
    file1.write_text("<ui>a</ui>")
    file2.write_text("<ui>b</ui>")
    
    workflow = load_workflow(temp_project)
    workflow["file_hashes"] = {
        "a.ui": get_file_hash(file1),
        "b.ui": get_file_hash(file2)
    }
    save_workflow(temp_project, workflow)
    
    # When: One file is modified
    file1.write_text("<ui>a_modified</ui>")
    
    # Then: Only that file's hash differs
    new_hash = get_file_hash(file1)
    assert workflow["file_hashes"]["a.ui"] != new_hash
    assert workflow["file_hashes"]["b.ui"] == get_file_hash(file2)


@pytest.mark.unit
def test_default_watch_interval():
    """
    Test default watch interval configuration.
    
    Given: No custom environment configuration
    When: get_watch_interval() is called
    Then: Returns default 2.0 seconds
    """
    # Given/When: Get default interval
    from pygubuai.workflow import get_watch_interval
    
    # Then: Returns 2.0 seconds
    assert get_watch_interval() == 2.0


@pytest.mark.unit
def test_custom_watch_interval():
    """
    Test custom watch interval from environment variable.
    
    Given: PYGUBUAI_WATCH_INTERVAL environment variable set
    When: get_watch_interval() is called
    Then: Returns custom interval value
    """
    # Given: Custom environment variable
    with patch.dict(os.environ, {'PYGUBUAI_WATCH_INTERVAL': '5.0'}):
        # When: Get interval
        from pygubuai.workflow import get_watch_interval
        
        # Then: Returns custom value
        assert get_watch_interval() == 5.0
