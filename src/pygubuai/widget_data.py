"""Widget library database"""

WIDGET_LIBRARY = {
    # Input Widgets
    "ttk.Entry": {
        "category": "input",
        "description": "Single-line text input field",
        "properties": ["textvariable", "width", "show", "state"],
        "use_cases": ["Text input", "Password fields", "Search boxes"],
    },
    "tk.Text": {
        "category": "input",
        "description": "Multi-line text editor",
        "properties": ["height", "width", "wrap", "state"],
        "use_cases": ["Text editors", "Log viewers", "Comments"],
    },
    "ttk.Combobox": {
        "category": "input",
        "description": "Dropdown selection with optional text entry",
        "properties": ["values", "textvariable", "state"],
        "use_cases": ["Dropdowns", "Autocomplete", "Selection lists"],
    },
    "ttk.Spinbox": {
        "category": "input",
        "description": "Numeric input with increment/decrement buttons",
        "properties": ["from_", "to", "increment", "textvariable"],
        "use_cases": ["Numeric input", "Quantity selectors", "Counters"],
    },
    "ttk.Checkbutton": {
        "category": "input",
        "description": "Boolean checkbox option",
        "properties": ["text", "variable", "command"],
        "use_cases": ["Options", "Toggles", "Multi-select"],
    },
    "ttk.Radiobutton": {
        "category": "input",
        "description": "Single selection from group",
        "properties": ["text", "variable", "value", "command"],
        "use_cases": ["Single choice", "Option groups", "Settings"],
    },
    "ttk.Scale": {
        "category": "input",
        "description": "Slider for numeric range selection",
        "properties": ["from_", "to", "orient", "variable"],
        "use_cases": ["Volume controls", "Brightness", "Range selection"],
    },
    # Display Widgets
    "ttk.Label": {
        "category": "display",
        "description": "Static text or image display",
        "properties": ["text", "textvariable", "image", "anchor"],
        "use_cases": ["Labels", "Titles", "Status text"],
    },
    "ttk.Progressbar": {
        "category": "display",
        "description": "Progress indicator bar",
        "properties": ["mode", "maximum", "value", "variable"],
        "use_cases": ["Loading indicators", "Progress tracking", "Status bars"],
    },
    "tk.Canvas": {
        "category": "display",
        "description": "Drawing and graphics area",
        "properties": ["width", "height", "bg"],
        "use_cases": ["Graphics", "Charts", "Custom drawings"],
    },
    "tk.Listbox": {
        "category": "display",
        "description": "Scrollable list of items",
        "properties": ["height", "selectmode", "listvariable"],
        "use_cases": ["Item lists", "File browsers", "Selection lists"],
    },
    "ttk.Treeview": {
        "category": "display",
        "description": "Hierarchical tree or table view",
        "properties": ["columns", "show", "selectmode"],
        "use_cases": ["Tables", "File trees", "Hierarchical data"],
    },
    # Action Widgets
    "ttk.Button": {
        "category": "action",
        "description": "Clickable button",
        "properties": ["text", "command", "state", "width"],
        "use_cases": ["Actions", "Submit forms", "Navigation"],
    },
    "ttk.Menubutton": {
        "category": "action",
        "description": "Button that opens a menu",
        "properties": ["text", "menu"],
        "use_cases": ["Dropdown menus", "Context menus", "Options"],
    },
    "tk.Menu": {
        "category": "action",
        "description": "Menu bar or popup menu",
        "properties": ["tearof"],
        "use_cases": ["Menu bars", "Context menus", "Submenus"],
    },
    # Container Widgets
    "ttk.Frame": {
        "category": "container",
        "description": "Container for grouping widgets",
        "properties": ["padding", "relie", "borderwidth"],
        "use_cases": ["Layout groups", "Sections", "Panels"],
    },
    "ttk.LabelFrame": {
        "category": "container",
        "description": "Frame with labeled border",
        "properties": ["text", "padding"],
        "use_cases": ["Grouped options", "Sections", "Settings groups"],
    },
    "ttk.Notebook": {
        "category": "container",
        "description": "Tabbed container",
        "properties": [],
        "use_cases": ["Tabs", "Multi-page forms", "Settings panels"],
    },
    "ttk.PanedWindow": {
        "category": "container",
        "description": "Resizable split container",
        "properties": ["orient"],
        "use_cases": ["Split views", "Resizable panels", "Sidebars"],
    },
    "tk.Toplevel": {
        "category": "container",
        "description": "Separate window",
        "properties": ["title"],
        "use_cases": ["Dialogs", "Popups", "Secondary windows"],
    },
    # Scrolling
    "ttk.Scrollbar": {
        "category": "layout",
        "description": "Scrollbar for scrollable widgets",
        "properties": ["orient", "command"],
        "use_cases": ["Scroll lists", "Scroll text", "Scroll canvas"],
    },
    "ttk.Separator": {
        "category": "layout",
        "description": "Visual separator line",
        "properties": ["orient"],
        "use_cases": ["Visual dividers", "Section breaks", "Spacing"],
    },
    "ttk.Sizegrip": {
        "category": "layout",
        "description": "Window resize grip",
        "properties": [],
        "use_cases": ["Resizable windows", "Dialog corners"],
    },
}

CATEGORIES = {
    "input": "Input Widgets - User data entry",
    "display": "Display Widgets - Show information",
    "action": "Action Widgets - Trigger events",
    "container": "Container Widgets - Group other widgets",
    "layout": "Layout Widgets - Arrange and organize",
}
