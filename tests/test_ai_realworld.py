"""Real-world AI integration tests with production-quality fixtures"""
import pytest
from pathlib import Path


@pytest.mark.integration
def test_crm_application_analysis(crm_app_fixture, monkeypatch):
    """Test AI analysis of realistic CRM application"""
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', crm_app_fixture['registry']) or setattr(self, '_cache', None))
    
    analysis = analyze_project(crm_app_fixture['name'])
    
    assert analysis['widget_count'] >= 25
    assert analysis['complexity'] > 8.0
    assert 'ttk.Treeview' in analysis['widget_types']
    assert 'ttk.Notebook' in analysis['widget_types']
    assert analysis['callback_count'] >= 5
    assert len(analysis['suggestions']) >= 0


@pytest.mark.integration
def test_settings_dialog_refactoring(settings_dialog_fixture, monkeypatch):
    """Test refactoring suggestions for settings dialog"""
    from pygubuai.ai_refactor import analyze_refactoring_opportunities
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', settings_dialog_fixture['registry']) or setattr(self, '_cache', None))
    
    suggestions = analyze_refactoring_opportunities(settings_dialog_fixture['name'])
    
    assert len(suggestions) >= 2
    categories = {s.category for s in suggestions}
    assert 'accessibility' in categories or 'quality' in categories
    assert any(s.auto_fixable for s in suggestions)


@pytest.mark.integration
def test_dashboard_context_generation(dashboard_fixture, monkeypatch):
    """Test context generation for dashboard with charts"""
    from pygubuai.ai_context import generate_context
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', dashboard_fixture['registry']) or setattr(self, '_cache', None))
    
    context = generate_context(dashboard_fixture['name'])
    
    assert context['metrics']['widget_count'] >= 20
    assert len(context['widgets']) >= 20
    assert any(w['class'] == 'ttk.Progressbar' for w in context['widgets'])
    assert any(w['class'] == 'tk.Canvas' for w in context['widgets'])


@pytest.mark.integration
def test_data_entry_form_queries(data_entry_fixture, monkeypatch):
    """Test natural language queries on data entry form"""
    from pygubuai.ai_query import query_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', data_entry_fixture['registry']) or setattr(self, '_cache', None))
    
    result = query_project(data_entry_fixture['name'], "How many widgets?")
    assert "widget" in result.lower() or str(15) in result or str(16) in result
    
    result = query_project(data_entry_fixture['name'], "What callbacks?")
    assert "callback" in result.lower() or "no callback" in result.lower()


@pytest.mark.integration
def test_file_browser_complexity(file_browser_fixture, monkeypatch):
    """Test complexity analysis of file browser"""
    from pygubuai.ai_analyzer import analyze_project
    from pygubuai.registry import Registry
    
    monkeypatch.setattr(Registry, '__init__', lambda self: setattr(self, 'registry_path', file_browser_fixture['registry']) or setattr(self, '_cache', None))
    
    analysis = analyze_project(file_browser_fixture['name'])
    
    assert analysis['complexity'] >= 7.0
    assert 'ttk.Treeview' in analysis['widget_types']
    assert analysis['widget_types']['ttk.Treeview'] >= 1
    assert len(analysis['layout_patterns']) >= 0


