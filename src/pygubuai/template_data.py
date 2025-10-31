"""Project templates with consistent data structures and validation."""

from typing import List, Tuple, Dict, Any
import uuid

TEMPLATES = {
    "login": {
        "description": "Login form with username, password, and submit button",
        "widgets": [
            {"type": "label", "text": "Username:", "id": "username_label"},
            {"type": "entry", "text": "", "id": "username_entry"},
            {"type": "label", "text": "Password:", "id": "password_label"},
            {"type": "entry", "text": "", "id": "password_entry", "properties": {"show": "*"}},
            {"type": "button", "text": "Login", "id": "login_button", "properties": {"command": "on_login"}},
        ],
        "callbacks": ["on_login"],
    },
    "crud": {
        "description": "CRUD interface with form and data table",
        "widgets": [
            {"type": "label", "text": "Name:", "id": "name_label"},
            {"type": "entry", "text": "", "id": "name_entry"},
            {"type": "button", "text": "Add", "id": "add_button", "properties": {"command": "on_add"}},
            {"type": "button", "text": "Update", "id": "update_button", "properties": {"command": "on_update"}},
            {"type": "button", "text": "Delete", "id": "delete_button", "properties": {"command": "on_delete"}},
            {"type": "treeview", "text": "", "id": "data_table", "properties": {"columns": ["id", "name"]}},
        ],
        "callbacks": ["on_add", "on_update", "on_delete"],
    },
    "settings": {
        "description": "Settings dialog with options and save button",
        "widgets": [
            {"type": "label", "text": "Theme:", "id": "theme_label"},
            {"type": "combobox", "text": "", "id": "theme_combo", "properties": {"values": ["Light", "Dark"]}},
            {"type": "checkbutton", "text": "Auto-save", "id": "autosave_check"},
            {"type": "checkbutton", "text": "Notifications", "id": "notify_check"},
            {"type": "button", "text": "Save", "id": "save_button", "properties": {"command": "on_save"}},
            {"type": "button", "text": "Cancel", "id": "cancel_button", "properties": {"command": "on_cancel"}},
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
    "radiobutton": "ttk.Radiobutton",
    "progressbar": "ttk.Progressbar",
    "scale": "ttk.Scale",
    "scrollbar": "ttk.Scrollbar",
    "separator": "ttk.Separator",
    "spinbox": "ttk.Spinbox",
}


def get_template(name: str) -> Dict[str, Any]:
    """Get template by name.

    Args:
        name: Template name

    Returns:
        Template dictionary or None if not found
    """
    return TEMPLATES.get(name)  # type: ignore[return-value]


def list_templates() -> List[Tuple[str, str]]:
    """List all available templates.

    Returns:
        List of (name, description) tuples
    """
    return [(name, tmpl["description"]) for name, tmpl in TEMPLATES.items()]  # type: ignore[misc]


def validate_widget(widget: Dict[str, Any]) -> None:
    """Validate widget structure.

    Args:
        widget: Widget dictionary

    Raises:
        ValueError: If widget is invalid
    """
    if "type" not in widget:
        raise ValueError(f"Widget missing 'type' field: {widget}")
    if widget["type"] not in WIDGET_MAP:
        raise ValueError(f"Unknown widget type: {widget['type']}")
    if "id" not in widget:
        raise ValueError(f"Widget missing 'id' field: {widget}")


def get_template_widgets_and_callbacks(template_name: str) -> Tuple[List[Tuple[str, Dict[str, Any]]], str]:
    """Extract widgets and callback code from template.

    Args:
        template_name: Name of the template

    Returns:
        Tuple of (widget list, callback code string)

    Raises:
        ValueError: If template is invalid
    """
    template = get_template(template_name)
    if not template:
        raise ValueError(f"Template not found: {template_name}")

    widgets_for_generator = []
    used_ids = set()

    for widget_data in template["widgets"]:
        validate_widget(widget_data)

        widget_type = widget_data["type"]
        text = widget_data.get("text", "")
        widget_id = widget_data["id"]
        props = widget_data.get("properties", {})

        # Ensure unique IDs
        if widget_id in used_ids:
            widget_id = f"{widget_id}_{uuid.uuid4().hex[:8]}"
        used_ids.add(widget_id)

        config = {"class": WIDGET_MAP[widget_type], "properties": {}, "id": widget_id}
        if text:
            config["properties"]["text"] = text
        config["properties"].update(props)

        widgets_for_generator.append((widget_type, config))

    code = []
    for callback in template.get("callbacks", []):
        code.append(f'    def {callback}(self):\n        """Handle {callback} event."""\n        pass\n')

    return widgets_for_generator, "\n".join(code)
