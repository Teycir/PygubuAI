# Architecture Fixes - v0.4.2

## Summary

Addressed 5 architecture issues identified in code review, implementing immediate fixes and deprecation path for v0.5.0.

## Issues Fixed

### ✅ 1. CLI Test Coverage Gap
**Problem**: No tests for actual CLI script invocation  
**Solution**: Added `tests/test_cli_scripts.py` with subprocess-based tests  
**Impact**: Catches entry point configuration errors

**Tests Added**:
- `test_pygubu_create_version()` - Verify --version flag
- `test_pygubu_create_help()` - Verify --help flag  
- `test_pygubu_register_help()` - Verify register command
- `test_pygubu_template_help()` - Verify template command
- `test_all_entry_points_exist()` - Verify all entry points have modules

### ✅ 2. Module Naming Conflict
**Problem**: `template.py` vs `templates.py` caused confusion  
**Solution**: Renamed `templates.py` → `template_data.py`  
**Impact**: Clear separation of responsibilities

**Module Roles**:
- `template.py` - CLI command handler
- `template_data.py` - Template definitions and data
- `template_discovery.py` - Dynamic template discovery

**Files Updated**:
- `src/pygubuai/templates.py` → `src/pygubuai/template_data.py`
- `src/pygubuai/template.py` - Updated import
- `src/pygubuai/template_discovery.py` - Updated import
- `tests/test_templates.py` - Updated import
- `tests/test_integration.py` - Updated import

### ✅ 3. Legacy Install Deprecation
**Problem**: `install.sh` creates inconsistent environments  
**Solution**: Added deprecation warnings, scheduled removal for v0.5.0  
**Impact**: Single installation path going forward

**Changes**:
- Added interactive warning to `install.sh`
- Updated README.md with deprecation notice
- Updated ARCHITECTURE.md with migration guide

### ✅ 4. Documentation Updates
**Problem**: Architecture docs didn't reflect versioning  
**Solution**: Added version history and deprecation notices  
**Impact**: Clear migration path for users

**Updated**:
- `ARCHITECTURE.md` - Added deprecation section and version history
- `README.md` - Emphasized pip installation, marked install.sh as deprecated
- `ARCHITECTURE_IMPROVEMENTS.md` - Comprehensive improvement plan

### ⏳ 5. Wrapper Script Removal (Planned v0.5.0)
**Problem**: Physical wrapper scripts can diverge from pyproject.toml  
**Solution**: Will remove in v0.5.0, use pip-generated scripts only  
**Impact**: Eliminates 5 files, reduces maintenance

**Current State**: Deprecated, scheduled for removal
**Migration**: Users should use `pip install -e .`

## Test Results

```bash
# New CLI tests
$ python3 -m unittest tests.test_cli_scripts -v
test_all_entry_points_exist ... ok
test_pygubu_create_help ... ok
test_pygubu_create_version ... ok
test_pygubu_register_help ... ok
test_pygubu_template_help ... ok

Ran 5 tests in 0.068s - OK

# Template tests (after rename)
$ python3 -m unittest tests.test_templates -v
Ran 11 tests in 0.000s - OK
```

## Migration Guide

### For Users

**Before (Deprecated)**:
```bash
./install.sh
```

**After (Recommended)**:
```bash
pip install -e .
```

### For Developers

**Adding New Command**:

**Before (3 steps)**:
1. Create `src/pygubuai/newcmd.py`
2. Add to `pyproject.toml`
3. Create wrapper script `pygubu-newcmd`

**After (2 steps)**:
1. Create `src/pygubuai/newcmd.py` with `main()` function
2. Add to `pyproject.toml`:
   ```toml
   [project.scripts]
   pygubu-newcmd = "pygubuai.newcmd:main"
   ```

## Files Changed

### Added
- `tests/test_cli_scripts.py` - CLI invocation tests
- `ARCHITECTURE_IMPROVEMENTS.md` - Improvement plan
- `ARCHITECTURE_FIXES_v0.4.2.md` - This file

### Modified
- `src/pygubuai/templates.py` → `src/pygubuai/template_data.py` (renamed)
- `src/pygubuai/template.py` - Updated import
- `src/pygubuai/template_discovery.py` - Updated import
- `tests/test_templates.py` - Updated import
- `tests/test_integration.py` - Updated import
- `install.sh` - Added deprecation warning
- `README.md` - Emphasized pip, deprecated install.sh
- `ARCHITECTURE.md` - Added deprecation notices and version history

### To Be Removed (v0.5.0)
- `pygubu-create` (wrapper script)
- `pygubu-register` (wrapper script)
- `pygubu-template` (wrapper script)
- `pygubu-ai-workflow` (wrapper script)
- `tkinter-to-pygubu` (wrapper script)
- `install.sh`
- `uninstall.sh`

## Benefits

1. **Better Testing**: CLI scripts tested via subprocess
2. **Clearer Naming**: No module confusion
3. **Single Install Method**: Reduces support burden
4. **Standard Practice**: Follows Python packaging conventions
5. **Reduced Maintenance**: Fewer files to maintain

## Backward Compatibility

- **v0.4.2**: Both methods work, deprecation warnings shown
- **v0.5.0**: pip-only, wrapper scripts removed

## Next Steps

For v0.5.0:
1. Remove physical wrapper scripts
2. Remove `install.sh` and `uninstall.sh`
3. Update all documentation
4. Add migration guide in CHANGELOG

## Verification

All tests pass:
- ✅ CLI script invocation tests (5/5)
- ✅ Template tests after rename (11/11)
- ✅ Integration tests (all passing)
- ✅ Entry points verified

## Conclusion

Architecture is now cleaner, better tested, and has a clear deprecation path. The changes are minimal, backward compatible, and set up a smooth transition to v0.5.0.