@pytest.fixture
def crm_app_fixture(tmp_path):
    """Realistic CRM application with contacts, deals, tasks"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "crm_registry.json"
    project_name = "crm_app"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">CRM System</property>
    <property name="width">1200</property>
    <property name="height">800</property>
    <object class="ttk.Frame" id="toolbar">
      <object class="ttk.Button" id="btn_new_contact">
        <property name="text">New Contact</property>
        <property name="command">on_new_contact</property>
      </object>
      <object class="ttk.Button" id="btn_new_deal">
        <property name="text">New Deal</property>
        <property name="command">on_new_deal</property>
      </object>
      <object class="ttk.Button" id="btn_refresh">
        <property name="text">Refresh</property>
        <property name="command">on_refresh</property>
      </object>
      <object class="ttk.Separator" id="sep1"/>
      <object class="ttk.Entry" id="entry_search">
        <property name="width">30</property>
      </object>
      <object class="ttk.Button" id="btn_search">
        <property name="text">Search</property>
        <property name="command">on_search</property>
      </object>
    </object>
    <object class="ttk.Notebook" id="notebook_main">
      <object class="ttk.Frame" id="tab_contacts">
        <object class="ttk.Treeview" id="tree_contacts">
          <property name="columns">name email phone company status</property>
          <property name="selectmode">browse</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_contacts_v">
          <property name="command">tree_contacts.yview</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_contacts_h">
          <property name="orient">horizontal</property>
          <property name="command">tree_contacts.xview</property>
        </object>
      </object>
      <object class="ttk.Frame" id="tab_deals">
        <object class="ttk.Treeview" id="tree_deals">
          <property name="columns">title value stage probability close_date</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_deals">
          <property name="command">tree_deals.yview</property>
        </object>
      </object>
      <object class="ttk.Frame" id="tab_tasks">
        <object class="ttk.Frame" id="frame_task_filters">
          <object class="ttk.Label" id="lbl_filter">
            <property name="text">Filter:</property>
          </object>
          <object class="ttk.Combobox" id="combo_task_status">
            <property name="values">All Open Completed Overdue</property>
          </object>
          <object class="ttk.Combobox" id="combo_task_priority">
            <property name="values">All High Medium Low</property>
          </object>
        </object>
        <object class="ttk.Treeview" id="tree_tasks">
          <property name="columns">task assignee due_date priority status</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_tasks">
          <property name="command">tree_tasks.yview</property>
        </object>
      </object>
      <object class="ttk.Frame" id="tab_reports">
        <object class="ttk.Frame" id="frame_report_controls">
          <object class="ttk.Label" id="lbl_date_range">
            <property name="text">Date Range:</property>
          </object>
          <object class="ttk.Entry" id="entry_start_date"/>
          <object class="ttk.Entry" id="entry_end_date"/>
          <object class="ttk.Button" id="btn_generate_report">
            <property name="text">Generate</property>
            <property name="command">on_generate_report</property>
          </object>
        </object>
        <object class="tk.Canvas" id="canvas_chart">
          <property name="width">800</property>
          <property name="height">400</property>
        </object>
      </object>
    </object>
    <object class="ttk.Frame" id="statusbar">
      <object class="ttk.Label" id="lbl_status">
        <property name="text">Ready</property>
      </object>
      <object class="ttk.Progressbar" id="progress_status">
        <property name="mode">indeterminate</property>
      </object>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""CRM Application"""

def on_new_contact():
    pass

def on_new_deal():
    pass

def on_refresh():
    pass

def on_search():
    pass

def on_generate_report():
    pass

def on_contact_select(event):
    pass

def on_deal_select(event):
    pass

def on_task_select(event):
    pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}


@pytest.fixture
def settings_dialog_fixture(tmp_path):
    """Settings dialog with multiple categories"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "settings_registry.json"
    project_name = "settings_dialog"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="settings_window">
    <property name="title">Settings</property>
    <object class="ttk.Notebook" id="notebook_settings">
      <object class="ttk.Frame" id="tab_general">
        <object class="ttk.Checkbutton" id="chk_auto_save">
          <property name="text">Auto-save</property>
        </object>
        <object class="ttk.Checkbutton" id="chk_notifications">
          <property name="text">Enable notifications</property>
        </object>
        <object class="ttk.Label" id="lbl_language">
          <property name="text">Language:</property>
        </object>
        <object class="ttk.Combobox" id="combo_language">
          <property name="values">English Spanish French German</property>
        </object>
        <object class="ttk.Label" id="lbl_theme">
          <property name="text">Theme:</property>
        </object>
        <object class="ttk.Combobox" id="combo_theme">
          <property name="values">Light Dark Auto</property>
        </object>
      </object>
      <object class="ttk.Frame" id="tab_network">
        <object class="ttk.Label" id="lbl_proxy">
          <property name="text">Proxy Server:</property>
        </object>
        <object class="ttk.Entry" id="entry_proxy"/>
        <object class="ttk.Label" id="lbl_port">
          <property name="text">Port:</property>
        </object>
        <object class="ttk.Spinbox" id="spin_port">
          <property name="from_">1</property>
          <property name="to">65535</property>
        </object>
        <object class="ttk.Checkbutton" id="chk_use_proxy">
          <property name="text">Use proxy</property>
        </object>
      </object>
      <object class="ttk.Frame" id="tab_advanced">
        <object class="ttk.Label" id="lbl_cache_size">
          <property name="text">Cache Size (MB):</property>
        </object>
        <object class="ttk.Scale" id="scale_cache">
          <property name="from_">100</property>
          <property name="to">5000</property>
        </object>
        <object class="ttk.Label" id="lbl_cache_value">
          <property name="text">1000</property>
        </object>
        <object class="ttk.Button" id="btn_clear_cache">
          <property name="text">Clear Cache</property>
          <property name="command">on_clear_cache</property>
        </object>
      </object>
    </object>
    <object class="ttk.Frame" id="frame_buttons">
      <object class="ttk.Button" id="btn_ok">
        <property name="text">OK</property>
        <property name="command">on_ok</property>
      </object>
      <object class="ttk.Button" id="btn_cancel">
        <property name="text">Cancel</property>
        <property name="command">on_cancel</property>
      </object>
      <object class="ttk.Button" id="btn_apply">
        <property name="text">Apply</property>
        <property name="command">on_apply</property>
      </object>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""Settings Dialog"""

