# Test Suite Improvement Plan

## Executive Summary

**Current Status:** Grade A- (Excellent coverage, room for improvement)
- 38 test files with comprehensive coverage
- Strong security and performance testing
- Well-structured with proper mocking
- 92%+ code coverage

**Key Improvements Needed:**
1. Test organization and maintainability
2. Enhanced documentation
3. Pytest migration for better fixtures
4. Expanded CLI integration testing

---

## 1. Test Organization Refactoring

### Problem
Large test classes (e.g., `TestWorkflow` 300+ lines) reduce maintainability.

### Solution
Split into focused test modules:

```
tests/
├── unit/
│   ├── test_workflow_core.py       # Basic workflow operations
│   ├── test_workflow_security.py   # Security validations
│   ├── test_workflow_recovery.py   # Error recovery
│   └── test_workflow_tracking.py   # File tracking
├── integration/
│   ├── test_cli_workflows.py       # End-to-end CLI tests
│   └── test_feature_integration.py # Cross-feature tests
└── performance/
    └── test_benchmarks.py          # Performance tests
```

**Implementation:**
```bash
# Create new structure
mkdir -p tests/{unit,integration,performance}

# Split test_workflow.py
pygubu-test-split tests/test_workflow.py \
  --output tests/unit/ \
  --by-class
```

**Effort:** 4 hours  
**Impact:** High (better maintainability)

---

## 2. Enhanced Test Documentation

### Problem
Minimal docstrings make test intent unclear.

### Solution
Add comprehensive docstrings with Given-When-Then format:

**Before:**
```python
def test_get_file_hash(self):
    """Test file hash generation with SHA256"""
    test_file = self.project_dir / "test.ui"
    test_file.write_text("<ui>test</ui>")
    hash1 = get_file_hash(test_file)
    self.assertEqual(len(hash1), 64)
```

**After:**
```python
def test_get_file_hash(self):
    """
    Test file hash generation produces consistent SHA256 hashes.
    
    Given: A UI file with specific content
    When: get_file_hash() is called
    Then: Returns 64-character SHA256 hash
    And: Same content produces same hash
    And: Different content produces different hash
    """
    # Given: A UI file with specific content
    test_file = self.project_dir / "test.ui"
    test_file.write_text("<ui>test</ui>")
    
    # When: get_file_hash() is called
    hash1 = get_file_hash(test_file)
    
    # Then: Returns 64-character SHA256 hash
    self.assertEqual(len(hash1), 64)
    
    # And: Same content produces same hash
    hash2 = get_file_hash(test_file)
    self.assertEqual(hash1, hash2)
```

**Effort:** 6 hours (38 files × 10 min avg)  
**Impact:** Medium (better understanding)

---

## 3. Pytest Migration

### Problem
unittest requires verbose setup/teardown, lacks powerful fixtures.

### Solution
Migrate to pytest with shared fixtures:

**Create `tests/conftest.py`:**
```python
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_project():
    """Temporary project directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "testproj"
        project_dir.mkdir()
        yield project_dir

@pytest.fixture
def mock_registry(temp_project):
    """Mock registry with test project."""
    from unittest.mock import MagicMock, patch
    with patch('pygubuai.workflow.Registry') as MockRegistry:
        mock_instance = MagicMock()
        mock_instance.list_projects.return_value = {
            'test': str(temp_project)
        }
        MockRegistry.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def ui_file(temp_project):
    """Create test UI file."""
    ui_file = temp_project / "test.ui"
    ui_file.write_text("<interface></interface>")
    return ui_file
```

**Migrate test:**
```python
# Before (unittest)
class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = pathlib.Path(self.temp_dir) / "testproj"
        self.project_dir.mkdir()
    
    def test_load_workflow_new(self):
        workflow = load_workflow(self.project_dir)
        self.assertIsNone(workflow["ui_hash"])

# After (pytest)
def test_load_workflow_new(temp_project):
    """Test loading workflow for new project returns defaults."""
    workflow = load_workflow(temp_project)
    assert workflow["ui_hash"] is None
    assert workflow["changes"] == []
```

**Benefits:**
- 50% less boilerplate code
- Reusable fixtures across tests
- Better parametrization support
- Cleaner assertions

**Effort:** 12 hours  
**Impact:** High (code quality + maintainability)

---

## 4. Test Categorization

### Problem
No separation between fast/slow, unit/integration tests.

### Solution
Add pytest markers:

```python
# tests/conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests (>1s)")
    config.addinivalue_line("markers", "security: Security-critical tests")

# Usage in tests
@pytest.mark.unit
@pytest.mark.fast
def test_get_file_hash(temp_project):
    """Fast unit test."""
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_complete_workflow(temp_project):
    """Slow integration test."""
    pass
```

**Run specific categories:**
```bash
pytest -m unit              # Only unit tests
pytest -m "not slow"        # Skip slow tests
pytest -m security          # Security tests only
```

