# Migration Guide - PygubuAI v0.1.0

## Breaking Changes

### Package Structure
- **Old**: Flat structure with `pygubu_create.py` at root
- **New**: Proper package structure in `src/pygubuai/`

### Installation Method (Recommended)
- **Old**: `./install.sh` (copies to ~/bin)
- **New**: `pip install -e .` (proper Python package)

### Import Changes
If you imported modules directly:
```python
# Old
import pygubuai_widgets

# New
from pygubuai import widgets
```

## Migration Steps

### For Users

**Option 1: Use pip (Recommended)**
```bash
# Uninstall old version
./uninstall.sh  # if you used install.sh

# Install new version
pip install -e .

# Verify
pygubu-create --version
```

**Option 2: Keep using install.sh**
```bash
# Still works, but not recommended for development
./install.sh
```

### For Developers

```bash
# Install in development mode with all tools
make dev

# Or manually
pip install -e ".[dev]"

# Run tests
make test

# Run with coverage
make coverage

# Lint code
make lint
```

## What's Fixed

✅ Proper package structure (src layout)  
✅ Error handling and validation  
✅ Input sanitization  
✅ Thread-safe registry with file locking  
✅ Logging framework  
✅ Version management (`--version` flag)  
✅ Uninstall script  
✅ pytest integration  
✅ Coverage reporting  
✅ CI/CD improvements  

## What Still Works

✅ All CLI commands (`pygubu-create`, etc.)  
✅ Project registry (`~/.pygubu-registry.json`)  
✅ AI context files  
✅ Existing projects  
✅ Legacy `install.sh` script  

## Known Issues

⚠️ Only `pygubu-create` migrated to new structure  
⚠️ Other tools (`pygubu-register`, `pygubu-template`, etc.) still use old structure  
⚠️ Tests need updating for new package structure  

## Next Steps

See [TODO.md](TODO.md) for remaining migration tasks.