def on_clear_cache():
    pass

def on_ok():
    pass

def on_cancel():
    pass

def on_apply():
    pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}


@pytest.fixture
def dashboard_fixture(tmp_path):
    """Dashboard with metrics and charts"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "dashboard_registry.json"
    project_name = "dashboard"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="dashboard">
    <property name="title">Analytics Dashboard</property>
    <object class="ttk.Frame" id="frame_metrics">
      <object class="ttk.Labelframe" id="lf_sales">
        <property name="text">Sales</property>
        <object class="ttk.Label" id="lbl_sales_value">
          <property name="text">$0</property>
        </object>
        <object class="ttk.Progressbar" id="progress_sales">
          <property name="value">75</property>
        </object>
      </object>
      <object class="ttk.Labelframe" id="lf_customers">
        <property name="text">Customers</property>
        <object class="ttk.Label" id="lbl_customers_value">
          <property name="text">0</property>
        </object>
        <object class="ttk.Progressbar" id="progress_customers">
          <property name="value">60</property>
        </object>
      </object>
      <object class="ttk.Labelframe" id="lf_revenue">
        <property name="text">Revenue</property>
        <object class="ttk.Label" id="lbl_revenue_value">
          <property name="text">$0</property>
        </object>
        <object class="ttk.Progressbar" id="progress_revenue">
          <property name="value">85</property>
        </object>
      </object>
    </object>
    <object class="ttk.Frame" id="frame_charts">
      <object class="tk.Canvas" id="canvas_line_chart">
        <property name="width">600</property>
        <property name="height">300</property>
      </object>
      <object class="tk.Canvas" id="canvas_bar_chart">
        <property name="width">600</property>
        <property name="height">300</property>
      </object>
    </object>
    <object class="ttk.Frame" id="frame_data">
      <object class="ttk.Treeview" id="tree_recent">
        <property name="columns">date type amount status</property>
      </object>
      <object class="ttk.Scrollbar" id="scroll_recent">
        <property name="command">tree_recent.yview</property>
      </object>
    </object>
    <object class="ttk.Frame" id="frame_controls">
      <object class="ttk.Button" id="btn_refresh">
        <property name="text">Refresh</property>
        <property name="command">on_refresh</property>
      </object>
      <object class="ttk.Button" id="btn_export">
        <property name="text">Export</property>
        <property name="command">on_export</property>
      </object>
      <object class="ttk.Combobox" id="combo_period">
        <property name="values">Today Week Month Year</property>
      </object>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""Dashboard Application"""

def on_refresh():
    pass

def on_export():
    pass

def update_metrics():
    pass

def draw_charts():
    pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}


