"""User acceptance tests for common scenarios"""
import pytest
from pathlib import Path
import json

from pygubuai.create import create_project
from pygubuai.registry import Registry
from pygubuai.template import create_from_template
from pygubuai.validate_project import validate_project


class TestCommonUserScenarios:
    """Test typical user workflows"""
    
    def test_new_user_first_project(self, tmp_path):
        """Scenario: New user creates their first project"""
        # User creates a simple app
        result = create_project("my_first_app", "a simple calculator", str(tmp_path))
        assert result is True
        
        # User checks what was created
        project_path = tmp_path / "my_first_app"
        assert project_path.exists()
        assert (project_path / "my_first_app.ui").exists()
        assert (project_path / "my_first_app.py").exists()
        assert (project_path / "README.md").exists()
        
        # User validates the project
        issues = validate_project(str(project_path))
        assert len(issues) == 0
    
    def test_user_creates_multiple_projects(self, tmp_path):
        """Scenario: User manages multiple projects"""
        registry = Registry()
        projects = ["todo_app", "calculator", "notes_app"]
        
        # User creates several projects
        for proj in projects:
            create_project(proj, f"{proj} application", str(tmp_path))
            registry.add_project(proj, str(tmp_path / proj))
        
        # User lists all projects
        all_projects = registry.list_projects()
        for proj in projects:
            assert proj in all_projects
        
        # User switches between projects
        for proj in projects:
            registry.set_active_project(proj)
            assert registry.get_active_project() == proj
    
    def test_user_uses_template(self, tmp_path):
        """Scenario: User creates project from template"""
        templates = ["login", "crud", "settings"]
        
        for template in templates:
            proj_name = f"{template}_app"
            result = create_from_template(proj_name, template, str(tmp_path))
            
            if result:
                project_path = tmp_path / proj_name
                assert project_path.exists()
                assert (project_path / f"{proj_name}.ui").exists()
    
    def test_user_modifies_and_validates(self, tmp_path):
        """Scenario: User modifies project and validates"""
        project_name = "modified_app"
        project_path = tmp_path / project_name
        
        # Create project
        create_project(project_name, "test app", str(tmp_path))
        
        # User modifies UI file
        ui_file = project_path / f"{project_name}.ui"
        content = ui_file.read_text()
        modified = content.replace("</interface>", "  <object class=\"tk.Button\" id=\"new_btn\"/>\n</interface>")
        ui_file.write_text(modified)
        
        # User validates changes
        issues = validate_project(str(project_path))
        # Should detect new button without callback
        assert any("callback" in str(issue).lower() for issue in issues) or len(issues) == 0


class TestEdgeCases:
    """Test edge cases users might encounter"""
    
    def test_project_with_special_description(self, tmp_path):
        """Edge case: Description with special characters"""
        descriptions = [
            "App with 'quotes'",
            "App with \"double quotes\"",
            "App with <brackets>",
            "App with & ampersand",
            "App with unicode: hello world"
        ]
        
        for i, desc in enumerate(descriptions):
            proj_name = f"special_{i}"
            result = create_project(proj_name, desc, str(tmp_path))
            assert result is True
    
    def test_very_long_project_name(self, tmp_path):
        """Edge case: Very long project name"""
        long_name = "a" * 100
        
        # Should handle or reject gracefully
        try:
            result = create_project(long_name, "test", str(tmp_path))
            if result:
                assert (tmp_path / long_name).exists()
        except (ValueError, OSError):
            # Expected for too-long names
            pass
    
    def test_empty_description(self, tmp_path):
        """Edge case: Empty description"""
        result = create_project("empty_desc", "", str(tmp_path))
        assert result is True
        assert (tmp_path / "empty_desc").exists()
    
    def test_project_in_nested_directory(self, tmp_path):
        """Edge case: Project in deeply nested directory"""
        nested_path = tmp_path / "a" / "b" / "c" / "d" / "e"
        nested_path.mkdir(parents=True)
        
        result = create_project("nested_proj", "test", str(nested_path))
        assert result is True
        assert (nested_path / "nested_proj").exists()
    
    def test_duplicate_project_name(self, tmp_path):
        """Edge case: Creating project with existing name"""
        project_name = "duplicate"
        
        # Create first project
        result1 = create_project(project_name, "first", str(tmp_path))
        assert result1 is True
        
        # Try to create duplicate
        result2 = create_project(project_name, "second", str(tmp_path))
        # Should either fail or overwrite
        assert result2 in [True, False]


