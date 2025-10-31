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
    from .theme_presets import THEME_PRESETS, list_presets, get_preset
    from .theme_advanced import apply_preset as apply_preset_advanced, get_preset_info
    from .theme_builder import create_custom_theme, export_theme, import_theme, list_custom_themes
    from .theme_preview import preview_theme
    
    if len(sys.argv) < 2:
        print("Usage: pygubu-theme <command> [args]")
        print("Commands:")
        print("  list [--presets]        - List available themes")
        print("  info <theme>            - Show theme details")
        print("  apply <project> <theme> - Apply theme/preset to project")
        print("  preview <project> <theme> - Preview theme without saving")
        print("  current <project>       - Show current theme")
        print("  create <name>           - Create custom theme")
        print("  export <name> [file]    - Export theme")
        print("  import <file>           - Import theme")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        show_presets = "--presets" in sys.argv or len(sys.argv) == 2
        
        print("\nAvailable Themes:\n")
        print("Basic Themes:")
        for theme, desc in AVAILABLE_THEMES.items():
            print(f"  {theme:15} - {desc}")
        
        if show_presets:
            print("\nTheme Presets:")
            for name in list_presets():
                preset = get_preset(name)
                print(f"  {name:15} - {preset['description']}")
            
            custom = list_custom_themes()
            if custom:
                print("\nCustom Themes:")
                for name in custom:
                    print(f"  {name:15} - Custom theme")
        print()
    
    elif command == "info" and len(sys.argv) == 3:
        theme_name = sys.argv[2]
        info = get_preset_info(theme_name)
        if info:
            print(f"\nTheme: {info['name']}")
            print(f"Description: {info['description']}")
            print(f"Base: {info['base']}")
            print(f"\nColors:")
            for key, value in info['colors'].items():
                print(f"  {key:15} {value}")
        else:
            print(f"Theme '{theme_name}' not found")
    
    elif command == "apply" and len(sys.argv) == 4:
        project_name = sys.argv[2]
        theme_name = sys.argv[3]
        
        try:
            # Try preset first
            if theme_name in THEME_PRESETS:
                apply_preset_advanced(project_name, theme_name)
                print(f"OK Applied preset '{theme_name}' to project '{project_name}'")
            else:
                # Try basic theme
                apply_theme(project_name, theme_name)
                print(f"OK Applied theme '{theme_name}' to project '{project_name}'")
            print(f"  Backup saved as {project_name}.ui.bak")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif command == "preview" and len(sys.argv) >= 4:
        project_name = sys.argv[2]
        theme_name = sys.argv[3]
        try:
            preview_theme(project_name, theme_name)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif command == "current" and len(sys.argv) == 3:
        project_name = sys.argv[2]
        theme = get_current_theme(project_name)
        if theme:
            print(f"Current theme: {theme}")
        else:
            print("Could not determine current theme")
    
    elif command == "create" and len(sys.argv) >= 3:
        name = sys.argv[2]
        print(f"Creating custom theme: {name}")
        print("Enter colors (or press Enter for defaults):")
        
        colors = {}
        for key in ["bg", "fg", "accent", "button_bg", "button_fg", "entry_bg", "entry_fg"]:
            value = input(f"  {key} (#hex): ").strip()
            if value:
                colors[key] = value
        
        if not colors:
            print("No colors provided, using defaults")
            colors = {"bg": "#ffffff", "fg": "#000000", "accent": "#0078d4"}
        
        try:
            create_custom_theme(name, colors=colors)
            print(f"OK Theme '{name}' created")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif command == "export" and len(sys.argv) >= 3:
        name = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else f"{name}.json"
        try:
            export_theme(name, output)
            print(f"OK Theme '{name}' exported to {output}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif command == "import" and len(sys.argv) == 3:
        source = sys.argv[2]
        try:
            name = import_theme(source)
            print(f"OK Theme '{name}' imported")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    else:
        print("Invalid command or arguments")
        sys.exit(1)

if __name__ == "__main__":
    main()