@pytest.fixture
def data_entry_fixture(tmp_path):
    """Data entry form with validation"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "data_entry_registry.json"
    project_name = "data_entry"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="form">
    <property name="title">Customer Form</property>
    <object class="ttk.Frame" id="frame_form">
      <object class="ttk.Label" id="lbl_first_name">
        <property name="text">First Name:</property>
      </object>
      <object class="ttk.Entry" id="entry_first_name"/>
      <object class="ttk.Label" id="lbl_last_name">
        <property name="text">Last Name:</property>
      </object>
      <object class="ttk.Entry" id="entry_last_name"/>
      <object class="ttk.Label" id="lbl_email">
        <property name="text">Email:</property>
      </object>
      <object class="ttk.Entry" id="entry_email"/>
      <object class="ttk.Label" id="lbl_phone">
        <property name="text">Phone:</property>
      </object>
      <object class="ttk.Entry" id="entry_phone"/>
      <object class="ttk.Label" id="lbl_company">
        <property name="text">Company:</property>
      </object>
      <object class="ttk.Entry" id="entry_company"/>
      <object class="ttk.Label" id="lbl_position">
        <property name="text">Position:</property>
      </object>
      <object class="ttk.Entry" id="entry_position"/>
      <object class="ttk.Label" id="lbl_category">
        <property name="text">Category:</property>
      </object>
      <object class="ttk.Combobox" id="combo_category">
        <property name="values">Lead Prospect Customer Partner</property>
      </object>
      <object class="ttk.Label" id="lbl_notes">
        <property name="text">Notes:</property>
      </object>
      <object class="tk.Text" id="text_notes">
        <property name="width">40</property>
        <property name="height">5</property>
      </object>
    </object>
    <object class="ttk.Frame" id="frame_buttons">
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
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""Data Entry Form"""

def on_save():
    pass

def on_cancel():
    pass

def validate_email(email):
    pass

def validate_phone(phone):
    pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}


@pytest.fixture
def file_browser_fixture(tmp_path):
    """File browser with tree view"""
    from pygubuai.registry import Registry
    
    temp_registry = tmp_path / "file_browser_registry.json"
    project_name = "file_browser"
    project_dir = tmp_path / project_name
    project_dir.mkdir()
    
    ui_file = project_dir / f"{project_name}.ui"
    ui_file.write_text('''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.0">
  <object class="tk.Toplevel" id="browser">
    <property name="title">File Browser</property>
    <object class="ttk.Frame" id="frame_toolbar">
      <object class="ttk.Button" id="btn_back">
        <property name="text">Back</property>
        <property name="command">on_back</property>
      </object>
      <object class="ttk.Button" id="btn_forward">
        <property name="text">Forward</property>
        <property name="command">on_forward</property>
      </object>
      <object class="ttk.Button" id="btn_up">
        <property name="text">Up</property>
        <property name="command">on_up</property>
      </object>
      <object class="ttk.Entry" id="entry_path">
        <property name="width">50</property>
      </object>
      <object class="ttk.Button" id="btn_go">
        <property name="text">Go</property>
        <property name="command">on_go</property>
      </object>
    </object>
    <object class="ttk.Panedwindow" id="paned">
      <object class="ttk.Frame" id="frame_tree">
        <object class="ttk.Treeview" id="tree_folders">
          <property name="selectmode">browse</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_tree">
          <property name="command">tree_folders.yview</property>
        </object>
      </object>
      <object class="ttk.Frame" id="frame_files">
        <object class="ttk.Treeview" id="tree_files">
          <property name="columns">name size modified type</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_files_v">
          <property name="command">tree_files.yview</property>
        </object>
        <object class="ttk.Scrollbar" id="scroll_files_h">
          <property name="orient">horizontal</property>
          <property name="command">tree_files.xview</property>
        </object>
      </object>
    </object>
    <object class="ttk.Frame" id="statusbar">
      <object class="ttk.Label" id="lbl_status">
        <property name="text">Ready</property>
      </object>
      <object class="ttk.Label" id="lbl_item_count">
        <property name="text">0 items</property>
      </object>
    </object>
  </object>
</interface>''')
    
    py_file = project_dir / f"{project_name}.py"
    py_file.write_text('''"""File Browser"""

def on_back():
    pass

def on_forward():
    pass

def on_up():
    pass

def on_go():
    pass

def on_folder_select(event):
    pass

def on_file_select(event):
    pass

def load_directory(path):
    pass
''')
    
    registry = Registry(registry_path=temp_registry)
    registry.add_project(project_name, str(project_dir))
    
    return {'name': project_name, 'path': str(project_dir), 'registry': temp_registry}
