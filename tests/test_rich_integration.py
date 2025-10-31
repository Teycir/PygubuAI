"""Tests for Rich terminal UI integration"""
import pytest
import sys
from io import StringIO

# Test with Rich available
try:
    import rich
    RICH_INSTALLED = True
except ImportError:
    RICH_INSTALLED = False

class TestRichIntegration:
    """Test Rich integration with graceful fallback"""
    
    def test_status_with_rich(self, temp_project):
        """Test status command with Rich"""
        if not RICH_INSTALLED:
            pytest.skip("Rich not installed")
        
        from pygubuai.status import main
        sys.argv = ['pygubu-status', temp_project['name']]
        
        # Should not raise
        try:
            main()
        except SystemExit:
            pass
    
    def test_status_without_rich(self, temp_project, monkeypatch):
        """Test status command fallback without Rich"""
        # Mock Rich as unavailable
        monkeypatch.setattr('pygubuai.status.RICH_AVAILABLE', False)
        
        from pygubuai.status import main
        sys.argv = ['pygubu-status', temp_project['name']]
        
        # Should not raise
        try:
            main()
        except SystemExit:
            pass
    
    def test_widgets_with_rich(self):
        """Test widgets command with Rich"""
        if not RICH_INSTALLED:
            pytest.skip("Rich not installed")
        
        from pygubuai.widgets import main
        sys.argv = ['pygubu-widgets', 'list']
        
        try:
            main()
        except SystemExit:
            pass
    
    def test_widgets_without_rich(self, monkeypatch):
        """Test widgets command fallback"""
        monkeypatch.setattr('pygubuai.widgets.RICH_AVAILABLE', False)
        
        from pygubuai.widgets import main
        sys.argv = ['pygubu-widgets', 'list']
        
        try:
            main()
        except SystemExit:
            pass
    
    def test_inspect_with_rich(self, temp_project):
        """Test inspect command with Rich"""
        if not RICH_INSTALLED:
            pytest.skip("Rich not installed")
        
        from pygubuai.inspect import main
        sys.argv = ['pygubu-inspect', temp_project['name'], '--tree']
        
        try:
            main()
        except SystemExit:
            pass
    
    def test_validate_with_rich(self, temp_project):
        """Test validate command with Rich"""
        if not RICH_INSTALLED:
            pytest.skip("Rich not installed")
        
        from pygubuai.validate_project import main
        sys.argv = ['pygubu-validate', temp_project['name']]
        
        try:
            main()
        except SystemExit:
            pass
    
    def test_batch_with_rich(self, temp_project):
        """Test batch command with Rich"""
        if not RICH_INSTALLED:
            pytest.skip("Rich not installed")
        
        from pygubuai.batch import main
        sys.argv = ['pygubu-batch', 'validate', temp_project['name']]
        
        try:
            main()
        except SystemExit:
            pass
    
    def test_register_list_with_rich(self, temp_project):
        """Test register list with Rich"""
        if not RICH_INSTALLED:
            pytest.skip("Rich not installed")
        
        from pygubuai.register import main
        sys.argv = ['pygubu-register', 'list']
        
        try:
            main()
        except SystemExit:
            pass

@pytest.fixture
def temp_project(tmp_path, registry):
    """Create temporary test project"""
    project_name = "test_rich"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    # Create UI file
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Test</property>
  </object>
</interface>''')
    
    # Create Python file
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('# Test file')
    
    # Register
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir)}
