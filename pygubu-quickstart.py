#!/usr/bin/env python3
"""Quick starter for pygubu projects"""
import sys
import pathlib

def create_project(name):
    base = pathlib.Path.cwd() / name
    base.mkdir(exist_ok=True)
    
    # Create UI file
    ui_file = base / f"{name}.ui"
    ui_file.write_text(f'''<?xml version='1.0' encoding='utf-8'?>
<interface version="1.2">
  <object class="tk.Toplevel" id="mainwindow">
    <property name="title">{name.title()}</property>
    <property name="height">400</property>
    <property name="width">600</property>
    <child>
      <object class="ttk.Frame" id="mainframe">
        <property name="padding">20</property>
        <layout manager="pack">
          <property name="expand">true</property>
          <property name="fill">both</property>
        </layout>
      </object>
    </child>
  </object>
</interface>''')
    
    # Create Python file
    py_file = base / f"{name}.py"
    py_file.write_text(f'''#!/usr/bin/env python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "{name}.ui"

class {name.title().replace('_', '')}App:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('mainwindow', master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = {name.title().replace('_', '')}App()
    app.run()
''')
    py_file.chmod(0o755)
    
    print(f"✓ Created project: {base}")
    print(f"  - {ui_file.name}")
    print(f"  - {py_file.name}")
    print(f"\nNext steps:")
    print(f"  ~/pygubu-designer {ui_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: pygubu-quickstart <project_name>")
        sys.exit(1)
    create_project(sys.argv[1])
