"""Project templates"""
from typing import List, Tuple, Dict, Any

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

def get_template_widgets_and_callbacks(template_name: str) -> Tuple[List[Tuple[str, Dict[str, Any]]], str]:
    """Extract widgets and callback code from template."""
    template = get_template(template_name)
    if not template:
        return [], ""

    widgets_for_generator = []
    for i, widget_data in enumerate(template["widgets"], 1):
        widget_type = widget_data[0]
        text = widget_data[1] if len(widget_data) > 1 else ""
        widget_id = widget_data[2] if len(widget_data) > 2 else f"{widget_type}{i}"
        props = widget_data[3] if len(widget_data) > 3 else {}
        
        config = {"class": WIDGET_MAP.get(widget_type, "ttk.Label"), "properties": {}, "id": widget_id}
        if text:
            config["properties"]["text"] = text
        config["properties"].update(props)
        
        widgets_for_generator.append((widget_type, config))

    code = []
    for callback in template.get("callbacks", []):
        code.append(f'    def {callback}(self):\n        print("{callback} triggered")\n')
    
    return widgets_for_generator, '\n'.join(code)
