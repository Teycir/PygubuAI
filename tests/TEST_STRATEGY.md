# PygubuAI Test Strategy

## Overview

This document describes the comprehensive testing strategy for PygubuAI, focusing on catching regressions in critical components.

## Test Suites

### 1. Security Tests (`test_security_fixes.py`)
**Purpose:** Verify all security vulnerabilities remain fixed  
**Tests:** 16  
**Run Time:** ~0.1s  

**Critical Coverage:**
- Path traversal prevention (CWE-22)
- Command injection prevention (CWE-77/78/88)
- XSS prevention (CWE-79/80)
- Secure hashing (SHA-256 vs MD5)
- Input validation

**When to Run:**
- Before every commit
- In CI/CD pipeline
- After any security-related changes

### 2. Error Handling Tests (`test_error_handling.py`)
**Purpose:** Ensure robust error handling throughout  
**Tests:** 20  
**Run Time:** ~0.02s  

**Critical Coverage:**
- Custom exception types
- Error chaining and causes
- Helpful error messages
- Error recovery mechanisms
- Graceful degradation

**When to Run:**
- Before every commit
- After changes to error handling
- When adding new features

### 3. Critical Regression Tests (`test_critical_regression.py`)
**Purpose:** Catch regressions in core functionality  
**Tests:** 23  
**Run Time:** ~0.13s  

**Critical Coverage:**
- Security regression prevention
- Registry operations
- Code generation validity
- Real-world workflows
- Edge cases
- Performance benchmarks

**When to Run:**
- Before every release
- After major refactoring
- Weekly automated runs

## Test Categories

### Security Tests (CRITICAL)
These tests MUST NEVER FAIL. They protect against:
- Path traversal attacks
- Command injection
- XSS attacks
- Insecure cryptography

**Failure Action:** BLOCK DEPLOYMENT

### Functional Tests (HIGH PRIORITY)
Ensure core features work correctly:
- Project creation
- Registry management
- Code generation
- Git integration

**Failure Action:** FIX IMMEDIATELY

### Performance Tests (MEDIUM PRIORITY)
Ensure acceptable performance:
- Registry scales to 100+ projects
- XML generation handles 50+ widgets
- Operations complete in reasonable time

**Failure Action:** INVESTIGATE AND OPTIMIZE

### Edge Case Tests (MEDIUM PRIORITY)
Handle unusual inputs gracefully:
- Empty values
- Very long strings
- Unicode characters
- Corrupted data

**Failure Action:** FIX OR DOCUMENT

## Running Tests

### Quick Check (< 1 second)
```bash
python3 tests/test_security_fixes.py
```

### Full Suite (< 1 second)
```bash
python3 tests/test_security_fixes.py && \
python3 tests/test_error_handling.py && \
python3 tests/test_critical_regression.py
```

### With Coverage
```bash
python3 -m pytest tests/ --cov=src/pygubuai --cov-report=term-missing
```

### Continuous Integration
```bash
make test  # Runs all tests with proper setup
```

## Test Quality Metrics

### Current Status
- **Total Tests:** 59
- **Pass Rate:** 100%
- **Coverage:** ~12% (needs improvement)
- **Run Time:** < 0.3s (excellent)

### Targets
- **Total Tests:** 100+ (by v1.0)
- **Pass Rate:** 100% (always)
- **Coverage:** 80%+ (by v1.0)
- **Run Time:** < 5s (maintain)

## Critical Test Scenarios

### 1. Security Regression Prevention
```python
def test_path_traversal_always_blocked(self):
    """CRITICAL: Path traversal must always be blocked."""
    malicious_paths = ["../../../etc/passwd", ...]
    for path in malicious_paths:
        with self.assertRaises(ValueError):
            validate_safe_path(path)
```

**Why Critical:** Prevents unauthorized file access

### 2. Registry Corruption Recovery
```python
def test_registry_survives_corruption(self):
    """CRITICAL: Registry must handle corrupted files gracefully."""
    registry_file.write_text("{ invalid json }")
    registry = Registry(registry_file)  # Must not crash
    projects = registry.list_projects()  # Must return valid dict
```

**Why Critical:** Prevents data loss and crashes

### 3. Generated Code Validity
```python
def test_generated_python_always_valid(self):
    """CRITICAL: Generated Python must always be valid syntax."""
    code = generate_python_app_structure(name, callbacks)
    compile(code, "<generated>", "exec")  # Must not raise
```

**Why Critical:** Ensures users get working code

### 4. End-to-End Workflow
```python
def test_create_project_end_to_end(self):
    """CRITICAL: Basic project creation must always work."""
    # Create project, generate files, verify validity
```

**Why Critical:** Core user workflow must work

## Adding New Tests

### When to Add Tests

1. **Before fixing a bug** - Write test that reproduces bug
2. **When adding features** - Test new functionality
3. **After security review** - Add security test cases
4. **When users report issues** - Add regression test

### Test Template

```python
def test_feature_name(self):
    """Brief description of what is being tested."""
    # Arrange - Set up test data
    test_data = create_test_data()
    
    # Act - Execute the code being tested
    result = function_under_test(test_data)
    
    # Assert - Verify expected behavior
    self.assertEqual(result, expected_value)
    self.assertIsNotNone(result)
```

### Test Naming Convention

- `test_<component>_<scenario>` - Normal tests
- `test_<component>_always_<behavior>` - Critical tests
- `test_<component>_edge_case_<case>` - Edge case tests

## Continuous Improvement

### Weekly Review
- Check test coverage reports
- Identify untested code paths
- Add tests for new features
- Update test documentation

### Monthly Audit
- Review test execution times
- Optimize slow tests
- Remove redundant tests
- Update test strategy

### Release Checklist
- [ ] All tests pass
- [ ] No security test failures
- [ ] Coverage > 80%
- [ ] Performance tests pass
- [ ] New features have tests
- [ ] Bug fixes have regression tests

## Test Maintenance

### Keeping Tests Useful

1. **Keep tests fast** - Total suite < 5 seconds
2. **Keep tests focused** - One assertion per test when possible
3. **Keep tests independent** - No test dependencies
4. **Keep tests readable** - Clear names and comments
5. **Keep tests updated** - Update when code changes

### Red Flags

- Tests that fail intermittently
- Tests that take > 1 second
- Tests with unclear purpose
- Tests that test implementation details
- Tests that are commented out

## Integration with Development

### Pre-Commit Hook
```bash
#!/bin/bash
python3 tests/test_security_fixes.py || exit 1
python3 tests/test_error_handling.py || exit 1
```

### CI/CD Pipeline
```yaml
test:
  script:
    - python3 -m pytest tests/ --cov=src/pygubuai
    - python3 tests/test_critical_regression.py
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### IDE Integration
Configure your IDE to run tests on save or with keyboard shortcut.

## Troubleshooting

### Test Failures

1. **Read the error message** - Usually tells you what's wrong
2. **Check recent changes** - What changed since tests last passed?
3. **Run test in isolation** - `python3 -m pytest tests/test_file.py::TestClass::test_method`
4. **Add debug output** - Use `print()` or `logging` to understand state
5. **Check test data** - Verify test setup is correct

### Common Issues

**Issue:** Tests pass locally but fail in CI  
**Solution:** Check for environment differences, file paths, dependencies

**Issue:** Tests are slow  
**Solution:** Use mocks, reduce I/O, parallelize tests

**Issue:** Tests are flaky  
**Solution:** Remove timing dependencies, fix race conditions

## Resources

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

---

**Last Updated:** 2025-01-31  
**Version:** 0.8.0  
**Maintained By:** PygubuAI Team
