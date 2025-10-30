#!/usr/bin/env python3
"""AI-powered pygubu project creator"""
import sys
import pathlib
import pygubuai_widgets

def parse_description(description):
    """Extract widgets and features from description"""
    return pygubuai_widgets.detect_widgets(description)

def generate_ui(name, description):
    """Generate UI XML from description"""
    widgets = parse_description(description)
    
    xml = [
        "<?xml version='1.0' encoding='utf-8'?>",
        '<interface version="1.2">',
        '  <object class="tk.Toplevel" id="mainwindow">',
        f'    <property name="title">{name.replace("_", " ").title()}</property>',
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
    
    for i, (widget_type, config) in enumerate(widgets, 1):
        widget_id = f"{widget_type}{i}"
        xml.extend(pygubuai_widgets.generate_widget_xml(widget_type, widget_id, config, i))
    
    xml.extend(['      </object>', '    </child>', '  </object>', '</interface>'])
    return '\n'.join(xml)

def generate_python(name, widgets):
    """Generate Python application code"""
    class_name = name.replace('_', ' ').title().replace(' ', '')
    callbacks = pygubuai_widgets.get_callbacks(widgets)
    
    code = f'''#!/usr/bin/env python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "{name}.ui"

class {class_name}App:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow', master)
        self.builder.connect_callbacks(self)
'''
    
    for callback in callbacks:
        code += f'''
    def {callback}(self):
        """Handle {callback.replace('on_', '').replace('_', ' ')}""" 
        print("{callback} triggered")
'''
    
    code += f'''
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = {class_name}App()
    app.run()
'''
    return code

def create_project(name, description):
    """Create complete pygubu project from description"""
    base = pathlib.Path.cwd() / name
    base.mkdir(exist_ok=True)
    
    # Generate UI
    ui_content = generate_ui(name, description)
    ui_file = base / f"{name}.ui"
    ui_file.write_text(ui_content)
    
    # Generate Python
    widgets = parse_description(description)
    py_content = generate_python(name, widgets)
    py_file = base / f"{name}.py"
    py_file.write_text(py_content)
    py_file.chmod(0o755)
    
    # Create README
    readme = base / "README.md"
    readme.write_text(f'''# {name.replace("_", " ").title()}

{description}

## Run
```bash
python {name}.py
```

## Edit UI
```bash
~/pygubu-designer {name}.ui
```
''')
    
    print(f"✓ Created project: {base}/")
    print(f"  Description: {description}")
    print(f"\n📁 Files created:")
    print(f"  - {name}.ui")
    print(f"  - {name}.py")
    print(f"  - README.md")
    print(f"\n🚀 Next steps:")
    print(f"  cd {name}")
    print(f"  python {name}.py              # Run app")
    print(f"  ~/pygubu-designer {name}.ui   # Edit UI")

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    
    if len(args) != 2:
        print("Usage: pygubu-create <project_name> '<description>'")
        print("\nExamples:")
        print("  pygubu-create login 'login form with username, password, and button'")
        print("  pygubu-create todo 'todo app with entry, button, and list'")
        print("  pygubu-create notes 'note taking app with text area and buttons'")
        sys.exit(1)
    
    create_project(args[0], args[1])

if __name__ == '__main__':
    main()
