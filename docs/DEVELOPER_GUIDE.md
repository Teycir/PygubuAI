# PygubuAI Developer Guide

Technical documentation for contributing to PygubuAI.

## Table of Contents
- [Architecture](#architecture)
- [Development Setup](#development-setup)
- [Code Structure](#code-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [API Reference](#api-reference)

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  CLI Commands: pygubu-create, pygubu-register, etc.    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Core Modules                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ create.py│  │register.py│  │template.py│             │
│  └──────────┘  └──────────┘  └──────────┘             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │widgets.py│  │generator.py│  │workflow.py│            │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Shared Utilities                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ utils.py │  │ config.py│  │ errors.py│              │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                Data Layer                                │
│  ~/.pygubu-registry.json                                │
│  ~/.amazonq/prompts/pygubu-context.md                   │
│  <project>/.pygubu-workflow.json                        │
└─────────────────────────────────────────────────────────┘
```

### Module Responsibilities

#### create.py
- **Purpose:** Project creation from natural language
- **Key Functions:**
  - `create_project(name: str, description: str) -> None`
  - `main(args: List[str]) -> None`
- **Dependencies:** widgets, generator, utils, errors

#### widgets.py
- **Purpose:** Widget detection and XML generation
- **Key Functions:**
  - `detect_widgets(description: str) -> List[Tuple[str, Dict]]`
  - `generate_widget_xml(widget_type: str, widget_id: str, config: dict, index: int) -> List[str]`
  - `get_callbacks(widgets: List[Tuple]) -> List[str]`
- **Data:** WIDGET_PATTERNS, CONTEXT_PATTERNS

#### generator.py
- **Purpose:** Code and XML generation
- **Key Functions:**
  - `generate_base_ui_xml_structure(project_name: str, widgets_data: List) -> str`
  - `generate_python_app_structure(project_name: str, callbacks: List[str]) -> str`
  - `generate_readme_content(project_name: str, description: str, ui_file_name: str) -> str`

#### registry.py
- **Purpose:** Project registry management
- **Key Class:** `ProjectRegistry`
  - `add_project(name: str, path: str) -> None`
  - `list_projects() -> List[Dict]`
  - `set_active(name: str) -> None`
  - `scan_directory(directory: str) -> List[str]`

#### template.py
- **Purpose:** Template-based project creation
- **Key Functions:**
  - `create_from_template(name: str, template: str) -> None`
  - `list_templates() -> None`
- **Dependencies:** templates, generator

#### workflow.py
- **Purpose:** Workflow automation and monitoring
- **Key Functions:**
  - `watch_project(project_name: str) -> None`
  - `get_project_status(project_name: str) -> Dict`

## Development Setup

### Prerequisites

- Python 3.9+
- Git
- pygubu and pygubu-designer

### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
make pre-commit-install

# Run tests
make test
```

### Development Tools

```bash
# Run tests
make test

# Run with coverage
make coverage

# Format code
make format

# Type checking
make typecheck

# Lint code
make lint

# All checks
make lint && make typecheck && make test
```

### Pre-commit Hooks

Pre-commit hooks automatically run on every commit:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML validation
- Black formatting
- Flake8 linting
- Mypy type checking

**Manual run:**
```bash
pre-commit run --all-files
```

## Code Structure

### Project Layout

```
PygubuAI/
├── src/pygubuai/          # Main package
│   ├── __init__.py        # Version and exports
│   ├── create.py          # Project creation
│   ├── register.py        # Registry CLI
│   ├── registry.py        # Registry logic
│   ├── template.py        # Template CLI
│   ├── templates.py       # Template definitions
│   ├── widgets.py         # Widget detection
│   ├── generator.py       # Code generation
│   ├── workflow.py        # Workflow automation
│   ├── utils.py           # Shared utilities
│   ├── config.py          # Configuration
│   └── errors.py          # Error handling
├── tests/                 # Test suite
│   ├── test_create.py
│   ├── test_registry.py
│   ├── test_widgets.py
│   ├── test_integration.py
│   └── ...
├── docs/                  # Documentation
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   └── ARCHITECTURE.md
├── examples/              # Example projects
├── .github/workflows/     # CI/CD
├── pyproject.toml         # Package configuration
├── Makefile               # Development commands
└── README.md              # Main documentation
```

### Coding Standards

#### Style Guide

- **Line length:** 120 characters
- **Formatter:** Black
- **Linter:** Flake8
- **Type checker:** Mypy

#### Naming Conventions

- **Functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** `_leading_underscore`

#### Type Hints

All public functions should have type hints:

```python
def create_project(name: str, description: str) -> None:
    """Create project with error handling"""
    ...

def detect_widgets(description: str) -> List[Tuple[str, Dict[str, Any]]]:
    """Detect widgets from description"""
    ...
```

#### Error Handling

Use custom exceptions from `errors.py`:

```python
from .errors import PygubuAIError, validate_pygubu

try:
    validate_pygubu()
    # ... operation
except PygubuAIError as e:
    logger.error(str(e))
    sys.exit(1)
```

#### Logging

Use structured logging:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("[SUCCESS] Created project: %s", project_path)
logger.error("[ERROR] Failed to create project: %s", error)
```

## Testing

### Test Structure

```
tests/
├── test_create.py         # Unit tests for create module
├── test_registry.py       # Unit tests for registry
├── test_widgets.py        # Unit tests for widgets
├── test_integration.py    # Integration tests
└── ...
```

### Writing Tests

#### Unit Tests

```python
import unittest
from pygubuai.widgets import detect_widgets

class TestWidgetDetection(unittest.TestCase):
    def test_button_detection(self):
        widgets = detect_widgets("app with button")
        self.assertTrue(any(w[0] == 'button' for w in widgets))
```

#### Integration Tests

```python
class TestEndToEndWorkflow(unittest.TestCase):
    def test_create_and_register_workflow(self):
        # Create project
        create_project("testapp", "simple app")
        
        # Verify files
        self.assertTrue(Path("testapp/testapp.ui").exists())
        
        # Register project
        registry = ProjectRegistry()
        registry.add_project("testapp", str(Path.cwd() / "testapp"))
```

### Running Tests

```bash
# All tests
make test

# With coverage
make coverage

# Specific test file
pytest tests/test_create.py -v

# Specific test
pytest tests/test_create.py::TestProjectCreation::test_parse_description -v
```

### Coverage Goals

- **Minimum:** 80% coverage
- **Target:** 90% coverage
- **Critical modules:** 95%+ coverage (create, registry, widgets)

## Contributing

### Workflow

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/my-feature`
3. **Make** changes with tests
4. **Run** checks: `make lint && make typecheck && make test`
5. **Commit** with clear message
6. **Push** and create Pull Request

### Commit Messages

Follow conventional commits:

```
feat: add dashboard template
fix: resolve registry path issue
docs: update installation guide
test: add integration tests
refactor: simplify widget detection
```

### Pull Request Guidelines

- Clear description of changes
- Tests for new features
- Documentation updates
- All CI checks passing
- No decrease in code coverage

## API Reference

### create.py

#### create_project
```python
def create_project(name: str, description: str) -> None:
    """
    Create a new Pygubu project from natural language description.
    
    Args:
        name: Project name (alphanumeric and underscores only)
        description: Natural language description of the UI
        
    Raises:
        PygubuAIError: If validation fails or project creation fails
        
    Example:
        create_project("myapp", "login form with username and password")
    """
```

### widgets.py

#### detect_widgets
```python
def detect_widgets(description: str) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Detect widgets from natural language description.
    
    Args:
        description: Natural language description
        
    Returns:
        List of (widget_type, config) tuples
        
    Example:
        widgets = detect_widgets("app with button and entry")
        # Returns: [('button', {...}), ('entry', {...})]
    """
```

#### generate_widget_xml
```python
def generate_widget_xml(
    widget_type: str, 
    widget_id: str, 
    config: dict, 
    index: int = 1
) -> List[str]:
    """
    Generate XML lines for a widget.
    
    Args:
        widget_type: Type of widget (button, entry, etc.)
        widget_id: Unique identifier for the widget
        config: Widget configuration dictionary
        index: Widget index for positioning
        
    Returns:
        List of XML lines
    """
```

### registry.py

#### ProjectRegistry
```python
class ProjectRegistry:
    """Manage project registry for AI context."""
    
    def __init__(self, registry_path: str = None):
        """Initialize registry with optional custom path."""
        
    def add_project(self, name: str, path: str) -> None:
        """Add project to registry."""
        
    def list_projects(self) -> List[Dict[str, str]]:
        """List all registered projects."""
        
    def set_active(self, name: str) -> None:
        """Set active project for AI context."""
        
    def scan_directory(self, directory: str) -> List[str]:
        """Scan directory for Pygubu projects."""
```

### generator.py

#### generate_base_ui_xml_structure
```python
def generate_base_ui_xml_structure(
    project_name: str, 
    widgets_data: List[Tuple[str, Dict[str, Any]]]
) -> str:
    """
    Generate complete UI XML structure.
    
    Args:
        project_name: Name of the project
        widgets_data: List of (widget_type, config) tuples
        
    Returns:
        Complete XML string for .ui file
    """
```

#### generate_python_app_structure
```python
def generate_python_app_structure(
    project_name: str, 
    callbacks: List[str], 
    custom_callbacks_code: str = ""
) -> str:
    """
    Generate Python application code.
    
    Args:
        project_name: Name of the project
        callbacks: List of callback function names
        custom_callbacks_code: Optional custom callback implementations
        
    Returns:
        Complete Python code string
    """
```

## Release Process

1. Update version in `src/pygubuai/__init__.py`
2. Update `CHANGELOG.md`
3. Run full test suite: `make test && make coverage`
4. Create git tag: `git tag v0.2.0`
5. Push tag: `git push origin v0.2.0`
6. Build package: `python -m build`
7. Upload to PyPI: `twine upload dist/*`

---

**Questions?** Open an issue or discussion on GitHub.
