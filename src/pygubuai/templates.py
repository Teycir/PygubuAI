"""Project templates"""

TEMPLATES = {
    "login": {
        "description": "Login form with username, password, and submit button",
        "widgets": [
            ("label", "Username:", "username_label"),
            ("entry", "", "username_entry"),
            ("label", "Password:", "password_label"),
            ("entry", "", "password_entry", {"show": "*"}),
            ("button", "Login", "login_button", {"command": "on_login"}),
        ],
        "callbacks": ["on_login"],
    },
    "crud": {
        "description": "CRUD interface with form and data table",
        "widgets": [
            ("label", "Name:", "name_label"),
            ("entry", "", "name_entry"),
            ("button", "Add", "add_button", {"command": "on_add"}),
            ("button", "Update", "update_button", {"command": "on_update"}),
            ("button", "Delete", "delete_button", {"command": "on_delete"}),
            ("treeview", "", "data_table", {"columns": ["id", "name"]}),
        ],
        "callbacks": ["on_add", "on_update", "on_delete"],
    },
    "settings": {
        "description": "Settings dialog with options and save button",
        "widgets": [
            ("label", "Theme:", "theme_label"),
            ("combobox", "", "theme_combo", {"values": ["Light", "Dark"]}),
            ("checkbutton", "Auto-save", "autosave_check"),
            ("checkbutton", "Notifications", "notify_check"),
            ("button", "Save", "save_button", {"command": "on_save"}),
            ("button", "Cancel", "cancel_button", {"command": "on_cancel"}),
        ],
        "callbacks": ["on_save", "on_cancel"],
    },
}

WIDGET_MAP = {
    "label": "ttk.Label",
    "entry": "ttk.Entry",
    "button": "ttk.Button",
    "treeview": "ttk.Treeview",
    "text": "tk.Text",
    "combobox": "ttk.Combobox",
    "checkbutton": "ttk.Checkbutton",
    "labelframe": "ttk.Labelframe",
    "notebook": "ttk.Notebook",
}

def get_template(name):
    """Get template by name"""
    return TEMPLATES.get(name)

def list_templates():
    """List templates"""
    return [(name, tmpl["description"]) for name, tmpl in TEMPLATES.items()]

def generate_from_template(template_name):
    """Generate UI XML"""
    template = get_template(template_name)
    if not template:
        return None
    
    xml = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<interface version="1.2">',
        '  <object class="tk.Toplevel" id="mainwindow">',
        f'    <property name="title">{template_name.title()}</property>',
        '    <property name="height">400</property>',
        '    <property name="width">600</property>',
        '    <child>',
        '      <object class="ttk.Frame" id="mainframe">',
        '        <property name="padding">20</property>',
        '        <layout manager="pack">',
        '          <property name="expand">true</property>',
        '          <property name="fill">both</property>',
        '        </layout>',
    ]
    
    for i, widget_data in enumerate(template["widgets"], 1):
        widget_type = widget_data[0]
        text = widget_data[1] if len(widget_data) > 1 else ""
        widget_id = widget_data[2] if len(widget_data) > 2 else f"{widget_type}{i}"
        props = widget_data[3] if len(widget_data) > 3 else {}
        
        widget_class = WIDGET_MAP.get(widget_type, "ttk.Label")
        xml.extend([
            '        <child>',
            f'          <object class="{widget_class}" id="{widget_id}">',
        ])
        
        if text:
            xml.append(f'            <property name="text">{text}</property>')
        
        for key, value in props.items():
            xml.append(f'            <property name="{key}">{value}</property>')
        
        xml.extend([
            '            <layout manager="pack"><property name="pady">5</property></layout>',
            '          </object>',
            '        </child>',
        ])
    
    xml.extend(['      </object>', '    </child>', '  </object>', '</interface>'])
    return '\n'.join(xml)

def generate_callbacks(template_name):
    """Generate callback methods"""
    template = get_template(template_name)
    if not template or not template.get("callbacks"):
        return ""
    
    code = []
    for callback in template["callbacks"]:
        code.append(f'    def {callback}(self):\n        print("{callback} triggered")\n')
    
    return '\n'.join(code)
