# Advanced Theming System - PygubuAI v0.6.0

## Overview

The Advanced Theming System extends PygubuAI's basic theme support with professional color schemes, custom theme creation, and visual theme management.

## Features

### 1. Professional Theme Presets
Pre-built color schemes for modern applications:
- **modern-dark** - Dark mode with blue accents
- **modern-light** - Clean light theme with subtle shadows
- **material** - Google Material Design colors
- **nord** - Nordic-inspired cool palette
- **solarized-dark** - Popular Solarized dark scheme
- **solarized-light** - Solarized light variant
- **high-contrast** - WCAG AAA accessibility compliant
- **dracula** - Popular dark theme for developers

### 2. Custom Theme Builder
Create and save your own themes with color pickers and live preview.

### 3. Theme Preview Mode
See theme changes instantly without modifying files.

### 4. Theme Import/Export
Share themes with the community or across projects.

---

## Commands

### List Available Themes

```bash
# List all themes (basic + presets)
pygubu-theme list

# List only presets
pygubu-theme list --presets

# Show theme details
pygubu-theme info modern-dark
```

**Output:**
```
Available Themes:

Basic Themes:
  default      - Default system theme
  clam         - Modern flat theme
  alt          - Alternative theme
  classic      - Classic Tk theme

Theme Presets:
  modern-dark  - Dark mode with blue accents
  modern-light - Clean light theme
  material     - Google Material Design
  nord         - Nordic cool palette
  high-contrast - WCAG AAA compliant
```

---

### Apply Theme Preset

```bash
# Apply preset to project
pygubu-theme apply <project> <preset>

# Examples
pygubu-theme apply myapp modern-dark
pygubu-theme apply todo material
pygubu-theme apply settings high-contrast
```

**What it does:**
1. Backs up current `.ui` file
2. Applies color scheme to all widgets
3. Updates ttk theme setting
4. Saves changes

---

### Preview Theme

```bash
# Preview without saving
pygubu-theme preview <project> <preset>

# Preview with live reload
pygubu-theme preview <project> <preset> --watch
```

**What it does:**
- Opens preview window with theme applied
- No file modifications
- Close window to exit preview

---

### Create Custom Theme

```bash
# Interactive theme builder
pygubu-theme create <name>

# From existing theme
pygubu-theme create <name> --base modern-dark

# From JSON file
pygubu-theme create <name> --from theme.json
```

**Interactive prompts:**
```
Creating theme: my-theme

Base theme (default/modern-dark/material): modern-dark
Background color (#hex): #1e1e1e
Foreground color (#hex): #ffffff
Accent color (#hex): #007acc
Button background (#hex): #0e639c
Button foreground (#hex): #ffffff
...

✓ Theme 'my-theme' created
  Saved to: ~/.pygubuai/themes/my-theme.json
```

---

### Export Theme

```bash
# Export to file
pygubu-theme export <name> [--output theme.json]

# Export to clipboard
pygubu-theme export <name> --clipboard
```

**Output (theme.json):**
```json
{
  "name": "my-theme",
  "base": "modern-dark",
  "colors": {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "accent": "#007acc",
    "button_bg": "#0e639c",
    "button_fg": "#ffffff",
    "entry_bg": "#2d2d2d",
    "entry_fg": "#ffffff"
  },
  "ttk_theme": "clam"
}
```

---

### Import Theme

```bash
# Import from file
pygubu-theme import theme.json

# Import from URL
pygubu-theme import https://example.com/theme.json

# Import from GitHub gist
pygubu-theme import gist:<gist_id>
```

---

### Get Current Theme

```bash
# Show current theme
pygubu-theme current <project>

# Show with details
pygubu-theme current <project> --verbose
```

**Output:**
```
Current theme: modern-dark
Base: clam
Colors: 8 custom colors applied
Modified: 2024-01-15 10:30:00
```

---

### Batch Apply

```bash
# Apply to all projects
pygubu-theme apply-all <preset>

# Apply to specific projects
pygubu-theme apply-all <preset> --projects app1,app2,app3

# Dry run
pygubu-theme apply-all <preset> --dry-run
```

