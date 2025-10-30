# Contributing to PygubuAI

Thank you for your interest in contributing to PygubuAI! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- Python 3.9+
- Git
- pygubu and pygubu-designer

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Or use make
make dev

# Run tests
make test

# Check coverage
make coverage

# Lint code
make lint
```

## Project Structure

```
PygubuAI/
├── src/pygubuai/          # Main package
│   ├── __init__.py        # Version and package init
│   ├── create.py          # pygubu-create CLI
│   ├── register.py        # pygubu-register CLI
│   ├── template.py        # pygubu-template CLI
│   ├── workflow.py        # pygubu-ai-workflow CLI
│   ├── config.py          # Configuration
│   ├── errors.py          # Error handling
│   ├── registry.py        # Thread-safe registry
│   ├── templates.py       # Template definitions
│   ├── utils.py           # Utilities
│   └── widgets.py         # Widget detection
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Example projects
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Write Code

Follow these guidelines:
- Use type hints for function parameters and return values
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use descriptive variable names
- Follow PEP 8 style guide

Example:
```python
def validate_project_name(name: str) -> str:
    """Validate and sanitize project name.
    
    Args:
        name: Raw project name from user input
        
    Returns:
        Sanitized project name safe for filesystem
        
    Raises:
        PygubuAIError: If name is empty after sanitization
    """
    # Implementation
```

### 3. Write Tests

All new features must include tests:

```python
# tests/test_your_feature.py
import unittest
from pygubuai.your_module import your_function

class TestYourFeature(unittest.TestCase):
    def test_basic_functionality(self):
        """Test basic functionality"""
        result = your_function("input")
        self.assertEqual(result, "expected")
```

Run tests:
```bash
make test
# or
python -m pytest tests/
```

### 4. Update Documentation

- Update README.md if adding user-facing features
- Update CHANGELOG.md with your changes
- Add docstrings to all new functions/classes
- Update relevant docs/ files

### 5. Commit Changes

Write clear commit messages:
```bash
git add .
git commit -m "feat: add new template for dashboard UI"
# or
git commit -m "fix: handle missing .ui files gracefully"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots (if UI changes)
- Test results

## Code Style

### Python Style
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use double quotes for strings

### Formatting
```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/
```

### Type Hints
Always use type hints:
```python
from typing import Optional, Dict, List

def process_project(name: str, config: Optional[Dict] = None) -> List[str]:
    """Process project with optional config"""
    pass
```

## Testing Guidelines

### Test Structure
```python
class TestFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests"""
        shutil.rmtree(self.temp_dir)
    
    def test_success_case(self):
        """Test successful operation"""
        pass
    
    def test_error_case(self):
        """Test error handling"""
        with self.assertRaises(ExpectedError):
            function_that_should_fail()
```

### Coverage
Aim for >80% code coverage:
```bash
make coverage
# View HTML report
open htmlcov/index.html
```

## Error Handling

Always use custom exceptions:
```python
from pygubuai.errors import PygubuAIError, ProjectNotFoundError

def find_project(name: str) -> Dict:
    """Find project by name"""
    if name not in projects:
        raise ProjectNotFoundError(
            name, 
            "Use 'pygubu-register list' to see available projects"
        )
    return projects[name]
```

## Adding New Features

### New CLI Command
1. Create module in `src/pygubuai/your_command.py`
2. Add entry point in `pyproject.toml`:
   ```toml
   [project.scripts]
   pygubu-your-command = "pygubuai.your_command:main"
   ```
3. Create wrapper script `pygubu-your-command`
4. Add tests in `tests/test_your_command.py`
5. Update README.md and docs

### New Template
1. Add template to `src/pygubuai/templates.py`:
   ```python
   TEMPLATES["your_template"] = {
       "name": "your_template",
       "description": "Description",
       "widgets": [...]
   }
   ```
2. Add tests
3. Update documentation

## Release Process

1. Update version in `src/pygubuai/__init__.py`
2. Update CHANGELOG.md
3. Run full test suite: `make test`
4. Create git tag: `git tag v0.2.0`
5. Push: `git push --tags`

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Join discussions in GitHub Discussions
- Read the documentation in docs/

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Questions?

Feel free to:
- Open an issue with the "question" label
- Start a discussion on GitHub
- Check the documentation

Thank you for contributing to PygubuAI! 🎉
