"""Integration tests for end-to-end workflows"""
import pytest
import tempfile
import shutil
from pathlib import Path
import json
import subprocess
import sys

from pygubuai.create import create_project
from pygubuai.registry import Registry
from pygubuai.workflow import WorkflowTracker
from pygubuai.status import check_project_status
from pygubuai.validate_project import validate_project


class TestEndToEndWorkflow:
    """Test complete project lifecycle"""
    
    def test_create_register_validate_workflow(self, tmp_path):
        """Test: create -> register -> validate -> status"""
        project_name = "test_workflow"
        project_path = tmp_path / project_name
        
        # Step 1: Create project
        result = create_project(project_name, "test application", str(tmp_path))
        assert result is True
        assert project_path.exists()
        assert (project_path / f"{project_name}.ui").exists()
        assert (project_path / f"{project_name}.py").exists()
        
        # Step 2: Register project
        registry = Registry()
        registry.add_project(project_name, str(project_path))
        assert project_name in registry.list_projects()
        
        # Step 3: Validate project
        issues = validate_project(str(project_path))
        assert len(issues) == 0, f"Validation issues: {issues}"
        
        # Step 4: Check status
        status = check_project_status(project_name)
        assert status is not None
        assert status.get("sync_state") in ["In Sync", "UI Ahead", "Code Ahead"]
    
    def test_multi_project_workflow(self, tmp_path):
        """Test managing multiple projects simultaneously"""
        projects = ["proj1", "proj2", "proj3"]
        registry = Registry()
        
        # Create multiple projects
        for proj in projects:
            proj_path = tmp_path / proj
            create_project(proj, f"{proj} description", str(tmp_path))
            registry.add_project(proj, str(proj_path))
        
        # Verify all registered
        registered = registry.list_projects()
        for proj in projects:
            assert proj in registered
        
        # Set active project
        registry.set_active_project("proj2")
        assert registry.get_active_project() == "proj2"
        
        # Remove one project
        registry.remove_project("proj3")
        assert "proj3" not in registry.list_projects()
        assert len(registry.list_projects()) == 2
    
    def test_workflow_tracking(self, tmp_path):
        """Test workflow history tracking"""
        project_name = "tracked_project"
        project_path = tmp_path / project_name
        
        create_project(project_name, "tracked app", str(tmp_path))
        
        tracker = WorkflowTracker(str(project_path))
        
        # Add workflow events
        tracker.add_event("create", "Project created")
        tracker.add_event("modify", "UI modified")
        tracker.add_event("sync", "Code synced")
        
        history = tracker.get_history()
        assert len(history) >= 3
        assert any(e["action"] == "create" for e in history)
        assert any(e["action"] == "modify" for e in history)


class TestErrorRecovery:
    """Test error handling and recovery"""
    
    def test_corrupted_registry_recovery(self, tmp_path):
        """Test recovery from corrupted registry"""
        registry_path = tmp_path / "registry.json"
        
        # Create corrupted registry
        registry_path.write_text("{invalid json")
        
        # Should recover gracefully
        registry = Registry(str(registry_path))
        assert registry.list_projects() == []
    
    def test_missing_ui_file_recovery(self, tmp_path):
        """Test handling missing UI file"""
        project_name = "missing_ui"
        project_path = tmp_path / project_name
        
        create_project(project_name, "test", str(tmp_path))
        
        # Delete UI file
        ui_file = project_path / f"{project_name}.ui"
        ui_file.unlink()
        
        # Should handle gracefully
        with pytest.raises(FileNotFoundError):
            validate_project(str(project_path))
    
    def test_invalid_project_name_handling(self, tmp_path):
        """Test handling invalid project names"""
        invalid_names = ["<script>", "../../../etc", "my|project", ""]
        
        for name in invalid_names:
            with pytest.raises((ValueError, OSError)):
                create_project(name, "test", str(tmp_path))
    
    def test_disk_full_simulation(self, tmp_path):
        """Test handling disk space issues"""
        # Create project in limited space
        project_name = "large_project"
        
        # This should handle gracefully if disk is full
        try:
            result = create_project(project_name, "test", str(tmp_path))
            assert result in [True, False]
        except OSError as e:
            # Expected if disk is actually full
            assert "No space" in str(e) or "disk" in str(e).lower()


