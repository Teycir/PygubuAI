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
    "dashboard": {
        "description": "Dashboard with multiple panels",
        "widgets": [
            ("label", "Dashboard", "title_label"),
            ("labelframe", "Statistics", "stats_frame"),
            ("labelframe", "Recent Activity", "activity_frame"),
            ("button", "Refresh", "refresh_button", {"command": "on_refresh"}),
        ],
        "callbacks": ["on_refresh"],
    },
    "wizard": {
        "description": "Multi-step wizard interface",
        "widgets": [
            ("label", "Step 1 of 3", "step_label"),
            ("notebook", "", "wizard_notebook"),
            ("button", "Previous", "prev_button", {"command": "on_previous"}),
            ("button", "Next", "next_button", {"command": "on_next"}),
            ("button", "Finish", "finish_button", {"command": "on_finish"}),
        ],
        "callbacks": ["on_previous", "on_next", "on_finish"],
    },
}

def get_template(name):
    """Get template by name"""
    return TEMPLATES.get(name)

def list_templates():
    """List templates"""
    return [(name, tmpl["description"]) for name, tmpl in TEMPLATES.items()]

def get_template_widgets_and_callbacks(template_name: str) -> Tuple[List[Tuple], List[str]]:
    """Extract widgets and callbacks from template."""
    from .errors import PygubuAIError
    
    template = get_template(template_name)
    if not template:
        raise PygubuAIError(f"Template '{template_name}' not found.")
    
    return template["widgets"], template.get("callbacks", [])
