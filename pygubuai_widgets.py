#!/usr/bin/env python3
"""Enhanced widget detection and generation"""

WIDGET_PATTERNS = {
    "label": {
        "keywords": ["label", "title", "heading", "text"],
        "class": "ttk.Label",
        "properties": {"text": "Label"},
    },
    "entry": {
        "keywords": ["entry", "input", "field", "textbox"],
        "class": "ttk.Entry",
        "properties": {},
    },
    "button": {
        "keywords": ["button", "submit", "click", "action"],
        "class": "ttk.Button",
        "properties": {"text": "Button", "command": "on_button_click"},
    },
    "treeview": {
        "keywords": ["list", "table", "tree", "grid"],
        "class": "ttk.Treeview",
        "properties": {},
        "expand": True,
    },
    "text": {
        "keywords": ["text area", "textarea", "multiline", "editor"],
        "class": "tk.Text",
        "properties": {"height": "10"},
        "expand": True,
    },
    "combobox": {
        "keywords": ["dropdown", "select", "combo", "choice"],
        "class": "ttk.Combobox",
        "properties": {},
    },
    "checkbutton": {
        "keywords": ["checkbox", "check", "toggle"],
        "class": "ttk.Checkbutton",
        "properties": {"text": "Option"},
    },
    "radiobutton": {
        "keywords": ["radio", "option button"],
        "class": "ttk.Radiobutton",
        "properties": {"text": "Option"},
    },
    "scale": {
        "keywords": ["slider", "scale", "range"],
        "class": "ttk.Scale",
        "properties": {"from_": "0", "to": "100"},
    },
    "spinbox": {
        "keywords": ["spinner", "spinbox", "number"],
        "class": "ttk.Spinbox",
        "properties": {"from_": "0", "to": "100"},
    },
    "progressbar": {
        "keywords": ["progress", "loading", "bar"],
        "class": "ttk.Progressbar",
        "properties": {"mode": "determinate"},
    },
    "notebook": {
        "keywords": ["tabs", "notebook", "pages"],
        "class": "ttk.Notebook",
        "properties": {},
        "expand": True,
    },
    "panedwindow": {
        "keywords": ["paned", "split", "divider"],
        "class": "ttk.Panedwindow",
        "properties": {},
        "expand": True,
    },
    "labelframe": {
        "keywords": ["group", "section", "panel"],
        "class": "ttk.Labelframe",
        "properties": {"text": "Group"},
    },
    "separator": {
        "keywords": ["separator", "divider", "line"],
        "class": "ttk.Separator",
        "properties": {},
    },
    "canvas": {
        "keywords": ["canvas", "drawing", "graphics"],
        "class": "tk.Canvas",
        "properties": {},
        "expand": True,
    },
    "menu": {
        "keywords": ["menu", "menubar"],
        "class": "tk.Menu",
        "properties": {},
    },
}

CONTEXT_PATTERNS = {
    "form": ["label", "entry", "entry", "button"],
    "login": ["label", "entry", "label", "entry", "button"],
    "search": ["entry", "button", "treeview"],
    "editor": ["text", "button", "button"],
    "settings": ["checkbutton", "checkbutton", "combobox", "button"],
}

def detect_widgets(description):
    """Enhanced widget detection with context awareness"""
    desc_lower = description.lower()
    widgets = []
    
    # Check for context patterns first
    for context, widget_list in CONTEXT_PATTERNS.items():
        if context in desc_lower:
            return [(w, WIDGET_PATTERNS[w]) for w in widget_list if w in WIDGET_PATTERNS]
    
    # Individual widget detection
    for widget_type, config in WIDGET_PATTERNS.items():
        if any(keyword in desc_lower for keyword in config["keywords"]):
            widgets.append((widget_type, config))
    
    return widgets

def generate_widget_xml(widget_type, widget_id, config, index=1):
    """Generate XML for a widget"""
    xml = [
        '        <child>',
        f'          <object class="{config["class"]}" id="{widget_id}">',
    ]
    
    for prop, value in config["properties"].items():
        xml.append(f'            <property name="{prop}">{value}</property>')
    
    layout = '            <layout manager="pack">'
    if config.get("expand"):
        xml.append(layout)
        xml.append('              <property name="expand">true</property>')
        xml.append('              <property name="fill">both</property>')
        xml.append('            </layout>')
    else:
        xml.append(f'{layout}<property name="pady">5</property></layout>')
    
    xml.extend(['          </object>', '        </child>'])
    return xml

def get_callbacks(widgets):
    """Extract callback methods needed"""
    callbacks = set()
    for widget_type, config in widgets:
        if "command" in config.get("properties", {}):
            callbacks.add(config["properties"]["command"])
    return list(callbacks)
