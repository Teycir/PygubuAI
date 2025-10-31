# PygubuAI Developer Onboarding

Welcome to PygubuAI! This guide will get you up and running in 15 minutes.

---

## 🚀 Quick Start (5 minutes)

### 1. Clone & Install
```bash
git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI
pip install -e ".[dev]"
```

### 2. Verify Installation
```bash
make test-fast          # Should pass in <1 min
pygubu-create --version # Should show version
pygubu-register list    # Should show empty list
```

### 3. Create Test Project
```bash
pygubu-create demo 'simple window with button'
cd demo
ls -la                  # See generated files
```

**✅ You're ready to develop!**

---

## 📚 Essential Reading (10 minutes)

### Must Read (5 min)
1. [QUICK_STATUS.md](QUICK_STATUS.md) - Current project status
2. [TESTING_QUICK_REF.md](TESTING_QUICK_REF.md) - How to test
3. This file - You're here!

### Should Read (5 min)
4. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - What we're building
5. [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md) - Current sprint
6. [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

### Nice to Read (Later)
7. [ROADMAP.md](ROADMAP.md) - Long-term vision
8. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
9. [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) - Deep dive

---

## 🛠️ Development Workflow

### Daily Routine
```bash
# 1. Start your day
git pull origin main
make test-fast

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Develop with TDD
# - Write test first
# - Implement feature
# - Run tests frequently

# 4. Before commit
make test-coverage      # Ensure >90% coverage
make lint               # Check code quality
git add .
git commit -m "feat: add my feature"

# 5. Push and PR
git push origin feature/my-feature
# Create PR on GitHub
```

---

## 🧪 Testing Strategy

### Test Pyramid
```
        /\
       /E2E\      <- Few (integration tests)
      /------\
     /  Unit  \   <- Many (unit tests)
    /----------\
```

### Quick Commands
```bash
make test-fast          # Unit tests only (<1 min)
make test-unit          # All unit tests
make test-integration   # Integration tests
make test               # Everything
make test-coverage      # With HTML report
```

### Test Markers
```bash
pytest -m unit          # Unit tests
pytest -m integration   # Integration tests
pytest -m "not slow"    # Skip slow tests
pytest -m security      # Security tests
```

### Writing Tests
```python
import pytest

@pytest.mark.unit
def test_my_feature(temp_project):
    """
    Test description.
    
    Given: Initial state
    When: Action performed
    Then: Expected result
    """
    # Given
    setup_code()
    
    # When
    result = my_feature()
    
    # Then
    assert result == expected
```

---

## 📁 Project Structure

```
PygubuAI/
├── src/pygubuai/           # Main source code
│   ├── create.py           # Project creation
│   ├── registry.py         # Project registry
│   ├── status.py           # Status checker
│   ├── widgets.py          # Widget browser
│   └── ...                 # Other modules
├── tests/                  # Test suite
│   ├── conftest.py         # Shared fixtures
│   ├── test_*.py           # Test files
│   └── ...
├── docs/                   # Documentation
├── examples/               # Example projects
├── .github/workflows/      # CI/CD
├── pytest.ini              # Test configuration
├── setup.py                # Package setup
├── Makefile                # Convenience commands
└── README.md               # Main docs
```

---

## 🎯 Current Sprint (v0.5.1)

### Goal
Add beautiful terminal output with Rich library

### Tasks (This Week)
- [ ] Complete Rich integration in 4 commands
- [ ] Test graceful fallback
- [ ] Update documentation
- [ ] Release v0.5.1

### How to Help
1. Pick a task from [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md)
2. Comment on the issue (or create one)
3. Implement with tests
4. Submit PR

---

## 💻 Common Tasks

### Add a New Command

**1. Create module:**
```python
# src/pygubuai/mycommand.py
def main():
    """My command implementation"""
    print("Hello from mycommand!")

if __name__ == '__main__':
    main()
```

**2. Add entry point:**
```python
# setup.py
entry_points={
    'console_scripts': [
        'pygubu-mycommand=pygubuai.mycommand:main',
    ],
}
```

**3. Write tests:**
```python
# tests/test_mycommand.py
@pytest.mark.unit
def test_mycommand():
    """Test my command"""
    from pygubuai.mycommand import main
    # Test implementation
```

**4. Update docs:**
- Add to README.md commands table
- Add example to USER_GUIDE.md
- Update CHANGELOG.md

---

### Add Rich Output

**Pattern:**
```python
# Graceful fallback
try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def display_data(data):
    if RICH_AVAILABLE:
        console = Console()
        table = Table(title="My Data")
        table.add_column("Name")
        table.add_column("Value")
        for item in data:
            table.add_row(item.name, item.value)
        console.print(table)
    else:
        # Plain text fallback
        print("My Data")
        for item in data:
            print(f"{item.name}: {item.value}")
```

---

### Add a Test Fixture

**1. Add to conftest.py:**
```python
# tests/conftest.py
@pytest.fixture
def my_fixture(tmp_path):
    """My reusable fixture"""
    # Setup
    data = create_test_data(tmp_path)
    yield data
    # Teardown (optional)
    cleanup(data)
```

**2. Use in tests:**
```python
def test_something(my_fixture):
    """Test using my fixture"""
    result = process(my_fixture)
    assert result.is_valid()
```

---

## 🐛 Debugging Tips

### Enable Debug Logging
```bash
PYGUBUAI_LOG_LEVEL=DEBUG pygubu-status myapp
```

### Run Single Test
```bash
pytest tests/test_status.py::test_specific_function -v
```

### Debug Test
```python
def test_debug():
    import pdb; pdb.set_trace()  # Breakpoint
    # Your test code
```

### Check Coverage
```bash
make test-coverage
open htmlcov/index.html  # View in browser
```

---

## 📝 Code Style

### Conventions
- **Imports:** Standard lib, third-party, local
- **Naming:** snake_case for functions, PascalCase for classes
- **Docstrings:** Google style
- **Line length:** 100 characters
- **Type hints:** Encouraged but not required

### Example
```python
"""Module docstring."""
import os
from pathlib import Path

from rich.console import Console

from pygubuai.registry import Registry


def my_function(name: str, count: int = 1) -> bool:
    """
    Function description.
    
    Args:
        name: The name parameter
        count: The count parameter (default: 1)
    
    Returns:
        True if successful, False otherwise
    """
    # Implementation
    return True
```

---

## 🔧 Tools & Setup

### Recommended IDE Setup

**VS Code:**
```json
{
  "python.testing.pytestEnabled": true,
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

**PyCharm:**
- Enable pytest as test runner
- Enable PEP 8 checking
- Set line length to 100

### Git Hooks (Optional)
```bash
# .git/hooks/pre-commit
#!/bin/bash
make test-fast
make lint
```

---

## 🎓 Learning Resources

### Python & Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/)
- [Test-Driven Development](https://www.obeythetestinggoat.com/)

### Tkinter & Pygubu
- [Pygubu Documentation](https://github.com/alejandroautalan/pygubu)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Pygubu Designer](https://github.com/alejandroautalan/pygubu-designer)

### Rich Terminal UI
- [Rich Documentation](https://rich.readthedocs.io/)
- [Rich Examples](https://github.com/Textualize/rich/tree/master/examples)

---

## 🤝 Getting Help

### Stuck on Something?
1. Check [QUICK_STATUS.md](QUICK_STATUS.md) for current status
2. Search [GitHub Issues](https://github.com/Teycir/PygubuAI/issues)
3. Ask in [GitHub Discussions](https://github.com/Teycir/PygubuAI/discussions)
4. Read relevant docs in [docs/](docs/)

### Found a Bug?
1. Check if it's already reported
2. Create minimal reproduction
3. Open GitHub issue with details
4. Include: OS, Python version, error message

### Want to Contribute?
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md) for tasks
3. Comment on issue or create new one
4. Fork, implement, test, PR!

---

## ✅ Onboarding Checklist

### Setup
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Tests passing
- [ ] Test project created

### Knowledge
- [ ] Read QUICK_STATUS.md
- [ ] Read TESTING_QUICK_REF.md
- [ ] Read IMPLEMENTATION_PLAN.md
- [ ] Understand project structure

### First Contribution
- [ ] Pick a task from PROGRESS_TRACKER.md
- [ ] Create feature branch
- [ ] Implement with tests
- [ ] Submit PR
- [ ] Celebrate! 🎉

---

## 🎉 Welcome to the Team!

You're now ready to contribute to PygubuAI. Here's what to do next:

1. **Explore:** Run the commands, create projects, break things
2. **Learn:** Read the code, understand the architecture
3. **Contribute:** Pick a task, implement, submit PR
4. **Engage:** Join discussions, help others, share ideas

**Remember:**
- Ask questions - no question is too small
- Start small - even docs improvements help
- Have fun - we're building something cool!

---

**Quick Links:**
- [Current Sprint](PROGRESS_TRACKER.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Testing Guide](TESTING_QUICK_REF.md)
- [Contributing Guide](CONTRIBUTING.md)

**Happy Coding! 🚀**
