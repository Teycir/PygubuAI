# Implementation Plan - PygubuAI v0.6.0

## Feature: Advanced Theming System

### Overview
Extend basic theme support with professional presets, custom theme builder, and visual management.

---

## Phase 1: Core Theme Engine (Day 1-2)

### 1.1 Theme Data Structures

**File:** `src/pygubuai/theme_presets.py`

```python
THEME_PRESETS = {
    "modern-dark": {
        "name": "Modern Dark",
        "description": "Dark mode with blue accents",
        "base": "clam",
        "colors": {
            "bg": "#2b2b2b",
            "fg": "#ffffff",
            "accent": "#0078d4",
            "button_bg": "#0e639c",
            "button_fg": "#ffffff",
            "entry_bg": "#3c3c3c",
            "entry_fg": "#ffffff",
            "select_bg": "#0078d4",
            "select_fg": "#ffffff",
            "disabled_fg": "#808080"
        }
    },
    # ... 7 more presets
}
```

**Tests:** `tests/test_theme_presets.py`
- Validate all preset structures
- Check color format (#hex)
- Verify base theme exists

---

### 1.2 Color Application Engine

**File:** `src/pygubuai/theme_advanced.py`

```python
def apply_preset(project_name: str, preset_name: str, backup: bool = True) -> bool:
    """Apply theme preset to project"""
    # 1. Load preset
    # 2. Parse UI file
    # 3. Apply colors to widgets
    # 4. Update ttk theme
    # 5. Save changes
    
def apply_colors_to_widget(widget_element, colors: dict, widget_type: str):
    """Apply colors based on widget type"""
    # Map colors to widget properties
    
def update_ttk_theme(ui_root, base_theme: str):
    """Update ttk theme setting"""
```

**Tests:** `tests/test_theme_advanced.py`
- Test preset application
- Test color mapping
- Test XML modification
- Test backup creation

---

## Phase 2: CLI Commands (Day 2-3)

### 2.1 List Command

**Extend:** `src/pygubuai/theme.py`

```python
def list_themes(show_presets: bool = True):
    """List basic themes and presets"""
    
def show_theme_info(theme_name: str):
    """Show detailed theme information"""
```

**CLI:**
```bash
pygubu-theme list [--presets]
pygubu-theme info <theme>
```

---

### 2.2 Apply Command

**Extend:** `src/pygubuai/theme.py`

```python
def apply_theme_or_preset(project: str, theme: str):
    """Apply basic theme or preset"""
    if theme in AVAILABLE_THEMES:
        # Basic theme
    elif theme in THEME_PRESETS:
        # Preset
```

**CLI:**
```bash
pygubu-theme apply <project> <preset>
```

---

### 2.3 Preview Command

**New:** `src/pygubuai/theme_preview.py`

```python
def preview_theme(project: str, theme: str, watch: bool = False):
    """Preview theme without saving"""
    # 1. Create temp copy of UI
    # 2. Apply theme to temp
    # 3. Open preview window
    # 4. Optional: watch for changes
```

**CLI:**
```bash
pygubu-theme preview <project> <preset> [--watch]
```

**Tests:** `tests/test_theme_preview.py`

---

## Phase 3: Custom Theme Builder (Day 3-4)

### 3.1 Theme Creation

**New:** `src/pygubuai/theme_builder.py`

```python
def create_custom_theme(name: str, base: str = None, interactive: bool = True):
    """Create custom theme"""
    if interactive:
        # Prompt for colors
        colors = prompt_for_colors(base)
    return save_theme(name, colors)
    
def prompt_for_colors(base_theme: str = None) -> dict:
    """Interactive color selection"""
    
def validate_theme(theme_data: dict) -> bool:
    """Validate theme structure"""
```

**CLI:**
```bash
pygubu-theme create <name> [--base <theme>] [--from <file>]
```

**Tests:** `tests/test_theme_builder.py`

---

### 3.2 Theme Storage

**Directory:** `~/.pygubuai/themes/`

**Format:**
```json
{
  "name": "my-theme",
  "description": "My custom theme",
  "base": "clam",
  "colors": {...},
  "created": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

**Functions:**
```python
def save_theme(name: str, theme_data: dict):
    """Save theme to user directory"""
    
def load_theme(name: str) -> dict:
    """Load theme from user directory"""
    
def list_custom_themes() -> list:
    """List all custom themes"""
```

---

## Phase 4: Import/Export (Day 4)

### 4.1 Export

**File:** `src/pygubuai/theme_builder.py`

```python
def export_theme(name: str, output_path: str = None, clipboard: bool = False):
    """Export theme to file or clipboard"""
    theme = load_theme(name)
    if clipboard:
        copy_to_clipboard(json.dumps(theme))
    else:
        save_to_file(theme, output_path)
```

**CLI:**
```bash
pygubu-theme export <name> [--output <file>] [--clipboard]
```

---

### 4.2 Import

**File:** `src/pygubuai/theme_builder.py`

```python
def import_theme(source: str):
    """Import theme from file or URL"""
    if source.startswith('http'):
        theme_data = download_theme(source)
    elif source.startswith('gist:'):
        theme_data = download_from_gist(source)
    else:
        theme_data = load_from_file(source)
    
    validate_theme(theme_data)
    save_theme(theme_data['name'], theme_data)
```

**CLI:**
```bash
pygubu-theme import <source>
```

**Tests:** `tests/test_theme_import_export.py`

---

## Phase 5: Integration (Day 5)

### 5.1 Batch Operations

**Extend:** `src/pygubuai/batch.py`

```python
def batch_apply_theme(preset: str, projects: list = None, dry_run: bool = False):
    """Apply theme to multiple projects"""
    if projects is None:
        projects = registry.list_projects()
    
    for project in projects:
        if dry_run:
            print(f"Would apply {preset} to {project}")
        else:
            apply_preset(project, preset)
```

**CLI:**
```bash
pygubu-theme apply-all <preset> [--projects <list>] [--dry-run]
```

---

### 5.2 Current Theme

**Extend:** `src/pygubuai/theme.py`

```python
def get_current_theme_info(project: str, verbose: bool = False):
    """Get current theme with details"""
    theme = get_current_theme(project)
    if verbose:
        # Show colors, modified date, etc.
    return theme
```

**CLI:**
```bash
pygubu-theme current <project> [--verbose]
```

---

### 5.3 Workflow Integration

**Extend:** `src/pygubuai/workflow.py`

Store theme info in `.pygubu-workflow.json`:

```json
{
  "theme": {
    "name": "modern-dark",
    "type": "preset",
    "applied": "2024-01-15T10:30:00"
  }
}
```

---

## File Structure

```
src/pygubuai/
├── theme.py              # Existing basic theme (extend)
├── theme_advanced.py     # NEW: Advanced theme engine
├── theme_presets.py      # NEW: Preset definitions
├── theme_builder.py      # NEW: Custom theme builder
├── theme_preview.py      # NEW: Preview functionality
└── batch.py              # Extend for theme operations

tests/
├── test_theme.py         # Existing (extend)
├── test_theme_advanced.py      # NEW
├── test_theme_presets.py       # NEW
├── test_theme_builder.py       # NEW
├── test_theme_preview.py       # NEW
└── test_theme_import_export.py # NEW

~/.pygubuai/
└── themes/               # NEW: User themes directory
    ├── my-theme.json
    └── company-brand.json
```

---

## Entry Points

**Update:** `pyproject.toml`

```toml
[project.scripts]
# Existing theme command (extend functionality)
pygubu-theme = "pygubuai.theme:main"
```

No new entry points needed - extend existing `pygubu-theme` command.

---

## Testing Strategy

### Unit Tests (90%+ coverage)

1. **test_theme_presets.py**
   - Validate all 8 presets
   - Check color formats
   - Verify base themes

2. **test_theme_advanced.py**
   - Test preset application
   - Test color mapping
   - Test XML modification
   - Test backup creation

3. **test_theme_builder.py**
   - Test theme creation
   - Test validation
   - Test storage

4. **test_theme_preview.py**
   - Test preview mode
   - Test watch mode
   - Test temp file handling

5. **test_theme_import_export.py**
   - Test export to file
   - Test import from file
   - Test JSON validation

### Integration Tests

```python
def test_full_theme_workflow():
    # Create project
    # Apply preset
    # Preview
    # Create custom
    # Export
    # Import
    # Apply custom
```

### Manual Testing

- Visual verification of all presets
- Test on different platforms (Linux, macOS, Windows)
- Test with pygubu-designer
- Test accessibility

---

## Documentation

### Update Files

1. **README.md**
   - Add theme presets to features
   - Update commands table

2. **USER_GUIDE.md**
   - Add theming section
   - Examples for each preset

3. **THEMING_SYSTEM.md** (NEW)
   - Complete theming guide
   - All presets documented
   - Custom theme tutorial

4. **CHANGELOG.md**
   - Document v0.6.0 changes

5. **FEATURE_SHOWCASE.md**
   - Add theming examples
   - Screenshots of presets

---

## Implementation Checklist

### Day 1: Core Engine
- [ ] Create `theme_presets.py` with 8 presets
- [ ] Create `theme_advanced.py` with apply logic
- [ ] Write unit tests for presets
- [ ] Write unit tests for application

### Day 2: CLI Commands
- [ ] Extend `theme.py` with list/info
- [ ] Add apply preset logic
- [ ] Create `theme_preview.py`
- [ ] Write CLI tests

### Day 3: Custom Builder
- [ ] Create `theme_builder.py`
- [ ] Implement interactive creation
- [ ] Implement theme storage
- [ ] Write builder tests

### Day 4: Import/Export
- [ ] Implement export functionality
- [ ] Implement import functionality
- [ ] Add URL/gist support
- [ ] Write import/export tests

### Day 5: Integration
- [ ] Extend batch operations
- [ ] Add current theme info
- [ ] Update workflow tracking
- [ ] Write integration tests

### Day 6: Documentation
- [ ] Create THEMING_SYSTEM.md
- [ ] Update README.md
- [ ] Update USER_GUIDE.md
- [ ] Update CHANGELOG.md

### Day 7: Testing & Polish
- [ ] Manual testing all presets
- [ ] Cross-platform testing
- [ ] Accessibility validation
- [ ] Performance optimization

---

## Success Metrics

- ✅ 8 professional presets implemented
- ✅ Custom theme creation working
- ✅ Import/export functional
- ✅ Preview mode operational
- ✅ 90%+ test coverage
- ✅ Zero breaking changes
- ✅ Documentation complete

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Color application breaks layouts | Extensive testing, backup before apply |
| Preview crashes on complex UIs | Error handling, safe mode |
| Theme files corrupt | Validation on import, backup |
| Performance issues | Cache parsed themes, lazy loading |

---

## Dependencies

**No new external dependencies!**

Uses existing:
- Python 3.9+ stdlib
- xml.etree.ElementTree (existing)
- json (existing)
- pathlib (existing)

Optional (for future):
- requests (for URL import)
- pyperclip (for clipboard)

---

## Version Target

**Release:** v0.6.0  
**Effort:** 7 days  
**Breaking Changes:** None  
**New Commands:** 0 (extends existing)  
**New Modules:** 4

---

## Future Enhancements (v0.7.0+)

- GUI theme editor with color picker
- Live preview in pygubu-designer
- Theme marketplace/gallery
- Gradient and image backgrounds
- Animation themes
- Auto dark mode switching
- Theme inheritance
- CSS-like theme syntax

---

**Ready to implement! 🎨**