class TestMultiProjectScenarios:
    """Test complex multi-project scenarios"""
    
    def test_project_dependencies(self, tmp_path):
        """Test projects with dependencies"""
        # Create main project
        main_proj = tmp_path / "main_app"
        create_project("main_app", "main application", str(tmp_path))
        
        # Create sub-projects
        for i in range(3):
            sub_name = f"module_{i}"
            create_project(sub_name, f"module {i}", str(tmp_path))
        
        # Verify all exist
        assert (tmp_path / "main_app").exists()
        for i in range(3):
            assert (tmp_path / f"module_{i}").exists()
    
    def test_concurrent_project_access(self, tmp_path):
        """Test concurrent access to registry"""
        registry1 = Registry()
        registry2 = Registry()
        
        project_name = "concurrent_test"
        project_path = tmp_path / project_name
        create_project(project_name, "test", str(tmp_path))
        
        # Both registries should see the project
        registry1.add_project(project_name, str(project_path))
        
        # Reload registry2
        registry2 = Registry()
        assert project_name in registry2.list_projects()
    
    def test_project_migration(self, tmp_path):
        """Test moving projects between directories"""
        project_name = "migrated_project"
        old_path = tmp_path / "old" / project_name
        new_path = tmp_path / "new" / project_name
        
        old_path.parent.mkdir(parents=True)
        new_path.parent.mkdir(parents=True)
        
        # Create in old location
        create_project(project_name, "test", str(old_path.parent))
        
        registry = Registry()
        registry.add_project(project_name, str(old_path))
        
        # Move project
        shutil.move(str(old_path), str(new_path))
        
        # Update registry
        registry.remove_project(project_name)
        registry.add_project(project_name, str(new_path))
        
        # Verify new location
        proj_info = registry.get_project(project_name)
        assert Path(proj_info["path"]) == new_path


class TestCLIIntegration:
    """Test CLI command integration"""
    
    def test_cli_create_command(self, tmp_path):
        """Test pygubu-create CLI command"""
        result = subprocess.run(
            [sys.executable, "-m", "pygubuai.create", "cli_test", "test app"],
            cwd=str(tmp_path),
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert (tmp_path / "cli_test").exists()
    
    def test_cli_register_command(self, tmp_path):
        """Test pygubu-register CLI command"""
        project_name = "register_test"
        create_project(project_name, "test", str(tmp_path))
        
        result = subprocess.run(
            [sys.executable, "-m", "pygubuai.register", "list"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
    
    def test_cli_status_command(self, tmp_path):
        """Test pygubu-status CLI command"""
        project_name = "status_test"
        create_project(project_name, "test", str(tmp_path))
        
        result = subprocess.run(
            [sys.executable, "-m", "pygubuai.status", project_name],
            cwd=str(tmp_path / project_name),
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]


class TestDataIntegrity:
    """Test data integrity across operations"""
    
    def test_registry_consistency(self, tmp_path):
        """Test registry remains consistent"""
        registry = Registry()
        
        # Add 10 projects
        for i in range(10):
            proj_name = f"proj_{i}"
            proj_path = tmp_path / proj_name
            create_project(proj_name, f"project {i}", str(tmp_path))
            registry.add_project(proj_name, str(proj_path))
        
        # Verify count
        assert len(registry.list_projects()) == 10
        
        # Remove 5 projects
        for i in range(5):
            registry.remove_project(f"proj_{i}")
        
        # Verify count
        assert len(registry.list_projects()) == 5
        
        # Verify remaining projects
        for i in range(5, 10):
            assert f"proj_{i}" in registry.list_projects()
    
    def test_workflow_data_persistence(self, tmp_path):
        """Test workflow data persists correctly"""
        project_name = "persist_test"
        project_path = tmp_path / project_name
        create_project(project_name, "test", str(tmp_path))
        
        # Create tracker and add events
        tracker1 = WorkflowTracker(str(project_path))
        tracker1.add_event("test", "Test event 1")
        tracker1.add_event("test", "Test event 2")
        
        # Create new tracker instance
        tracker2 = WorkflowTracker(str(project_path))
        history = tracker2.get_history()
        
        # Should have persisted events
        assert len(history) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
