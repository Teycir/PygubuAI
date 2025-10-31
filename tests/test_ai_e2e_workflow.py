"""End-to-end AI workflow tests"""
import pytest
from pathlib import Path
import json


@pytest.mark.integration
def test_complete_ai_workflow_crm(crm_workflow_fixture, monkeypatch):
    """
    Complete AI workflow: Create -> Analyze -> Query -> Refactor -> Context
    
    Simulates full Amazon Q integration workflow:
    1. Project exists in registry
    2. AI analyzes project structure
    3. User queries via natural language
    4. AI suggests refactorings
    5. Context generated for chat
    """
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.ai_query import query_project
    from pygubuai.ai_refactor import analyze_refactoring_opportunities
    from pygubuai.ai_context import generate_context, format_for_ai
    from pygubuai.registry import Registry
    
    project_name = crm_workflow_fixture['name']
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', crm_workflow_fixture['registry']) or setattr(self, '_cache', None))
    
    # Step 1: Analyze project
    analysis = analyze_project(project_name)
    assert 'error' not in analysis
    assert analysis['widget_count'] >= 25
    assert analysis['complexity'] > 8.0
    
    # Step 2: Natural language queries
    widget_query = query_project(project_name, "How many widgets?")
    assert str(analysis['widget_count']) in widget_query or "widget" in widget_query.lower()
    
    callback_query = query_project(project_name, "What callbacks?")
    assert "callback" in callback_query.lower() or "on_" in callback_query
    
    complexity_query = query_project(project_name, "Show complexity")
    assert "complexity" in complexity_query.lower()
    
    # Step 3: Get refactoring suggestions
    suggestions = analyze_refactoring_opportunities(project_name)
    assert len(suggestions) > 0
    assert any(s.category == 'layout' for s in suggestions)
    assert any(s.category == 'accessibility' for s in suggestions)
    
    # Step 4: Generate AI context
    context = generate_context(project_name)
    assert context['project'] == project_name
    assert context['metrics']['widget_count'] >= 25
    assert len(context['widgets']) >= 25
    assert len(context['callbacks']) >= 5
    
    # Step 5: Format for AI consumption
    formatted = format_for_ai(context)
    assert project_name in formatted
    assert "Widgets" in formatted
    assert "Callbacks" in formatted


@pytest.mark.integration
def test_workflow_with_modifications(modifiable_project_fixture, monkeypatch):
    """
    Test workflow with project modifications:
    1. Initial analysis
    2. Modify UI (add widgets)
    3. Re-analyze and detect changes
    4. Update suggestions
    """
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.ai_refactor import analyze_refactoring_opportunities
    from pygubuai.registry import Registry
    
    project_name = modifiable_project_fixture['name']
    project_dir = Path(modifiable_project_fixture['path'])
    ui_file = project_dir / f"{project_name}.ui"
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', modifiable_project_fixture['registry']) or setattr(self, '_cache', None))
    
    # Initial analysis
    analysis1 = analyze_project(project_name)
    initial_count = analysis1['widget_count']
    initial_complexity = analysis1['complexity']
    
    # Modify UI - add more widgets
    ui_content = ui_file.read_text()
    new_widgets = '''
      <object class="ttk.Button" id="btn_new1">
        <property name="text">New Button 1</property>
        <property name="command">on_new1</property>
      </object>
      <object class="ttk.Button" id="btn_new2">
        <property name="text">New Button 2</property>
        <property name="command">on_new2</property>
      </object>
      <object class="ttk.Entry" id="entry_new"/>
'''
    ui_content = ui_content.replace('</object>\n</interface>', new_widgets + '  </object>\n</interface>')
    ui_file.write_text(ui_content)
    
    # Re-analyze
    analysis2 = analyze_project(project_name)
    assert analysis2['widget_count'] > initial_count
    assert analysis2['complexity'] >= initial_complexity
    
    # Verify suggestions updated
    suggestions = analyze_refactoring_opportunities(project_name)
    assert len(suggestions) > 0


@pytest.mark.integration
def test_multi_project_workflow(multi_project_fixture, monkeypatch):
    """
    Test workflow across multiple projects:
    1. Analyze all projects
    2. Compare complexity
    3. Generate contexts for each
    """
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.ai_context import generate_context
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', multi_project_fixture['registry']) or setattr(self, '_cache', None))
    
    analyses = {}
    contexts = {}
    
    for project_name in multi_project_fixture['projects']:
        analyses[project_name] = analyze_project(project_name)
        contexts[project_name] = generate_context(project_name)
    
    # Verify all analyzed
    assert len(analyses) == 3
    assert all('error' not in a for a in analyses.values())
    
    # Compare complexity
    complexities = {name: a['complexity'] for name, a in analyses.items()}
    assert max(complexities.values()) > min(complexities.values())
    
    # Verify contexts
    assert all(c['project'] in multi_project_fixture['projects'] for c in contexts.values())


@pytest.mark.integration
def test_error_handling_workflow(tmp_path, monkeypatch):
    """Test workflow with error conditions"""
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.ai_query import query_project
    from pygubuai.ai_context import generate_context
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "error_registry.json"
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', temp_registry) or setattr(self, '_cache', None))
    
    # Non-existent project
    analysis = analyze_project("nonexistent")
    assert 'error' in analysis
    
    query_result = query_project("nonexistent", "How many widgets?")
    assert "error" in query_result.lower() or "not found" in query_result.lower()
    
    context = generate_context("nonexistent")
    assert 'error' in context


