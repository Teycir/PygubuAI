"""Professional theme presets for PygubuAI"""

THEME_PRESETS = {
    "modern-dark": {
        "name": "Modern Dark",
        "description": "Dark mode with blue accents",
        "base": "clam",
        "colors": {
            "bg": "#2b2b2b",
            "fg": "#fffff",
            "accent": "#0078d4",
            "button_bg": "#0e639c",
            "button_fg": "#fffff",
            "entry_bg": "#3c3c3c",
            "entry_fg": "#fffff",
            "select_bg": "#0078d4",
            "select_fg": "#fffff",
            "disabled_fg": "#808080",
        },
    },
    "modern-light": {
        "name": "Modern Light",
        "description": "Clean light theme",
        "base": "clam",
        "colors": {
            "bg": "#fffff",
            "fg": "#000000",
            "accent": "#0078d4",
            "button_bg": "#e1e1e1",
            "button_fg": "#000000",
            "entry_bg": "#f3f3f3",
            "entry_fg": "#000000",
            "select_bg": "#0078d4",
            "select_fg": "#fffff",
            "disabled_fg": "#a0a0a0",
        },
    },
    "material": {
        "name": "Material Design",
        "description": "Google Material Design colors",
        "base": "clam",
        "colors": {
            "bg": "#fafafa",
            "fg": "#212121",
            "accent": "#2196f3",
            "button_bg": "#2196f3",
            "button_fg": "#fffff",
            "entry_bg": "#fffff",
            "entry_fg": "#212121",
            "select_bg": "#2196f3",
            "select_fg": "#fffff",
            "disabled_fg": "#9e9e9e",
        },
    },
    "nord": {
        "name": "Nord",
        "description": "Nordic cool palette",
        "base": "clam",
        "colors": {
            "bg": "#2e3440",
            "fg": "#d8dee9",
            "accent": "#88c0d0",
            "button_bg": "#5e81ac",
            "button_fg": "#eceff4",
            "entry_bg": "#3b4252",
            "entry_fg": "#d8dee9",
            "select_bg": "#88c0d0",
            "select_fg": "#2e3440",
            "disabled_fg": "#4c566a",
        },
    },
    "solarized-dark": {
        "name": "Solarized Dark",
        "description": "Popular Solarized dark scheme",
        "base": "clam",
        "colors": {
            "bg": "#002b36",
            "fg": "#839496",
            "accent": "#268bd2",
            "button_bg": "#073642",
            "button_fg": "#93a1a1",
            "entry_bg": "#073642",
            "entry_fg": "#839496",
            "select_bg": "#268bd2",
            "select_fg": "#fdf6e3",
            "disabled_fg": "#586e75",
        },
    },
    "solarized-light": {
        "name": "Solarized Light",
        "description": "Solarized light variant",
        "base": "clam",
        "colors": {
            "bg": "#fdf6e3",
            "fg": "#657b83",
            "accent": "#268bd2",
            "button_bg": "#eee8d5",
            "button_fg": "#586e75",
            "entry_bg": "#eee8d5",
            "entry_fg": "#657b83",
            "select_bg": "#268bd2",
            "select_fg": "#fdf6e3",
            "disabled_fg": "#93a1a1",
        },
    },
    "high-contrast": {
        "name": "High Contrast",
        "description": "WCAG AAA compliant",
        "base": "clam",
        "colors": {
            "bg": "#000000",
            "fg": "#fffff",
            "accent": "#ffff00",
            "button_bg": "#fffff",
            "button_fg": "#000000",
            "entry_bg": "#000000",
            "entry_fg": "#fffff",
            "select_bg": "#ffff00",
            "select_fg": "#000000",
            "disabled_fg": "#808080",
        },
    },
    "dracula": {
        "name": "Dracula",
        "description": "Popular dark theme for developers",
        "base": "clam",
        "colors": {
            "bg": "#282a36",
            "fg": "#f8f8f2",
            "accent": "#bd93f9",
            "button_bg": "#44475a",
            "button_fg": "#f8f8f2",
            "entry_bg": "#44475a",
            "entry_fg": "#f8f8f2",
            "select_bg": "#bd93f9",
            "select_fg": "#282a36",
            "disabled_fg": "#6272a4",
        },
    },
}


def get_preset(name: str) -> dict:
    """Get theme preset by name"""
    return THEME_PRESETS.get(name)


def list_presets() -> list:
    """List all preset names"""
    return list(THEME_PRESETS.keys())


def validate_preset(preset_data: dict) -> bool:
    """Validate preset structure"""
    required = ["name", "description", "base", "colors"]
    if not all(k in preset_data for k in required):
        return False

    required_colors = ["bg", "fg", "accent"]
    if not all(k in preset_data["colors"] for k in required_colors):
        return False

    # Validate hex colors
    for color in preset_data["colors"].values():
        if not color.startswith("#") or len(color) != 7:
            return False

    return True
