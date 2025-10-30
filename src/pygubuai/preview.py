#!/usr/bin/env python3
"""Quick preview tool for UI files"""
import tkinter as tk
from pathlib import Path
from typing import Optional
import time
from .registry import Registry

def preview_ui(ui_file_path: str, watch: bool = False):
    """Preview UI file in Tkinter window"""
    try:
        import pygubu
    except ImportError:
        raise ImportError("pygubu is required for preview. Install: pip install pygubu")
    
    ui_path = Path(ui_file_path)
    if not ui_path.exists():
        raise FileNotFoundError(f"UI file not found: {ui_file_path}")
    
    last_mtime = ui_path.stat().st_mtime
    
    def create_window():
        root = tk.Tk()
        root.title(f"Preview: {ui_path.name}")
        
        builder = pygubu.Builder()
        try:
            builder.add_from_file(str(ui_path))
            builder.get_object('mainwindow', root)
        except Exception as e:
            # If mainwindow not found, try first object
            try:
                builder.add_from_file(str(ui_path))
                first_obj = list(builder.objects.keys())[0] if builder.objects else None
                if first_obj:
                    builder.get_object(first_obj, root)
                else:
                    raise ValueError("No objects found in UI file")
            except Exception as e2:
                tk.Label(root, text=f"Error loading UI:\\n{str(e2)}", fg="red", padx=20, pady=20).pack()
        
        if watch:
            def check_changes():
                nonlocal last_mtime
                try:
                    current_mtime = ui_path.stat().st_mtime
                    if current_mtime != last_mtime:
                        last_mtime = current_mtime
                        root.destroy()
                        create_window()
                except:
                    pass
                root.after(1000, check_changes)
            
            root.after(1000, check_changes)
        
        return root
    
    root = create_window()
    root.mainloop()

def preview_project(project_name: str, watch: bool = False):
    """Preview project by name"""
    registry = Registry()
    project_path = registry.get_project(project_name)
    
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")
    
    ui_file = Path(project_path) / f"{project_name}.ui"
    preview_ui(str(ui_file), watch)

def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: pygubu-preview <project_name|file.ui> [--watch]")
        print("\\nOptions:")
        print("  --watch    Auto-reload on file changes")
        sys.exit(1)
    
    target = sys.argv[1]
    watch = "--watch" in sys.argv
    
    try:
        if target.endswith('.ui'):
            preview_ui(target, watch)
        else:
            preview_project(target, watch)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
