# Testing Quick Reference

## Quick Commands

```bash
# Fast feedback (< 1 min)
make test-fast

# Before commit
make test-coverage

# Full suite
make test

# Specific categories
make test-unit
make test-integration
make test-security
```

## Test Markers

```python
@pytest.mark.unit          # Fast, isolated unit tests
@pytest.mark.integration   # Multi-component tests
@pytest.mark.slow          # Tests taking >1s
@pytest.mark.security      # Security-critical tests
@pytest.mark.performance   # Performance benchmarks
@pytest.mark.cli           # CLI integration tests
```

## Writing Tests

### Use Shared Fixtures

```python
def test_my_feature(temp_project, ui_file):
    """Test description."""
    # Fixtures ready to use!
    assert ui_file.exists()
```

### Available Fixtures

- `temp_project` - Temporary project directory
- `temp_registry` - Temporary registry file
- `mock_registry` - Mocked Registry instance
- `ui_file` - Test UI file
- `workflow_file` - Test workflow file

### Documentation Format

```python
@pytest.mark.unit
def test_feature_name(temp_project):
    """
    Brief one-line description.
    
    Given: Initial state/setup
    When: Action performed
    Then: Expected result
    And: Additional expectations
    """
    # Given: Setup code
    data = setup_data()
    
    # When: Action
    result = perform_action(data)
    
    # Then: Assertions
    assert result == expected
```

## Running Tests

### By Category
```bash
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests
pytest -m security          # Security tests
pytest -m "not slow"        # Skip slow tests
```

### By File
```bash
pytest tests/test_workflow.py
pytest tests/test_workflow_pytest.py -v
```

### With Coverage
```bash
pytest --cov=pygubuai --cov-report=html
# Open htmlcov/index.html
```

### Specific Test
```bash
pytest tests/test_workflow_pytest.py::test_get_file_hash_generates_sha256
```

## CI Pipeline

### Stages
1. **Fast Tests** - Unit tests, fail fast
2. **Full Tests** - All tests + coverage (Python 3.9-3.12)
3. **Security Tests** - Security-critical tests
4. **Integration Tests** - Integration tests

### Local CI Simulation
```bash
# Stage 1: Fast tests
pytest -m "unit and not slow" --maxfail=3

# Stage 2: Full tests
pytest --cov=pygubuai --cov-report=xml

# Stage 3: Security
pytest -m security

# Stage 4: Integration
pytest -m integration
```

## Common Patterns

### Testing File Operations
```python
def test_file_operation(temp_project):
    file_path = temp_project / "test.txt"
    file_path.write_text("content")
    assert file_path.read_text() == "content"
```

### Testing with Mocks
```python
from unittest.mock import patch, MagicMock

def test_with_mock(mock_registry):
    mock_registry.list_projects.return_value = {'proj': '/path'}
    # Test code using mocked registry
```

### Testing Exceptions
```python
def test_raises_error():
    with pytest.raises(ValueError) as exc_info:
        raise_error()
    assert "expected message" in str(exc_info.value)
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("a", "A"),
    ("b", "B"),
])
def test_multiple_cases(input, expected):
    assert input.upper() == expected
```

## Debugging Tests

### Run with verbose output
```bash
pytest -vv
```

### Show print statements
```bash
pytest -s
```

### Drop into debugger on failure
```bash
pytest --pdb
```

### Run last failed tests
```bash
pytest --lf
```

## Coverage Tips

### View missing lines
```bash
pytest --cov=pygubuai --cov-report=term-missing
```

### Generate HTML report
```bash
make test-coverage
open htmlcov/index.html
```

### Check specific module
```bash
pytest --cov=pygubuai.workflow --cov-report=term-missing
```

## Best Practices

### ✅ DO
- Use shared fixtures from conftest.py
- Add appropriate markers
- Write clear Given-When-Then docs
- Test one thing per test
- Use descriptive test names
- Keep tests fast (<100ms for unit)

### ❌ DON'T
- Don't test implementation details
- Don't use sleep() in tests
- Don't share state between tests
- Don't write tests without markers
- Don't skip documentation

## Migration Guide

### From unittest to pytest

**Before:**
```python
class TestFeature(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def test_something(self):
        self.assertEqual(result, expected)
```

**After:**
```python
@pytest.mark.unit
def test_something(temp_project):
    assert result == expected
```

### Compatibility
- Pytest runs unittest tests ✅
- Both styles work together ✅
- Gradual migration supported ✅

## Troubleshooting

### Tests not found
```bash
# Check test discovery
pytest --collect-only
```

### Import errors
```bash
# Ensure package installed
pip install -e .
```

### Fixture not found
```bash
# Check conftest.py is in tests/
ls tests/conftest.py
```

### Marker warnings
```bash
# Check pytest.ini has marker definitions
cat pytest.ini | grep markers
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [TEST_IMPROVEMENT_PLAN.md](TEST_IMPROVEMENT_PLAN.md) - Full improvement plan
- [TEST_IMPLEMENTATION_SUMMARY.md](TEST_IMPLEMENTATION_SUMMARY.md) - What was implemented
- [tests/conftest.py](tests/conftest.py) - Available fixtures
- [pytest.ini](pytest.ini) - Configuration

---

**Quick Start:**
```bash
pip install -e '.[dev]'  # Install dependencies
make test-fast           # Run fast tests
make test-coverage       # Full coverage report
```
