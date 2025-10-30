"""Widget detection and generation"""
from typing import List, Tuple, Dict, Any

WIDGET_PATTERNS = {
    "label": {"keywords": ["label", "title", "heading"], "class": "ttk.Label", "properties": {"text": "Label"}},
    "entry": {"keywords": ["entry", "input", "field"], "class": "ttk.Entry", "properties": {}},
    "button": {"keywords": ["button", "submit", "click"], "class": "ttk.Button", "properties": {"text": "Button", "command": "on_button_click"}},
    "treeview": {"keywords": ["list", "table", "tree"], "class": "ttk.Treeview", "properties": {}, "expand": True},
    "text": {"keywords": ["text area", "textarea", "multiline"], "class": "tk.Text", "properties": {"height": "10"}, "expand": True},
    "combobox": {"keywords": ["dropdown", "select", "combo"], "class": "ttk.Combobox", "properties": {}},
    "checkbutton": {"keywords": ["checkbox", "check"], "class": "ttk.Checkbutton", "properties": {"text": "Option"}},
}

CONTEXT_PATTERNS = {
    "form": ["label", "entry", "entry", "button"],
    "login": ["label", "entry", "label", "entry", "button"],
    "search": ["entry", "button", "treeview"],
}

def detect_widgets(description):
    """Detect widgets from description"""
    desc_lower = description.lower()
    
    for context, widget_list in CONTEXT_PATTERNS.items():
        if context in desc_lower:
            return [(w, WIDGET_PATTERNS[w]) for w in widget_list if w in WIDGET_PATTERNS]
    
    widgets = []
    for widget_type, config in WIDGET_PATTERNS.items():
        if any(kw in desc_lower for kw in config["keywords"]):
            widgets.append((widget_type, config))
    
    return widgets if widgets else [("label", WIDGET_PATTERNS["label"]), ("button", WIDGET_PATTERNS["button"])]

def generate_widget_xml(widget_type: str, widget_id: str, config: dict, index: int = 1) -> List[str]:
    """Generate XML for widget"""
    xml = ['        <child>', f'          <object class="{config.get("class", "ttk.Label")}" id="{widget_id}">']
    
    for prop, value in config.get("properties", {}).items():
        xml.append(f'            <property name="{prop}">{value}</property>')
    
    layout = '            <layout manager="pack">'
    if config.get("expand"):
        xml.extend([layout, '              <property name="expand">true</property>', '              <property name="fill">both</property>', '            </layout>'])
    else:
        xml.append(f'{layout}<property name="pady">5</property></layout>')
    
    xml.extend(['          </object>', '        </child>'])
    return xml

def get_callbacks(widgets):
    """Extract callbacks"""
    callbacks = set()
    for _, config in widgets:
        if "command" in config.get("properties", {}):
            callbacks.add(config["properties"]["command"])
    return list(callbacks)
