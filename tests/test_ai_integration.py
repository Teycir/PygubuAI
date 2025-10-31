"""Tests for AI integration features"""
import pytest
from pathlib import Path

@pytest.mark.unit
def test_ai_context_generation(temp_ai_project, monkeypatch):
    """Test AI context generation"""
    from pygubuai.ai_context import generate_context
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_ai_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    context = generate_context(temp_ai_project['name'])
    
    assert 'project' in context
    assert context['project'] == temp_ai_project['name']
    assert 'widgets' in context
    assert 'callbacks' in context
    assert 'metrics' in context

@pytest.mark.unit
def test_ai_analyzer(temp_ai_project, monkeypatch):
    """Test project analysis"""
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_ai_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    analysis = analyze_project(temp_ai_project['name'])
    
    assert 'project' in analysis
    assert 'complexity' in analysis
    assert 'widget_count' in analysis
    assert 'suggestions' in analysis
    assert isinstance(analysis['complexity'], float)

@pytest.mark.unit
def test_ai_refactor_suggestions(temp_ai_project, monkeypatch):
    """Test refactoring suggestions"""
    from pygubuai.ai_refactor import analyze_refactoring_opportunities
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_ai_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    suggestions = analyze_refactoring_opportunities(temp_ai_project['name'])
    
    assert isinstance(suggestions, list)
    for sug in suggestions:
        assert hasattr(sug, 'id')
        assert hasattr(sug, 'category')
        assert hasattr(sug, 'title')
        assert hasattr(sug, 'impact')

@pytest.mark.unit
def test_ai_query_widgets(temp_ai_project, monkeypatch):
    """Test natural language query for widgets"""
    from pygubuai.ai_query import query_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_ai_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    result = query_project(temp_ai_project['name'], "How many widgets?")
    
    assert "widget" in result.lower()
    assert isinstance(result, str)

@pytest.mark.unit
def test_ai_query_callbacks(temp_ai_project, monkeypatch):
    """Test natural language query for callbacks"""
    from pygubuai.ai_query import query_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_ai_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    result = query_project(temp_ai_project['name'], "What callbacks?")
    
    assert isinstance(result, str)

@pytest.mark.unit
def test_ai_query_complexity(temp_ai_project, monkeypatch):
    """Test natural language query for complexity"""
    from pygubuai.ai_query import query_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_ai_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    result = query_project(temp_ai_project['name'], "Show complexity")
    
    assert "complexity" in result.lower()

@pytest.mark.unit
def test_ai_analyzer_complex_ui(temp_complex_project, monkeypatch):
    """Test analysis with realistic complex UI"""
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_complex_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    analysis = analyze_project(temp_complex_project['name'])
    
    assert analysis['widget_count'] >= 8
    assert 'ttk.Treeview' in analysis['widget_types']
    assert 'ttk.Notebook' in analysis['widget_types']
    assert analysis['complexity'] > 3.0
    assert len(analysis['suggestions']) >= 0

@pytest.mark.unit
def test_ai_query_specific_widgets(temp_complex_project, monkeypatch):
    """Test queries for specific widget types"""
    from pygubuai.ai_query import query_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_complex_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    result = query_project(temp_complex_project['name'], "How many buttons?")
    assert "button" in result.lower()
    assert "2" in result or "two" in result.lower()
    
    result = query_project(temp_complex_project['name'], "What widget types?")
    assert "Treeview" in result or "treeview" in result.lower()

@pytest.mark.unit
def test_ai_context_with_metadata(temp_complex_project, monkeypatch):
    """Test context generation includes all metadata"""
    from pygubuai.ai_context import generate_context
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_complex_project['registry']) or setattr(self, '_cache', None) or setattr(self, '_cache_time', None) or setattr(self, '_cache_ttl', 5.0))
    
    context = generate_context(temp_complex_project['name'])
    
    assert context['metrics']['widget_count'] >= 8
    assert context['metrics']['callback_count'] >= 3
    assert len(context['widgets']) >= 8
    assert any(w['class'] == 'ttk.Treeview' for w in context['widgets'])

@pytest.fixture
def temp_ai_project(tmp_path):
    """Create temporary test project with UI"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "test_registry.json"
    
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
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}

@pytest.fixture
def temp_complex_project(tmp_path):
    """Create realistic complex project with multiple widget types"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "test_registry_complex.json"
    
    project_name = "test_complex"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Complex App</property>
    <object class="ttk.Notebook" id="notebook">
      <object class="ttk.Frame" id="tab_data">
        <object class="ttk.Treeview" id="tree_items">
          <property name="columns">name value status</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_tree">
          <property name="command">tree_items.yview</property>
        </object>
      </object>
      <object class="ttk.Frame" id="tab_form">
        <object class="ttk.Label" id="lbl_name">
          <property name="text">Name:</property>
        </object>
        <object class="ttk.Entry" id="entry_name"/>
        <object class="ttk.Combobox" id="combo_category">
          <property name="values">A B C</property>
        </object>
        <object class="ttk.Scale" id="scale_priority">
          <property name="from_">0</property>
          <property name="to">100</property>
        </object>
        <object class="ttk.Button" id="btn_save">
          <property name="text">Save</property>
          <property name="command">on_save</property>
        </object>
        <object class="ttk.Button" id="btn_cancel">
          <property name="text">Cancel</property>
          <property name="command">on_cancel</property>
        </object>
      </object>
    </object>
    <object class="ttk.Progressbar" id="progress">
      <property name="mode">indeterminate</property>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""Complex test application"""

def on_save():
    """Save data"""
    pass

def on_cancel():
    """Cancel operation"""
    pass

def on_tree_select(event):
    """Handle tree selection"""
    pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}
