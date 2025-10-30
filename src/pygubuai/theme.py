#!/usr/bin/env python3
"""Theme switcher for pygubu projects"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
import shutil
from .registry import Registry

AVAILABLE_THEMES = {
    "default": "Default system theme",
    "clam": "Modern flat theme",
    "alt": "Alternative theme",
    "classic": "Classic Tk theme",
    "vista": "Windows Vista theme (Windows only)",
    "xpnative": "Windows XP theme (Windows only)",
    "aqua": "macOS native theme (macOS only)",
}

def list_themes():
    """List all available themes"""
    return AVAILABLE_THEMES

def apply_theme(project_name: str, theme_name: str, backup: bool = True) -> bool:
    """Apply theme to project UI file"""
    if theme_name not in AVAILABLE_THEMES:
        raise ValueError(f"Unknown theme: {theme_name}. Available: {', '.join(AVAILABLE_THEMES.keys())}")
    
    registry = Registry()
    project_path = registry.get_project(project_name)
    
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")
    
    ui_file = Path(project_path) / f"{project_name}.ui"
    if not ui_file.exists():
        raise FileNotFoundError(f"UI file not found: {ui_file}")
    
    # Backup
    if backup:
        backup_file = ui_file.with_suffix('.ui.bak')
        shutil.copy2(ui_file, backup_file)
    
    # Parse and modify
    tree = ET.parse(ui_file)
    root = tree.getroot()
    
    # Find or create theme property in root widget
    root_object = root.find(".//object[@class='tk.Toplevel']")
    if root_object is None:
        root_object = root.find(".//object")
    
    if root_object is not None:
        # Remove existing theme property
        for prop in root_object.findall("property[@name='theme']"):
            root_object.remove(prop)
        
        # Add new theme property
        theme_prop = ET.SubElement(root_object, "property", name="theme")
        theme_prop.text = theme_name
    
    # Write back
    tree.write(ui_file, encoding='utf-8', xml_declaration=True)
    return True

def get_current_theme(project_name: str) -> Optional[str]:
    """Get current theme from project"""
    registry = Registry()
    project_path = registry.get_project(project_name)
    
    if not project_path:
        return None
    
    ui_file = Path(project_path) / f"{project_name}.ui"
    if not ui_file.exists():
        return None
    
    try:
        tree = ET.parse(ui_file)
        root = tree.getroot()
        theme_prop = root.find(".//property[@name='theme']")
        return theme_prop.text if theme_prop is not None else "default"
    except:
        return None

def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: pygubu-theme <command> [args]")
        print("Commands:")
        print("  list                    - List available themes")
        print("  <project> <theme>       - Apply theme to project")
        print("  <project> --current     - Show current theme")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        print("\\nAvailable Themes:\\n")
        for theme, desc in AVAILABLE_THEMES.items():
            print(f"  {theme:12} - {desc}")
        print()
    
    elif len(sys.argv) == 3:
        project_name = sys.argv[1]
        
        if sys.argv[2] == "--current":
            theme = get_current_theme(project_name)
            if theme:
                print(f"Current theme: {theme}")
            else:
                print("Could not determine current theme")
        else:
            theme_name = sys.argv[2]
            try:
                apply_theme(project_name, theme_name)
                print(f"✓ Applied theme '{theme_name}' to project '{project_name}'")
                print(f"  Backup saved as {project_name}.ui.bak")
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
    else:
        print("Invalid arguments")
        sys.exit(1)

if __name__ == "__main__":
    main()