**Effort:** 2 hours  
**Impact:** Medium (better CI/CD)

---

## 5. Property-Based Testing

### Problem
Limited edge case coverage for validation functions.

### Solution
Add hypothesis for property-based testing:

```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=1000))
def test_validate_path_handles_any_string(path_string):
    """
    Property: validate_path should never crash on any string input.
    
    Given: Any random string
    When: validate_path() is called
    Then: Either returns Path or raises ValueError (never crashes)
    """
    from pygubuai.utils import validate_path
    try:
        result = validate_path(path_string, must_exist=False)
        assert isinstance(result, Path)
    except ValueError:
        pass  # Expected for invalid paths

@given(
    st.text(min_size=1, max_size=100),
    st.text(min_size=1, max_size=100)
)
def test_registry_project_names_are_unique(name1, name2):
    """
    Property: Registry should maintain unique project names.
    
    Given: Two different project names
    When: Both are added to registry
    Then: Both exist independently
    """
    registry = Registry()
    registry.add_project(name1, f"/tmp/{name1}")
    registry.add_project(name2, f"/tmp/{name2}")
    
    projects = registry.list_projects()
    if name1 != name2:
        assert name1 in projects
        assert name2 in projects
```

**Effort:** 8 hours  
**Impact:** High (better edge case coverage)

---

## 6. CLI Integration Testing

### Problem
Limited end-to-end CLI testing.

### Solution
Add comprehensive CLI workflow tests:

```python
# tests/integration/test_cli_complete_workflows.py
import subprocess
import pytest

def run_cli(command):
    """Helper to run CLI commands."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def test_complete_app_creation_workflow(tmp_path):
    """
    Test complete workflow: create → theme → db → export.
    
    Scenario: User creates a complete CRUD app from scratch
    """
    os.chdir(tmp_path)
    
    # Step 1: Create project
    code, out, err = run_cli("pygubu-create myapp 'user management'")
    assert code == 0
    assert (tmp_path / "myapp" / "myapp.ui").exists()
    
    # Step 2: Apply theme
    code, out, err = run_cli("pygubu-theme apply myapp modern-dark")
    assert code == 0
    assert "Theme applied" in out
    
    # Step 3: Initialize database
    code, out, err = run_cli("pygubu-db init myapp --type sqlite")
    assert code == 0
    assert (tmp_path / "myapp" / "database.py").exists()
    
    # Step 4: Add table
    code, out, err = run_cli(
        "pygubu-db add-table myapp users name:str email:str"
    )
    assert code == 0
    
    # Step 5: Add export
    code, out, err = run_cli("pygubu-data-export add myapp --format csv")
    assert code == 0
    
    # Step 6: Validate
    code, out, err = run_cli("pygubu-validate myapp")
    assert code == 0
    assert "No issues found" in out

@pytest.mark.parametrize("template", ["login", "crud", "settings"])
def test_all_templates_work(tmp_path, template):
    """Test all templates create valid projects."""
    os.chdir(tmp_path)
    code, out, err = run_cli(f"pygubu-template myapp {template}")
    assert code == 0
    assert (tmp_path / "myapp" / "myapp.ui").exists()
```

**Effort:** 6 hours  
**Impact:** High (catches integration bugs)

---

## 7. Performance Benchmarking

### Problem
No baseline performance metrics or regression detection.

### Solution
Add pytest-benchmark tests:

```python
# tests/performance/test_benchmarks.py
import pytest

def test_registry_read_performance(benchmark, temp_registry):
    """Benchmark registry read operations."""
    registry = Registry()
    for i in range(100):
        registry.add_project(f"proj{i}", f"/tmp/proj{i}")
    
    result = benchmark(registry.list_projects)
    assert len(result) == 100

def test_file_hash_performance(benchmark, ui_file):
    """Benchmark file hashing."""
    result = benchmark(get_file_hash, ui_file)
    assert len(result) == 64

def test_workflow_save_performance(benchmark, temp_project):
    """Benchmark workflow save operations."""
    workflow = {"file_hashes": {}, "changes": []}
    benchmark(save_workflow, temp_project, workflow)
```

**Run benchmarks:**
```bash
pytest tests/performance/ --benchmark-only
pytest tests/performance/ --benchmark-compare
```

**Effort:** 4 hours  
**Impact:** Medium (performance regression detection)

---

## 8. Coverage Improvements

### Current Gaps
- CLI script entry points: ~60% coverage
- Error handling edge cases: ~75% coverage
- Interactive prompts: ~50% coverage

### Solution

**CLI Entry Points:**
```python
# tests/unit/test_cli_entry_points.py
def test_pygubu_create_entry_point():
    """Test pygubu-create CLI entry point."""
    from pygubuai.cli.create import main
    with patch('sys.argv', ['pygubu-create', '--version']):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0

def test_pygubu_create_handles_keyboard_interrupt():
    """Test graceful handling of Ctrl+C."""
    from pygubuai.cli.create import main
    with patch('sys.argv', ['pygubu-create', 'test', 'desc']):
        with patch('pygubuai.create.create_project', 
                   side_effect=KeyboardInterrupt):
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 130
```