---

## Theme Preset Details

### modern-dark
```yaml
Description: Dark mode with blue accents
Base: clam
Colors:
  Background: #2b2b2b
  Foreground: #ffffff
  Accent: #0078d4
  Button: #0e639c / #ffffff
  Entry: #3c3c3c / #ffffff
Best for: Professional applications, developer tools
```

### modern-light
```yaml
Description: Clean light theme
Base: clam
Colors:
  Background: #ffffff
  Foreground: #000000
  Accent: #0078d4
  Button: #e1e1e1 / #000000
  Entry: #f3f3f3 / #000000
Best for: Business applications, data entry
```

### material
```yaml
Description: Google Material Design
Base: clam
Colors:
  Background: #fafafa
  Foreground: #212121
  Accent: #2196f3
  Button: #2196f3 / #ffffff
  Entry: #ffffff / #212121
Best for: Modern web-like applications
```

### nord
```yaml
Description: Nordic cool palette
Base: clam
Colors:
  Background: #2e3440
  Foreground: #d8dee9
  Accent: #88c0d0
  Button: #5e81ac / #eceff4
  Entry: #3b4252 / #d8dee9
Best for: Calm, focused applications
```

### high-contrast
```yaml
Description: WCAG AAA compliant
Base: clam
Colors:
  Background: #000000
  Foreground: #ffffff
  Accent: #ffff00
  Button: #ffffff / #000000
  Entry: #000000 / #ffffff
Best for: Accessibility, vision impairment
```

---

## Custom Theme Format

### JSON Structure

```json
{
  "name": "theme-name",
  "description": "Theme description",
  "author": "Your Name",
  "version": "1.0.0",
  "base": "clam",
  "colors": {
    "bg": "#hex",
    "fg": "#hex",
    "accent": "#hex",
    "button_bg": "#hex",
    "button_fg": "#hex",
    "entry_bg": "#hex",
    "entry_fg": "#hex",
    "select_bg": "#hex",
    "select_fg": "#hex",
    "disabled_fg": "#hex"
  },
  "widget_styles": {
    "TButton": {
      "background": "#hex",
      "foreground": "#hex",
      "borderwidth": 1,
      "relief": "flat"
    },
    "TEntry": {
      "fieldbackground": "#hex",
      "foreground": "#hex"
    }
  }
}
```

### Minimal Theme

```json
{
  "name": "simple-theme",
  "base": "clam",
  "colors": {
    "bg": "#ffffff",
    "fg": "#000000",
    "accent": "#0078d4"
  }
}
```

---

## Usage Examples

### Example 1: Apply Modern Dark Theme

```bash
# Create project
pygubu-create dashboard "dashboard with charts and tables"

# Apply modern dark theme
pygubu-theme apply dashboard modern-dark

# Preview
pygubu-preview dashboard
```

### Example 2: Create Custom Brand Theme

```bash
# Create theme interactively
pygubu-theme create company-brand

# Apply to project
pygubu-theme apply myapp company-brand

# Export for sharing
pygubu-theme export company-brand --output brand.json
```

### Example 3: Theme All Projects

```bash
# List projects
pygubu-register list

# Preview theme on one project
pygubu-theme preview app1 material

# Apply to all
pygubu-theme apply-all material
```

### Example 4: Import Community Theme

```bash
# Download theme
curl -o awesome-theme.json https://example.com/theme.json

# Import
pygubu-theme import awesome-theme.json

# Apply
pygubu-theme apply myapp awesome-theme
```

---

## Integration with Existing Features

### With Preview

```bash
# Preview with theme
pygubu-theme preview myapp modern-dark --watch
```

### With Batch Operations

```bash
# Apply theme to multiple projects
pygubu-batch apply-theme modern-dark --projects app1,app2
```

### With Validation

```bash
# Validate theme compatibility
pygubu-validate myapp --check-theme
```

---

## Theme Storage

### User Themes Directory

```
~/.pygubuai/themes/
├── my-theme.json
├── company-brand.json
└── custom-dark.json
```

### Project Theme Metadata

Stored in `.pygubu-workflow.json`:

```json
{
  "theme": {
    "name": "modern-dark",
    "applied": "2024-01-15T10:30:00",
    "custom": false
  }
}
```

---

## API Usage

### Python API

```python
from pygubuai.theme_advanced import (
    list_presets,
    apply_preset,
    create_custom_theme,
    export_theme,
    import_theme
)

# List presets
presets = list_presets()

# Apply preset
apply_preset("myapp", "modern-dark")

# Create custom
theme = create_custom_theme(
    name="my-theme",
    base="clam",
    colors={"bg": "#1e1e1e", "fg": "#ffffff"}
)

# Export
export_theme("my-theme", "theme.json")

# Import
import_theme("theme.json")
```

---

## Technical Details

### Implementation

- **Module:** `src/pygubuai/theme_advanced.py`
- **Storage:** `~/.pygubuai/themes/`
- **Format:** JSON
- **Base:** Extends existing `theme.py`

### Color Application

1. Parse `.ui` XML file
2. Find all widget objects
3. Apply color properties based on widget type
4. Update ttk style configuration
5. Save modified XML

### Widget Support

- ✅ ttk.Button
- ✅ ttk.Entry
- ✅ ttk.Label
- ✅ ttk.Frame
- ✅ ttk.Combobox
- ✅ ttk.Checkbutton
- ✅ ttk.Radiobutton
- ✅ ttk.Treeview
- ✅ tk.Text
- ✅ tk.Canvas

---

## Accessibility

### High Contrast Mode

```bash
pygubu-theme apply myapp high-contrast
```

**Features:**
- WCAG AAA contrast ratios (7:1+)
- Clear focus indicators
- No color-only information
- Large touch targets

### Validation

```bash
# Check accessibility
pygubu-theme validate myapp --accessibility
```

**Checks:**
- Contrast ratios
- Font sizes
- Color blindness simulation
- Keyboard navigation

---

## Best Practices

1. **Test themes before applying:**
   ```bash
   pygubu-theme preview myapp <theme>
   ```

2. **Backup before batch operations:**
   ```bash
   pygubu-batch backup
   pygubu-theme apply-all <theme>
   ```

3. **Use semantic colors:**
   - Don't hardcode colors in code
   - Use theme variables
   - Support theme switching

4. **Consider accessibility:**
   - Test with high-contrast
   - Check color blindness
   - Validate contrast ratios

5. **Version control themes:**
   ```bash
   git add ~/.pygubuai/themes/
   ```

---

## Troubleshooting

### Theme not applying?

```bash
# Check current theme
pygubu-theme current myapp

# Validate UI file
pygubu-validate myapp

# Reapply with force
pygubu-theme apply myapp <theme> --force
```

### Colors look wrong?

```bash
# Check ttk theme compatibility
pygubu-theme info <theme>

# Try different base theme
pygubu-theme create new-theme --base alt
```

### Preview crashes?

```bash
# Use safe mode
pygubu-theme preview myapp <theme> --safe

# Check logs
cat ~/.pygubuai/logs/theme.log
```

---

## Roadmap

### v0.6.0 (Current)
- ✅ 8 professional presets
- ✅ Custom theme builder
- ✅ Import/export
- ✅ Preview mode

### v0.7.0 (Future)
- [ ] GUI theme editor
- [ ] Live color picker
- [ ] Theme marketplace
- [ ] Gradient support
- [ ] Animation themes
- [ ] Dark mode auto-switch

---

## Community Themes

Share your themes at: https://github.com/Teycir/PygubuAI/discussions/themes

### Popular Community Themes

- **cyberpunk** - Neon colors and dark backgrounds
- **forest** - Nature-inspired greens and browns
- **ocean** - Blue gradient theme
- **sunset** - Warm orange and purple tones

---

## Contributing

Create and share themes:

1. Create theme: `pygubu-theme create my-theme`
2. Export: `pygubu-theme export my-theme --output my-theme.json`
3. Share on GitHub Discussions
4. Submit PR to include in presets

---

## License

MIT License - Same as PygubuAI

---

**Transform your Tkinter apps with professional themes! 🎨**
