# Critical Bug Fixes - v0.4.0

## Summary
This document tracks the critical bugs identified in the architectural review and their fixes.

## Fixed Issues

### 1. Version Inconsistency ✅
**Issue**: Version mismatch between code (0.3.0) and documentation (0.4.0)

**Files Changed**:
- `pyproject.toml`: Updated version from 0.3.0 → 0.4.0
- `src/pygubuai/__init__.py`: Updated version from 0.3.0 → 0.4.0

**Impact**: Ensures version consistency across the project

---

### 2. Template Creation Bug ✅
**Issue**: Template creation in `create.py` was never invoked (lines 44-47)

**File**: `src/pygubuai/create.py`

**Before**:
```python
if template:
    from .template import create_from_template
    # Template function creates files, just return after
    return  # This never executes due to missing call
```

**After**:
```python
if template:
    from .template import create_from_template
    create_from_template(name, template, dry_run=dry_run, init_git=init_git)
    return
```

**Impact**: Template-based project creation now works correctly

---

### 3. Missing Exception Classes ✅
**Issue**: `register.py` imported non-existent exception classes

**File**: `src/pygubuai/errors.py`

**Added**:
- Proper constructor for `ProjectNotFoundError(project_name, suggestion)`
- Proper constructor for `InvalidProjectError(path, reason)`

**Impact**: Eliminates import errors and provides better error messages

---

### 4. Path Resolution Bug ✅
**Issue**: `resolve()` called before checking if path exists

**File**: `src/pygubuai/register.py`

**Before**:
```python
project_path = pathlib.Path(path).resolve()
if not project_path.exists():
    raise InvalidProjectError(str(path), "path does not exist")
```

**After**:
```python
project_path = pathlib.Path(path)
if not project_path.exists():
    raise InvalidProjectError(str(path), "path does not exist")
project_path = project_path.resolve()
```

**Impact**: Prevents exceptions when resolving invalid paths

---

### 5. Workflow Changes Array Growth ✅
**Issue**: Changes array could grow beyond 100 entries during a session

**File**: `src/pygubuai/workflow.py`

**Added**: Trim changes array before appending new entries:
```python
# Trim changes array before appending to prevent unbounded growth
if len(workflow["changes"]) >= 100:
    workflow["changes"] = workflow["changes"][-99:]
workflow["changes"].append({...})
```

**Impact**: Prevents memory issues during long watch sessions

---

### 6. Number Game UI State Bug ✅
**Issue**: After winning, guess button remained active causing misleading error messages

**File**: `examples/number_game/number_game.py`

**Changes**:
1. Added guard in `on_guess()` to prevent processing after win
2. Disabled guess button when player wins
3. Re-enabled guess button in `on_reset()`

**Impact**: Prevents confusing error messages after game completion

---

## Remaining Issues (Not Fixed)

### Low Priority
1. **Dual Installation Methods**: Shell script installation still exists alongside pip
   - Recommendation: Phase out in v0.5.0
   
2. **Registry Backward Compatibility**: Old string-format entries still supported
   - Recommendation: Add migration tool in v0.5.0

3. **Mixed Logging Patterns**: Some modules use `basicConfig()` directly
   - Recommendation: Centralize logging configuration

4. **Type Hints**: Many functions lack complete type annotations
   - Recommendation: Gradual improvement with mypy enforcement

### Security Considerations
1. **Path Traversal**: File operations don't validate paths against allowed directories
   - Recommendation: Add path validation utilities

2. **Template Loading**: User templates loaded without validation
   - Recommendation: Add template schema validation

### Performance Optimizations
1. **Registry Caching**: Every operation involves file I/O
   - Recommendation: Add in-memory cache with periodic sync

2. **Template Discovery**: Scans directories repeatedly
   - Recommendation: Cache template metadata

---

## Testing Recommendations

### High Priority
- [ ] Test template creation with all available templates
- [ ] Test concurrent registry access (thread-safety)
- [ ] Test path resolution with invalid/non-existent paths
- [ ] Test workflow watching with rapid UI changes

### Medium Priority
- [ ] Test CLI wrapper scripts execution
- [ ] Test dual installation methods
- [ ] Test error message formatting consistency

---

## Version 0.4.0 Release Notes

### Bug Fixes
- Fixed template creation not being invoked
- Fixed missing exception class constructors
- Fixed path resolution order causing exceptions
- Fixed unbounded growth of workflow changes array
- Updated version consistency across project

### Known Limitations
- Dual installation methods still supported (will be deprecated in v0.5.0)
- Registry backward compatibility adds complexity
- No path traversal validation (security consideration)

---

**Date**: 2024
**Reviewer**: Architectural Code Review
**Status**: Critical bugs fixed, ready for v0.4.0 release