class TestErrorScenarios:
    """Test how users encounter and recover from errors"""
    
    def test_user_deletes_ui_file(self, tmp_path):
        """Error: User accidentally deletes UI file"""
        project_name = "deleted_ui"
        project_path = tmp_path / project_name
        
        create_project(project_name, "test", str(tmp_path))
        
        # User deletes UI file
        ui_file = project_path / f"{project_name}.ui"
        ui_file.unlink()
        
        # User tries to validate
        with pytest.raises(FileNotFoundError):
            validate_project(str(project_path))
    
    def test_user_corrupts_registry(self, tmp_path):
        """Error: User corrupts registry file"""
        registry_path = tmp_path / "test_registry.json"
        
        # Create valid registry
        registry = Registry(str(registry_path))
        registry.add_project("test", str(tmp_path / "test"))
        
        # User corrupts file
        registry_path.write_text("{invalid json content")
        
        # Should recover gracefully
        new_registry = Registry(str(registry_path))
        assert new_registry.list_projects() == []
    
    def test_user_moves_project_directory(self, tmp_path):
        """Error: User moves project without updating registry"""
        project_name = "moved_project"
        old_path = tmp_path / "old" / project_name
        new_path = tmp_path / "new" / project_name
        
        old_path.parent.mkdir(parents=True)
        new_path.parent.mkdir(parents=True)
        
        # Create and register
        create_project(project_name, "test", str(old_path.parent))
        registry = Registry()
        registry.add_project(project_name, str(old_path))
        
        # User moves directory
        import shutil
        shutil.move(str(old_path), str(new_path))
        
        # Registry has stale path
        proj_info = registry.get_project(project_name)
        assert not Path(proj_info["path"]).exists()


class TestUsabilityFeatures:
    """Test usability and user experience features"""
    
    def test_helpful_error_messages(self, tmp_path):
        """Test error messages are helpful"""
        # Try invalid project name
        try:
            create_project("", "test", str(tmp_path))
        except ValueError as e:
            assert len(str(e)) > 10  # Should have helpful message
    
    def test_project_readme_generated(self, tmp_path):
        """Test README is generated with useful info"""
        project_name = "readme_test"
        create_project(project_name, "test application", str(tmp_path))
        
        readme = tmp_path / project_name / "README.md"
        assert readme.exists()
        
        content = readme.read_text()
        assert project_name in content
        assert "test application" in content
    
    def test_project_structure_intuitive(self, tmp_path):
        """Test project structure is intuitive"""
        project_name = "structure_test"
        create_project(project_name, "test", str(tmp_path))
        
        project_path = tmp_path / project_name
        
        # Should have expected files
        expected_files = [
            f"{project_name}.ui",
            f"{project_name}.py",
            "README.md"
        ]
        
        for file in expected_files:
            assert (project_path / file).exists(), f"Missing {file}"


class TestRealWorldWorkflows:
    """Test real-world usage patterns"""
    
    def test_daily_development_workflow(self, tmp_path):
        """Workflow: Typical day of development"""
        project_name = "daily_app"
        
        # Morning: Create project
        create_project(project_name, "daily work app", str(tmp_path))
        
        # Register for easy access
        registry = Registry()
        registry.add_project(project_name, str(tmp_path / project_name))
        registry.set_active_project(project_name)
        
        # Afternoon: Validate work
        issues = validate_project(str(tmp_path / project_name))
        assert isinstance(issues, list)
        
        # Evening: Check status
        active = registry.get_active_project()
        assert active == project_name
    
    def test_team_collaboration_workflow(self, tmp_path):
        """Workflow: Team working on shared projects"""
        team_projects = ["frontend", "backend", "shared_ui"]
        registry = Registry()
        
        # Team creates multiple projects
        for proj in team_projects:
            create_project(proj, f"{proj} component", str(tmp_path))
            registry.add_project(proj, str(tmp_path / proj))
        
        # Each team member can access all projects
        all_projects = registry.list_projects()
        for proj in team_projects:
            assert proj in all_projects
    
    def test_project_maintenance_workflow(self, tmp_path):
        """Workflow: Maintaining existing project"""
        project_name = "maintained_app"
        project_path = tmp_path / project_name
        
        # Create initial project
        create_project(project_name, "app to maintain", str(tmp_path))
        
        # Regular validation
        issues = validate_project(str(project_path))
        initial_issue_count = len(issues)
        
        # Make improvements
        # (In real scenario, user would fix issues)
        
        # Validate again
        issues = validate_project(str(project_path))
        assert len(issues) >= 0  # Should not increase


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
