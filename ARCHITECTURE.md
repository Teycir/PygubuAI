# PygubuAI Architecture

## Overview

PygubuAI uses a **modular package architecture** with thin CLI wrappers for all commands.

## Architecture Pattern

### ✅ Correct Pattern: Wrapper Scripts

All CLI scripts follow this pattern:

```python
#!/usr/bin/env python3
"""Command description - wrapper for package module"""
from pygubuai.module import main

if __name__ == '__main__':
    main()
```

### ❌ Deprecated: Standalone Scripts

Standalone implementations with duplicated logic are deprecated and have been removed.

## Directory Structure

```
PygubuAI/
├── src/pygubuai/          # Core package (all logic here)
│   ├── __init__.py
│   ├── create.py          # Project creation
│   ├── register.py        # Project registry
│   ├── template.py        # Template management
│   ├── workflow.py        # Watch mode
│   ├── converter.py       # Tkinter conversion
│   ├── widgets.py         # Widget detection
│   ├── generator.py       # Code generation
│   ├── registry.py        # Registry operations
│   ├── dryrun.py          # Dry-run mode
│   ├── cache.py           # Performance caching
│   ├── accessibility.py   # WCAG helpers
│   └── ...                # Other modules
│
├── pygubu-create          # CLI wrapper → pygubuai.create:main
├── pygubu-register        # CLI wrapper → pygubuai.register:main
├── pygubu-template        # CLI wrapper → pygubuai.template:main
├── pygubu-ai-workflow     # CLI wrapper → pygubuai.workflow:main
├── tkinter-to-pygubu      # CLI wrapper → pygubuai.converter:main
│
├── tests/                 # Test suite
└── pyproject.toml         # Package config with entry points
```

## Entry Points

Defined in `pyproject.toml`:

```toml
[project.scripts]
pygubu-create = "pygubuai.create:main"
pygubu-register = "pygubuai.register:main"
pygubu-template = "pygubuai.template:main"
pygubu-ai-workflow = "pygubuai.workflow:main"
tkinter-to-pygubu = "pygubuai.converter:main"
```

## Installation Methods

### 1. pip install (Recommended)

```bash
pip install -e .
```

This installs the package and creates entry points automatically.

### 2. Shell Script (Legacy)

```bash
./install.sh
```

Copies wrapper scripts to `~/bin/` or `/usr/local/bin/`.

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| `create.py` | Project creation with validation |
| `register.py` | Global project registry |
| `template.py` | Template-based creation (CLI handler) |
| `template_data.py` | Template definitions and data |
| `workflow.py` | Watch mode for UI changes |
| `converter.py` | Tkinter-to-pygubu conversion |
| `widgets.py` | Widget detection from descriptions |
| `generator.py` | UI XML and Python code generation |
| `registry.py` | Registry file operations |
| `dryrun.py` | Preview mode without file changes |
| `cache.py` | Performance optimization |
| `accessibility.py` | WCAG compliance checking |
| `validation.py` | Input validation |
| `errors.py` | Custom exceptions |
| `utils.py` | Shared utilities |

## Import Pattern

All CLI wrappers and internal modules import from `pygubuai.*`:

```python
from pygubuai.widgets import detect_widgets, get_callbacks
from pygubuai.generator import generate_base_ui_xml_structure
from pygubuai.registry import Registry
from pygubuai.dryrun import enable_dryrun
```

## Testing

Tests import from package:

```python
from pygubuai.create import create_project
from pygubuai.widgets import detect_widgets
from pygubuai.cache import get_cached, set_cached
```

Run tests:

```bash
python -m unittest discover tests/
```

## Benefits of This Architecture

1. **Single Source of Truth**: All logic in `src/pygubuai/`
2. **Easy Testing**: Import and test modules directly
3. **No Duplication**: CLI wrappers are 3-line files
4. **Maintainable**: Changes in one place
5. **Standard**: Follows Python packaging best practices
6. **Flexible**: Works with pip or shell install

## Migration Complete

All standalone implementations have been replaced with the wrapper pattern:

- ✅ `pygubu-create` → uses `pygubuai.create`
- ✅ `pygubu-register` → uses `pygubuai.register`
- ✅ `pygubu-template` → uses `pygubuai.template`
- ✅ `pygubu-ai-workflow` → uses `pygubuai.workflow`
- ✅ `tkinter-to-pygubu` → uses `pygubuai.converter`

## Adding New Commands

1. Create module in `src/pygubuai/newfeature.py` with `main()` function
2. Add entry point to `pyproject.toml`:
   ```toml
   pygubu-newfeature = "pygubuai.newfeature:main"
   ```
3. Create wrapper script `pygubu-newfeature`:
   ```python
   #!/usr/bin/env python3
   from pygubuai.newfeature import main
   if __name__ == '__main__': main()
   ```
4. Add to `install.sh` if supporting shell install

## Deprecation Notice (v0.4.2)

### Shell Script Installation (Deprecated)

The `install.sh` method is **deprecated** and will be removed in v0.5.0.

**Use pip installation instead:**
```bash
pip install -e .
```

### Physical Wrapper Scripts (To Be Removed)

Physical wrapper scripts (`pygubu-create`, etc.) will be removed in v0.5.0.
Entry points in `pyproject.toml` will be the sole installation method.

## Module Naming (v0.4.2)

- `template.py` - CLI command handler for template operations
- `template_data.py` - Template definitions and data (renamed from `templates.py`)
- `template_discovery.py` - Dynamic template discovery system

## Version History

- **v0.4.0**: Architecture standardized with wrapper pattern
- **v0.4.2**: Deprecated install.sh, renamed templates.py → template_data.py, added CLI tests
- **v0.5.0**: (Planned) Remove wrapper scripts and install.sh, pip-only installation
