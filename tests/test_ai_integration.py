"""Tests for AI integration features"""
import pytest
from pathlib import Path

@pytest.mark.unit
def test_ai_context_generation(temp_project):
    """Test AI context generation"""
    from pygubuai.ai_context import generate_context
    
    context = generate_context(temp_project['name'])
    
    assert 'project' in context
    assert context['project'] == temp_project['name']
    assert 'widgets' in context
    assert 'callbacks' in context
    assert 'metrics' in context

@pytest.mark.unit
def test_ai_analyzer(temp_project):
    """Test project analysis"""
    from pygubuai.ai_analyzer import analyze_project
    
    analysis = analyze_project(temp_project['name'])
    
    assert 'project' in analysis
    assert 'complexity' in analysis
    assert 'widget_count' in analysis
    assert 'suggestions' in analysis
    assert isinstance(analysis['complexity'], float)

@pytest.mark.unit
def test_ai_refactor_suggestions(temp_project):
    """Test refactoring suggestions"""
    from pygubuai.ai_refactor import analyze_refactoring_opportunities
    
    suggestions = analyze_refactoring_opportunities(temp_project['name'])
    
    assert isinstance(suggestions, list)
    for sug in suggestions:
        assert hasattr(sug, 'id')
        assert hasattr(sug, 'category')
        assert hasattr(sug, 'title')
        assert hasattr(sug, 'impact')

@pytest.mark.unit
def test_ai_query_widgets(temp_project):
    """Test natural language query for widgets"""
    from pygubuai.ai_query import query_project
    
    result = query_project(temp_project['name'], "How many widgets?")
    
    assert "widget" in result.lower()
    assert isinstance(result, str)

@pytest.mark.unit
def test_ai_query_callbacks(temp_project):
    """Test natural language query for callbacks"""
    from pygubuai.ai_query import query_project
    
    result = query_project(temp_project['name'], "What callbacks?")
    
    assert isinstance(result, str)

@pytest.mark.unit
def test_ai_query_complexity(temp_project):
    """Test natural language query for complexity"""
    from pygubuai.ai_query import query_project
    
    result = query_project(temp_project['name'], "Show complexity")
    
    assert "complexity" in result.lower()

@pytest.fixture
def temp_project(tmp_path, mock_registry):
    """Create temporary test project with UI"""
    project_name = "test_ai"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Test</property>
    <object class="ttk.Button" id="btn_submit">
      <property name="text">Submit</property>
      <property name="command">on_submit</property>
    </object>
    <object class="ttk.Entry" id="entry_name">
      <property name="text">Name</property>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""Test application"""

def on_submit():
    """Handle submit"""
    pass
''')
    
    mock_registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir)}
