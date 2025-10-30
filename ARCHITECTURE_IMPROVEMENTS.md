# Architecture Improvements - v0.4.2

## Issues Identified

### 1. Wrapper Script Duplication Risk ⚠️
**Problem**: Manual wrapper scripts can diverge from `pyproject.toml` entry points.

**Solution**: Remove physical wrapper scripts entirely. Use `pip install -e .` exclusively, which auto-generates scripts from `[project.scripts]`.

**Impact**: Eliminates 5 wrapper files, reduces maintenance overhead.

### 2. Legacy Install Method ⚠️
**Problem**: `install.sh` creates inconsistent environments when mixed with pip.

**Solution**: Deprecate `install.sh` in v0.4.2, remove in v0.5.0.

**Impact**: Single installation path, clearer documentation.

### 3. Entry Point Synchronization ⚠️
**Problem**: Adding commands requires updating 3 places (module, pyproject.toml, wrapper).

**Solution**: With wrapper removal, only 2 places needed (module + pyproject.toml).

**Impact**: 33% reduction in steps to add commands.

### 4. Module Naming Conflict ⚠️
**Problem**: `template.py` vs `templates.py` causes confusion.

**Solution**: 
- `template.py` → CLI command handler (keep)
- `templates.py` → Template data/logic (rename to `template_data.py`)

**Impact**: Clearer module responsibilities.

### 5. CLI Test Coverage Gap ⚠️
**Problem**: No tests for actual CLI script invocation.

**Solution**: Add subprocess-based CLI tests in `test_cli_scripts.py`.

**Impact**: Catches entry point configuration errors.

## Implementation Plan

### Phase 1: Immediate (v0.4.2)
1. ✅ Add CLI script invocation tests
2. ✅ Rename `templates.py` → `template_data.py`
3. ✅ Update ARCHITECTURE.md with deprecation notice
4. ✅ Add migration guide

### Phase 2: Deprecation (v0.4.2)
1. Mark `install.sh` as deprecated
2. Update README to recommend pip only
3. Add deprecation warning to `install.sh`

### Phase 3: Removal (v0.5.0)
1. Remove wrapper scripts
2. Remove `install.sh`
3. Update all documentation

## Benefits

- **Reduced Maintenance**: 5 fewer files to maintain
- **Consistency**: Single installation method
- **Standard Practice**: Follows Python packaging conventions
- **Better Testing**: CLI scripts tested via subprocess
- **Clearer Naming**: No module confusion

## Migration Guide

### For Users

**Old (Deprecated)**:
```bash
./install.sh
```

**New (Recommended)**:
```bash
pip install -e .
```

### For Developers

**Adding New Command (Old)**:
1. Create `src/pygubuai/newcmd.py`
2. Add to `pyproject.toml`
3. Create wrapper script `pygubu-newcmd`
4. Update `install.sh`

**Adding New Command (New)**:
1. Create `src/pygubuai/newcmd.py`
2. Add to `pyproject.toml`:
   ```toml
   pygubu-newcmd = "pygubuai.newcmd:main"
   ```
3. Done! `pip install -e .` handles the rest.

## Backward Compatibility

- v0.4.2: Both methods work, deprecation warnings
- v0.5.0: pip-only, wrapper scripts removed

## Testing Strategy

```python
# New test: test_cli_scripts.py
def test_cli_script_invocation():
    """Test actual CLI script execution"""
    result = subprocess.run(['pygubu-create', '--version'], 
                          capture_output=True)
    assert result.returncode == 0
```

## Documentation Updates

- ✅ ARCHITECTURE.md - Add deprecation notice
- ✅ README.md - Emphasize pip install
- ✅ DEVELOPER_GUIDE.md - Update command addition steps
- ✅ CHANGELOG.md - Document changes

## Version History

- **v0.4.0**: Standardized wrapper architecture
- **v0.4.2**: Deprecate install.sh, add CLI tests, rename templates.py
- **v0.5.0**: Remove wrappers, pip-only installation