**Interactive Prompts:**
```python
# tests/unit/test_interactive_prompts.py
def test_confirm_prompt_yes(monkeypatch):
    """Test confirmation prompt accepts 'yes'."""
    monkeypatch.setattr('builtins.input', lambda _: 'yes')
    from pygubuai.interactive import confirm
    assert confirm("Continue?") is True

def test_confirm_prompt_no(monkeypatch):
    """Test confirmation prompt rejects 'no'."""
    monkeypatch.setattr('builtins.input', lambda _: 'no')
    from pygubuai.interactive import confirm
    assert confirm("Continue?") is False
```

**Effort:** 6 hours  
**Impact:** High (95%+ coverage target)

---

## 9. Mutation Testing

### Problem
High coverage doesn't guarantee test quality.

### Solution
Add mutation testing with mutmut:

```bash
# Install
pip install mutmut

# Run mutation tests
mutmut run --paths-to-mutate=src/pygubuai

# View results
mutmut results
mutmut show <mutation_id>
```

**Example mutation:**
```python
# Original
if hash1 != hash2:
    return True

# Mutated
if hash1 == hash2:  # Operator changed
    return True

# If tests still pass, they're not thorough enough
```

**Effort:** 8 hours (initial setup + fixing weak tests)  
**Impact:** High (test quality validation)

---

## 10. Continuous Integration Enhancements

### Problem
Single test run doesn't optimize for speed or coverage.

### Solution
Multi-stage CI pipeline:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  fast-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run fast unit tests
        run: pytest -m "unit and not slow" --maxfail=3
  
  full-tests:
    runs-on: ubuntu-latest
    needs: fast-tests
    steps:
      - uses: actions/checkout@v3
      - name: Run all tests with coverage
        run: |
          pytest --cov=pygubuai --cov-report=xml
          codecov
  
  security-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run security tests
        run: pytest -m security
  
  mutation-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3
      - name: Run mutation tests
        run: mutmut run --paths-to-mutate=src/pygubuai
```

**Effort:** 3 hours  
**Impact:** High (faster feedback, better quality gates)

---

## Implementation Roadmap

### Phase 1: Quick Wins (1 week)
1. ✅ Test categorization with markers (2h)
2. ✅ Enhanced docstrings (6h)
3. ✅ CI pipeline improvements (3h)
4. ✅ Coverage gap fixes (6h)

**Total:** 17 hours  
**Impact:** Immediate improvements in test clarity and CI speed

### Phase 2: Foundation (2 weeks)
1. ✅ Pytest migration (12h)
2. ✅ Test organization refactoring (4h)
3. ✅ Shared fixtures (4h)
4. ✅ CLI integration tests (6h)

**Total:** 26 hours  
**Impact:** Better maintainability and test structure

### Phase 3: Advanced (2 weeks)
1. ✅ Property-based testing (8h)
2. ✅ Performance benchmarking (4h)
3. ✅ Mutation testing (8h)

**Total:** 20 hours  
**Impact:** Highest quality test suite

---

## Success Metrics

### Before
- 38 test files
- 92% coverage
- ~5 min test runtime
- unittest framework
- Manual test categorization

### After (Target)
- 50+ test files (better organized)
- 95%+ coverage
- <2 min fast tests, <5 min full suite
- pytest framework
- Automated categorization
- Property-based testing
- Mutation testing score >80%
- Comprehensive CLI integration tests

---

## Maintenance Guidelines

### Adding New Tests
1. Use pytest fixtures from `conftest.py`
2. Add appropriate markers (`@pytest.mark.unit`, etc.)
3. Follow Given-When-Then docstring format
4. Add property-based tests for validation logic
5. Update integration tests for new features

### Test Review Checklist
- [ ] Clear docstring with Given-When-Then
- [ ] Appropriate markers applied
- [ ] Uses shared fixtures
- [ ] Tests one thing clearly
- [ ] Includes edge cases
- [ ] Fast (<100ms for unit tests)

### Running Tests Locally
```bash
# Fast feedback loop
pytest -m "unit and not slow"

# Before commit
pytest -m "not slow" --cov=pygubuai

# Full suite
pytest --cov=pygubuai --cov-report=html

# Specific category
pytest -m security
pytest -m integration
```

---

## Conclusion

The current test suite is excellent (Grade A-) with strong coverage and security focus. These improvements will:

1. **Reduce maintenance burden** through better organization
2. **Improve test quality** with property-based and mutation testing
3. **Speed up development** with faster test feedback
4. **Increase confidence** with comprehensive CLI integration tests
5. **Maintain quality** with automated benchmarking and CI gates

**Recommended Priority:** Phase 1 → Phase 2 → Phase 3

**Total Effort:** ~63 hours (~2 months part-time)  
**ROI:** High - Better maintainability, quality, and developer experience
