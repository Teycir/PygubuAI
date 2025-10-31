"""Advanced theming engine for PygubuAI"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
import shutil
from .registry import Registry

WIDGET_COLOR_MAP = {
    "ttk.Button": {"background": "button_bg", "foreground": "button_fg"},
    "ttk.Entry": {"fieldbackground": "entry_bg", "foreground": "entry_fg"},
    "ttk.Label": {"background": "bg", "foreground": "fg"},
    "ttk.Frame": {"background": "bg"},
    "ttk.Combobox": {"fieldbackground": "entry_bg", "foreground": "entry_fg"},
    "tk.Text": {"background": "entry_bg", "foreground": "entry_fg"},
}


def apply_preset(project_name: str, preset_name: str, backup: bool = True) -> bool:
    """Apply theme preset to project"""
    preset = get_preset(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: {preset_name}")

    registry = Registry()
    project_path = registry.get_project(project_name)
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")

    ui_file = Path(project_path) / f"{project_name}.ui"
    if not ui_file.exists():
        raise FileNotFoundError(f"UI file not found: {ui_file}")

    if backup:
        shutil.copy2(ui_file, ui_file.with_suffix('.ui.bak'))

    tree = ET.parse(ui_file)
    root = tree.getroot()

    # Apply base theme
    root_object = root.find(".//object[@class='tk.Toplevel']") or root.find(".//object")
    if root_object is not None:
        for prop in root_object.findall("property[@name='theme']"):
            root_object.remove(prop)
        theme_prop = ET.SubElement(root_object, "property", name="theme")
        theme_prop.text = preset["base"]

    # Apply colors to widgets
    for obj in root.findall(".//object"):
        widget_class = obj.get("class")
        if widget_class in WIDGET_COLOR_MAP:
            apply_colors_to_widget(obj, preset["colors"], widget_class)

    tree.write(ui_file, encoding='utf-8', xml_declaration=True)
    return True


def apply_colors_to_widget(widget_element, colors: dict, widget_type: str):
    """Apply colors to widget based on type"""
    color_map = WIDGET_COLOR_MAP.get(widget_type, {})

    for prop_name, color_key in color_map.items():
        if color_key in colors:
            # Remove existing property
            for prop in widget_element.findall(f"property[@name='{prop_name}']"):
                widget_element.remove(prop)

            # Add new property
            prop = ET.SubElement(widget_element, "property", name=prop_name)
            prop.text = colors[color_key]


def get_preset_info(preset_name: str) -> Optional[dict]:
    """Get detailed preset information"""
    return get_preset(preset_name)
