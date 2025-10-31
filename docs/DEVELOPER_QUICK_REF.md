# Developer Quick Reference

## Architecture at a Glance

```
CLI Wrapper (3 lines) → Package Module (full logic) → Shared Utilities
```

## File Locations

- **All Logic**: `src/pygubuai/*.py`
- **CLI Wrappers**: Root directory (`pygubu-*`)
- **Tests**: `tests/test_*.py`
- **Config**: `pyproject.toml`

## Common Tasks

### Add New Command

1. Create `src/pygubuai/myfeature.py`:
```python
def main():
    print("My feature")

if __name__ == '__main__':
    main()
```

2. Add to `pyproject.toml`:
```toml
[project.scripts]
pygubu-myfeature = "pygubuai.myfeature:main"
```

3. Create wrapper `pygubu-myfeature`:
```python
#!/usr/bin/env python3
from pygubuai.myfeature import main
if __name__ == '__main__': main()
```

### Import Pattern

```python
# In package modules
from .widgets import detect_widgets
from .registry import Registry

# In CLI wrappers
from pygubuai.module import main

# In tests
from pygubuai.create import create_project
```

### Run Tests

```bash
export PYTHONPATH=/path/to/PygubuAI/src:$PYTHONPATH
python -m unittest discover tests/
```

### Install for Development

```bash
pip install -e .
```

### Check Imports

```bash
python3 -c "from pygubuai.create import main; print('OK')"
```

## Module Map

| Need to... | Use Module |
|------------|------------|
| Create project | `create.py` |
| Detect widgets | `widgets.py` |
| Generate code | `generator.py` |
| Manage registry | `registry.py` |
| Preview changes | `dryrun.py` |
| Cache data | `cache.py` |
| Check accessibility | `accessibility.py` |
| Validate input | `validation.py` |
| Handle errors | `errors.py` |

## Key Functions

```python
# Project creation
from pygubuai.create import create_project
create_project(name, description, dry_run=False)

# Widget detection
from pygubuai.widgets import detect_widgets, get_callbacks
widgets = detect_widgets("login form")
callbacks = get_callbacks(widgets)

# Registry operations
from pygubuai.registry import Registry
reg = Registry()
reg.add_project(name, path)

# Dry-run mode
from pygubuai.dryrun import enable_dryrun, record_operation
enable_dryrun()
record_operation("CREATE_FILE", "test.py")
```

## Testing Pattern

```python
import unittest
from pygubuai.module import function

class TestFeature(unittest.TestCase):
    def test_something(self):
        result = function()
        self.assertEqual(result, expected)
```

## Debugging

```bash
# Enable debug logging
export PYGUBUAI_LOG_LEVEL=DEBUG

# Check PYTHONPATH
echo $PYTHONPATH

# Verify imports
python3 -c "import sys; print(sys.path)"
```

## Common Errors

### ImportError: No module named 'pygubuai'

**Fix**: Set PYTHONPATH or install package
```bash
export PYTHONPATH=/path/to/PygubuAI/src:$PYTHONPATH
# OR
pip install -e .
```

### ImportError: No module named 'pygubuai_widgets'

**Fix**: This module doesn't exist. Use `from pygubuai.widgets import ...`

## Code Style

- Use type hints where helpful
- Keep CLI wrappers minimal (3 lines)
- Put all logic in package modules
- Write tests for new features
- Follow existing patterns

## Quick Checks

```bash
# Syntax check
python3 -m py_compile src/pygubuai/*.py

# Import check
python3 -c "from pygubuai import *"

# Test one module
python3 -m unittest tests.test_widgets

# Coverage
coverage run -m unittest discover tests/
coverage report
```

## Resources

- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Migration**: [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)
- **User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Full Dev Guide**: [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)
