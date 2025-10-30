"""Accessibility helpers for WCAG compliance."""
from typing import Dict, List, Tuple


def check_color_contrast(fg: str, bg: str) -> Tuple[bool, float]:
    """Check if color contrast meets WCAG AA standards (4.5:1)."""
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def luminance(rgb: Tuple[int, int, int]) -> float:
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    try:
        fg_rgb = hex_to_rgb(fg)
        bg_rgb = hex_to_rgb(bg)
        l1 = luminance(fg_rgb)
        l2 = luminance(bg_rgb)
        ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
        return ratio >= 4.5, ratio
    except:
        return False, 0.0


def generate_aria_labels(widget_type: str, widget_id: str) -> Dict[str, str]:
    """Generate ARIA labels for widgets."""
    labels = {
        "Button": f"Button: {widget_id}",
        "Entry": f"Text input: {widget_id}",
        "Label": f"Label: {widget_id}",
        "Checkbutton": f"Checkbox: {widget_id}",
        "Radiobutton": f"Radio button: {widget_id}",
        "Combobox": f"Dropdown: {widget_id}",
        "Scale": f"Slider: {widget_id}",
    }
    return {"aria-label": labels.get(widget_type, f"{widget_type}: {widget_id}")}


def validate_keyboard_navigation(widgets: List[Dict]) -> List[str]:
    """Validate keyboard navigation setup."""
    issues = []
    has_focus = any(w.get("takefocus") == "1" for w in widgets)
    
    if not has_focus:
        issues.append("No widgets have keyboard focus enabled")
    
    buttons = [w for w in widgets if w.get("class") == "ttk.Button"]
    if buttons and not any(b.get("underline") for b in buttons):
        issues.append("Buttons lack keyboard shortcuts (underline)")
    
    return issues


def check_accessibility(ui_data: Dict) -> Dict[str, List[str]]:
    """Run accessibility checks on UI data."""
    issues = {
        "contrast": [],
        "keyboard": [],
        "labels": []
    }
    
    widgets = ui_data.get("widgets", [])
    
    # Check keyboard navigation
    issues["keyboard"] = validate_keyboard_navigation(widgets)
    
    # Check for missing labels
    for widget in widgets:
        if widget.get("class") in ["ttk.Entry", "ttk.Combobox"] and not widget.get("label"):
            issues["labels"].append(f"Widget {widget.get('id')} missing label")
    
    return {k: v for k, v in issues.items() if v}
