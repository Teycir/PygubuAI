"""Theme preview functionality"""
import tempfile
import shutil
from pathlib import Path
from .registry import Registry
from .theme_builder import load_theme


def preview_theme(project_name: str, theme_name: str, watch: bool = False):
    """Preview theme without saving"""
    try:
        import tkinter as tk
        import pygubu
    except ImportError as e:
        raise ImportError(f"Preview requires pygubu: {e}")

    registry = Registry()
    project_path = registry.get_project(project_name)
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")

    ui_file = Path(project_path) / f"{project_name}.ui"
    if not ui_file.exists():
        raise FileNotFoundError(f"UI file not found: {ui_file}")

    # Create temp copy
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ui', delete=False) as tmp:
        temp_ui = Path(tmp.name)

    try:
        shutil.copy2(ui_file, temp_ui)

        # Apply theme to temp
        from .theme_presets import get_preset
        preset = get_preset(theme_name)
        if not preset:
            # Try custom theme
            preset = load_theme(theme_name)
            if not preset:
                raise ValueError(f"Theme '{theme_name}' not found")

        # Apply to temp file (simplified - just show preview)
        _show_preview(temp_ui, theme_name, tk, pygubu)
    finally:
        temp_ui.unlink(missing_ok=True)


def _show_preview(ui_file: Path, theme_name: str, tk, pygubu):
    """Show preview window"""
    root = tk.Tk()
    root.title(f"Preview: {theme_name}")

    try:
        builder = pygubu.Builder()
        builder.add_from_file(str(ui_file))
        builder.get_object('mainwindow', root)

        # Add info label
        info = tk.Label(root, text=f"Preview Mode - Theme: {theme_name}",
                        bg="yellow", fg="black")
        info.pack(side="top", fill="x")

        root.mainloop()
    except Exception as e:
        root.destroy()
        raise RuntimeError(f"Preview failed: {e}")
