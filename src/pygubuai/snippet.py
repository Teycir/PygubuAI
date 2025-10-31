#!/usr/bin/env python3
"""XML snippet generator for common widgets"""
from typing import Dict, Optional

SNIPPET_TEMPLATES = {
    "button": """    <object class="ttk.Button" id="{id}">
      <property name="text">{text}</property>
      <property name="command">{command}</property>
      <layout manager="pack">
        <property name="pady">5</property>
      </layout>
    </object>""",

    "entry": """    <object class="ttk.Entry" id="{id}">
      <property name="textvariable">{variable}</property>
      <layout manager="pack">
        <property name="pady">5</property>
        <property name="fill">x</property>
      </layout>
    </object>""",

    "label": """    <object class="ttk.Label" id="{id}">
      <property name="text">{text}</property>
      <layout manager="pack">
        <property name="pady">5</property>
      </layout>
    </object>""",

    "frame": """    <object class="ttk.Frame" id="{id}">
      <property name="padding">10</property>
      <layout manager="{layout}">
        <property name="expand">true</property>
        <property name="fill">both</property>
      </layout>
    </object>""",

    "combobox": """    <object class="ttk.Combobox" id="{id}">
      <property name="textvariable">{variable}</property>
      <property name="values">{values}</property>
      <layout manager="pack">
        <property name="pady">5</property>
      </layout>
    </object>""",

    "checkbutton": """    <object class="ttk.Checkbutton" id="{id}">
      <property name="text">{text}</property>
      <property name="variable">{variable}</property>
      <layout manager="pack">
        <property name="pady">5</property>
      </layout>
    </object>""",

    "text": """    <object class="tk.Text" id="{id}">
      <property name="height">{height}</property>
      <layout manager="pack">
        <property name="expand">true</property>
        <property name="fill">both</property>
      </layout>
    </object>""",

    "treeview": """    <object class="ttk.Treeview" id="{id}">
      <property name="columns">{columns}</property>
      <layout manager="pack">
        <property name="expand">true</property>
        <property name="fill">both</property>
      </layout>
    </object>""",
}

DEFAULT_VALUES = {
    "button": {"id": "button_1", "text": "Button", "command": "on_button_click"},
    "entry": {"id": "entry_1", "variable": "entry_var"},
    "label": {"id": "label_1", "text": "Label"},
    "frame": {"id": "frame_1", "layout": "pack"},
    "combobox": {"id": "combobox_1", "variable": "combo_var", "values": "Option1 Option2 Option3"},
    "checkbutton": {"id": "check_1", "text": "Option", "variable": "check_var"},
    "text": {"id": "text_1", "height": "10"},
    "treeview": {"id": "tree_1", "columns": "col1 col2"},
}

def generate_snippet(widget_type: str, **kwargs) -> str:
    """Generate XML snippet for widget"""
    if widget_type not in SNIPPET_TEMPLATES:
        raise ValueError(f"Unknown widget type: {widget_type}")

    # Merge defaults with provided values
    values = DEFAULT_VALUES[widget_type].copy()
    values.update(kwargs)

    return SNIPPET_TEMPLATES[widget_type].format(**values)

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: pygubu-snippet <widget_type> [text] [options]")
        print("\\nAvailable widgets:")
        for widget in SNIPPET_TEMPLATES.keys():
            print(f"  {widget}")
        print("\\nExamples:")
        print("  pygubu-snippet button 'Submit' --command on_submit")
        print("  pygubu-snippet entry 'Email' --variable email_var")
        print("  pygubu-snippet frame --layout grid")
        sys.exit(1)

    widget_type = sys.argv[1]

    if widget_type not in SNIPPET_TEMPLATES:
        print(f"Error: Unknown widget type '{widget_type}'")
        print(f"Available: {', '.join(SNIPPET_TEMPLATES.keys())}")
        sys.exit(1)

    # Parse arguments
    kwargs = {}

    # Get text if provided (first non-option argument)
    if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
        if widget_type in ["button", "label", "checkbutton"]:
            kwargs["text"] = sys.argv[2]
        elif widget_type in ["entry", "combobox"]:
            # Use text as variable name (sanitized)
            var_name = sys.argv[2].lower().replace(' ', '_') + '_var'
            kwargs["variable"] = var_name

    # Parse --options
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            option = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                kwargs[option] = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        else:
            i += 1

    try:
        snippet = generate_snippet(widget_type, **kwargs)
        print("\\n" + snippet + "\\n")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
