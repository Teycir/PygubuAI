"""Custom theme builder for PygubuAI"""
import json
from pathlib import Path
from typing import Optional
from .theme_presets import validate_preset

def get_themes_dir() -> Path:
    """Get user themes directory"""
    themes_dir = Path.home() / ".pygubuai" / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)
    return themes_dir


def create_custom_theme(name: str, base: str = "clam", colors: dict = None,
                       description: str = "") -> dict:
    """Create custom theme"""
    theme_data = {
        "name": name,
        "description": description or f"Custom theme: {name}",
        "base": base,
        "colors": colors or {}
    }

    if not validate_preset(theme_data):
        raise ValueError("Invalid theme data")

    save_theme(name, theme_data)
    return theme_data


def save_theme(name: str, theme_data: dict):
    """Save theme to user directory"""
    themes_dir = get_themes_dir()
    theme_file = themes_dir / f"{name}.json"

    with open(theme_file, 'w') as f:
        json.dump(theme_data, f, indent=2)


def load_theme(name: str) -> Optional[dict]:
    """Load theme from user directory"""
    themes_dir = get_themes_dir()
    theme_file = themes_dir / f"{name}.json"

    if not theme_file.exists():
        return None

    with open(theme_file, 'r') as f:
        return json.load(f)


def list_custom_themes() -> list:
    """List all custom themes"""
    themes_dir = get_themes_dir()
    return [f.stem for f in themes_dir.glob("*.json")]


def export_theme(name: str, output_path: str = None) -> str:
    """Export theme to file"""
    theme = load_theme(name)
    if not theme:
        raise ValueError(f"Theme '{name}' not found")

    if output_path is None:
        output_path = f"{name}.json"

    with open(output_path, 'w') as f:
        json.dump(theme, f, indent=2)

    return output_path


def import_theme(source: str):
    """Import theme from file"""
    with open(source, 'r') as f:
        theme_data = json.load(f)

    if not validate_preset(theme_data):
        raise ValueError("Invalid theme file")

    save_theme(theme_data['name'], theme_data)
    return theme_data['name']
