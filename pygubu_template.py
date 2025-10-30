#!/usr/bin/env python3
"""Create pygubu project from template"""
import sys
import pathlib
import pygubuai_templates

def create_from_template(name, template_name):
    """Create project from template"""
    template = pygubuai_templates.get_template(template_name)
    if not template:
        print(f"❌ Template '{template_name}' not found")
        print("\nAvailable templates:")
        for tmpl_name, desc in pygubuai_templates.list_templates():
            print(f"  {tmpl_name:12} - {desc}")
        sys.exit(1)
    
    base = pathlib.Path.cwd() / name
    base.mkdir(exist_ok=True)
    
    # Generate UI from template
    ui_content = pygubuai_templates.generate_from_template(template_name)
    ui_file = base / f"{name}.ui"
    ui_file.write_text(ui_content)
    
    # Generate Python with callbacks
    class_name = name.replace('_', ' ').title().replace(' ', '')
    callbacks = pygubuai_templates.generate_callbacks(template_name)
    
    py_content = f'''#!/usr/bin/env python3
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

{callbacks}
    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = {class_name}App()
    app.run()
'''
    
    py_file = base / f"{name}.py"
    py_file.write_text(py_content)
    py_file.chmod(0o755)
    
    # Create README
    readme = base / "README.md"
    readme.write_text(f'''# {name.replace("_", " ").title()}

Template: {template_name}
{template["description"]}

## Run
```bash
python {name}.py
```

## Edit UI
```bash
~/pygubu-designer {name}.ui
```
''')
    
    print(f"✓ Created project from '{template_name}' template: {base}/")
    print(f"\n📁 Files created:")
    print(f"  - {name}.ui")
    print(f"  - {name}.py")
    print(f"  - README.md")
    print(f"\n🚀 Next steps:")
    print(f"  cd {name}")
    print(f"  python {name}.py")

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    
    if len(args) == 1 and args[0] == 'list':
        print("Available templates:\n")
        for name, desc in pygubuai_templates.list_templates():
            print(f"  {name:12} - {desc}")
        sys.exit(0)
    
    if len(args) != 2:
        print("Usage: pygubu-template <project_name> <template>")
        print("       pygubu-template list")
        print("\nExamples:")
        print("  pygubu-template mylogin login")
        print("  pygubu-template myapp crud")
        print("  pygubu-template config settings")
        sys.exit(1)
    
    create_from_template(args[0], args[1])

if __name__ == '__main__':
    main()