@pytest.mark.integration
def test_performance_large_project(large_project_fixture, monkeypatch):
    """Test workflow performance with large project"""
    import time
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.ai_context import generate_context
    from pygubuai.registry import Registry
    
    project_name = large_project_fixture['name']
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', large_project_fixture['registry']) or setattr(self, '_cache', None))
    
    # Analysis should complete in reasonable time
    start = time.time()
    analysis = analyze_project(project_name)
    analysis_time = time.time() - start
    
    assert analysis_time < 2.0  # Should be fast
    assert analysis['widget_count'] >= 50
    
    # Context generation
    start = time.time()
    context = generate_context(project_name)
    context_time = time.time() - start
    
    assert context_time < 2.0
    assert len(context['widgets']) >= 50


@pytest.fixture
def crm_workflow_fixture(tmp_path):
    """CRM app for complete workflow testing"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "workflow_registry.json"
    project_name = "crm_workflow"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">CRM System</property>
    <object class="ttk.Frame" id="toolbar">
      <object class="ttk.Button" id="btn_new"><property name="text">New</property><property name="command">on_new</property></object>
      <object class="ttk.Button" id="btn_edit"><property name="text">Edit</property><property name="command">on_edit</property></object>
      <object class="ttk.Button" id="btn_delete"><property name="text">Delete</property><property name="command">on_delete</property></object>
      <object class="ttk.Button" id="btn_refresh"><property name="text">Refresh</property><property name="command">on_refresh</property></object>
      <object class="ttk.Entry" id="entry_search"><property name="width">30</property></object>
      <object class="ttk.Button" id="btn_search"><property name="text">Search</property><property name="command">on_search</property></object>
    </object>
    <object class="ttk.Notebook" id="notebook">
      <object class="ttk.Frame" id="tab_contacts">
        <object class="ttk.Treeview" id="tree_contacts"><property name="columns">name email phone company</property></object>
        <object class="ttk.Scrollbar" id="scroll_contacts"><property name="command">tree_contacts.yview</property></object>
      </object>
      <object class="ttk.Frame" id="tab_deals">
        <object class="ttk.Treeview" id="tree_deals"><property name="columns">title value stage</property></object>
        <object class="ttk.Scrollbar" id="scroll_deals"><property name="command">tree_deals.yview</property></object>
      </object>
      <object class="ttk.Frame" id="tab_tasks">
        <object class="ttk.Label" id="lbl_filter"><property name="text">Filter:</property></object>
        <object class="ttk.Combobox" id="combo_status"><property name="values">All Open Closed</property></object>
        <object class="ttk.Combobox" id="combo_priority"><property name="values">All High Low</property></object>
        <object class="ttk.Treeview" id="tree_tasks"><property name="columns">task due priority</property></object>
        <object class="ttk.Scrollbar" id="scroll_tasks"><property name="command">tree_tasks.yview</property></object>
      </object>
      <object class="ttk.Frame" id="tab_reports">
        <object class="ttk.Label" id="lbl_period"><property name="text">Period:</property></object>
        <object class="ttk.Entry" id="entry_start"/><object class="ttk.Entry" id="entry_end"/>
        <object class="ttk.Button" id="btn_generate"><property name="text">Generate</property><property name="command">on_generate</property></object>
        <object class="tk.Canvas" id="canvas_chart"><property name="width">600</property><property name="height">400</property></object>
      </object>
    </object>
    <object class="ttk.Frame" id="statusbar">
      <object class="ttk.Label" id="lbl_status"><property name="text">Ready</property></object>
      <object class="ttk.Progressbar" id="progress"><property name="mode">indeterminate</property></object>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""CRM Workflow App"""
def on_new(): pass
def on_edit(): pass
def on_delete(): pass
def on_refresh(): pass
def on_search(): pass
def on_generate(): pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}


@pytest.fixture
def modifiable_project_fixture(tmp_path):
    """Simple project for modification testing"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "mod_registry.json"
    project_name = "modifiable"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Modifiable</property>
    <object class="ttk.Button" id="btn_test"><property name="text">Test</property></object>
    <object class="ttk.Entry" id="entry_test"/>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('"""Modifiable App"""\n')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}


@pytest.fixture
def multi_project_fixture(tmp_path):
    """Multiple projects for comparison"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "multi_registry.json"
    registry = Registry(registry_path=temp_registry)
    projects = []
    
    for i, (name, widget_count) in enumerate([('simple', 3), ('medium', 10), ('complex', 20)]):
        project_dir = tmp_path / name
        project_dir.mkdir()
        
        widgets = ''.join([f'<object class="ttk.Button" id="btn_{j}"><property name="text">Btn{j}</property></object>' 
                          for j in range(widget_count)])
        
        ui_file = project_dir / f"{name}.ui"
        ui_file.write_text(f'''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">{name.title()}</property>
    {widgets}
  </object>
</interface>''')
        
        py_file = project_dir / f"{name}.py"
        py_file.write_text(f'"""{name.title()} App"""\n')
        
        registry.add_project(name, str(project_dir))
        projects.append(name)
    
    return {'projects': projects, 'registry': temp_registry}


@pytest.fixture
def large_project_fixture(tmp_path):
    """Large project for performance testing"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "large_registry.json"
    project_name = "large_app"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    # Generate 50+ widgets
    widgets = []
    for i in range(50):
        widget_type = ['ttk.Button', 'ttk.Entry', 'ttk.Label', 'ttk.Combobox'][i % 4]
        widgets.append(f'<object class="{widget_type}" id="widget_{i}"><property name="text">Widget{i}</property></object>')
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text(f'''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">Large App</property>
    {''.join(widgets)}
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('"""Large App"""\n')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}
