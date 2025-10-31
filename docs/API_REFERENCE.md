# API Reference

Complete API documentation for PygubuAI v0.8.0.

## Table of Contents

- [Core Modules](#core-modules)
- [Utilities](#utilities)
- [Registry](#registry)
- [Generator](#generator)
- [Git Integration](#git-integration)
- [Error Handling](#error-handling)
- [CLI Commands](#cli-commands)

---

## Core Modules

### pygubuai.utils

Core utility functions for path validation, XML escaping, and file operations.

#### validate_safe_path(path: str | Path, base_dir: Path = None) -> Path

Validates that a path is safe and doesn't contain path traversal attempts.

**Parameters:**
- `path`: Path to validate
- `base_dir`: Optional base directory to validate against

**Returns:** Validated Path object

**Raises:** `ValueError` if path contains ".." or is outside base_dir

**Example:**
```python
from pygubuai.utils import validate_safe_path

# Valid path
safe_path = validate_safe_path("myproject/ui.xml")

# Invalid - raises ValueError
validate_safe_path("../../../etc/passwd")
```

#### safe_xml_text(text: str) -> str

Escapes text for safe use in XML content.

**Parameters:**
- `text`: Text to escape

**Returns:** XML-safe escaped text

**Example:**
```python
from pygubuai.utils import safe_xml_text

escaped = safe_xml_text("<script>alert('xss')</script>")
# Returns: "&lt;script&gt;alert('xss')&lt;/script&gt;"
```

#### get_file_hash(file_path: Path) -> str

Computes SHA-256 hash of a file.

**Parameters:**
- `file_path`: Path to file

**Returns:** 64-character hex string (SHA-256)

**Example:**
```python
from pygubuai.utils import get_file_hash

hash_value = get_file_hash(Path("myfile.txt"))
print(f"SHA-256: {hash_value}")
```

#### validate_project_name(name: str) -> bool

Validates project name contains only safe characters.

**Parameters:**
- `name`: Project name to validate

**Returns:** True if valid

**Raises:** `ValidationError` if invalid

**Example:**
```python
from pygubuai.utils import validate_project_name

validate_project_name("my_project")  # OK
validate_project_name("my<>project")  # Raises ValidationError
```

#### ensure_directory(path: Path) -> Path

Creates directory if it doesn't exist.

**Parameters:**
- `path`: Directory path

**Returns:** Path object

**Raises:** `FileOperationError` on failure

---

### pygubuai.registry

Project registry for tracking and managing PygubuAI projects.

#### Registry

Main registry class for project management.

**Constructor:**
```python
Registry(registry_file: Path = None)
```

**Parameters:**
- `registry_file`: Path to registry JSON file (default: ~/.pygubu-registry.json)

**Methods:**

##### add_project(name: str, path: str | Path, **metadata) -> None

Adds or updates a project in the registry.

**Parameters:**
- `name`: Project name
- `path`: Project directory path
- `**metadata`: Optional metadata (description, tags, etc.)

**Example:**
```python
from pygubuai.registry import Registry

registry = Registry()
registry.add_project(
    "myapp",
    "/home/user/projects/myapp",
    description="My application",
    tags=["gui", "tkinter"]
)
```

##### get_project(name: str) -> dict

Gets project information.

**Parameters:**
- `name`: Project name

**Returns:** Project metadata dict

**Raises:** `ProjectNotFoundError` if not found

##### list_projects() -> dict

Lists all registered projects.

**Returns:** Dict of {name: metadata}

##### set_active(name: str) -> None

Sets the active project.

**Parameters:**
- `name`: Project name

##### get_active() -> str | None

Gets the active project name.

**Returns:** Active project name or None

##### remove_project(name: str) -> None

Removes a project from registry.

**Parameters:**
- `name`: Project name

---

### pygubuai.generator

Code generation for UI XML and Python application structure.

#### generate_base_ui_xml_structure(project_name: str, widgets: list = None) -> str

Generates base Pygubu UI XML structure.

**Parameters:**
- `project_name`: Project name
- `widgets`: List of (widget_type, properties) tuples

**Returns:** XML string

**Example:**
```python
from pygubuai.generator import generate_base_ui_xml_structure

xml = generate_base_ui_xml_structure(
    "myapp",
    [
        ("button", {"id": "btn1", "text": "Click Me"}),
        ("label", {"id": "lbl1", "text": "Hello"})
    ]
)
```

#### generate_python_app_structure(project_name: str, callbacks: list = None) -> str

Generates Python application boilerplate.

**Parameters:**
- `project_name`: Project name
- `callbacks`: List of callback method names

**Returns:** Python code string

**Example:**
```python
from pygubuai.generator import generate_python_app_structure

code = generate_python_app_structure(
    "myapp",
    ["on_button_click", "on_close"]
)
```

#### generate_readme_content(project_name: str, description: str = "") -> str

Generates README.md content.

**Parameters:**
- `project_name`: Project name
- `description`: Project description

**Returns:** Markdown string

---

### pygubuai.git_integration

Git repository initialization and operations.

#### init_git_repo(project_path: Path) -> bool

Initializes a Git repository.

**Parameters:**
- `project_path`: Project directory

**Returns:** True if successful

**Example:**
```python
from pygubuai.git_integration import init_git_repo
from pathlib import Path

success = init_git_repo(Path("/path/to/project"))
```

#### git_commit(project_path: Path, message: str) -> bool

Creates a Git commit.

**Parameters:**
- `project_path`: Project directory
- `message`: Commit message

**Returns:** True if successful

**Example:**
```python
from pygubuai.git_integration import git_commit

git_commit(Path("/path/to/project"), "Initial commit")
```

---

### pygubuai.errors

Custom exception hierarchy for better error handling.

#### PygubuAIError

Base exception for all PygubuAI errors.

**Attributes:**
- `message`: Error message
- `suggestion`: Helpful suggestion
- `cause`: Original exception (if any)

#### ProjectNotFoundError

Raised when a project is not found in registry.

**Example:**
```python
from pygubuai.errors import ProjectNotFoundError

raise ProjectNotFoundError("myapp")
```

#### FileOperationError

Raised when file operations fail.

**Constructor:**
```python
FileOperationError(operation: str, path: Path, cause: Exception = None)
```

#### ValidationError

Raised when validation fails.

**Constructor:**
```python
ValidationError(field: str, value: str, reason: str)
```

#### RegistryError

Raised when registry operations fail.

#### UIParseError

Raised when UI XML parsing fails.

#### GitError

Raised when Git operations fail.

---

## CLI Commands

### pygubu-create

Creates a new PygubuAI project.

**Usage:**
```bash
pygubu-create <name> '<description>' [--dry-run] [--no-git]
```

**Options:**
- `--dry-run`: Show what would be created without creating
- `--no-git`: Skip Git initialization

**Example:**
```bash
pygubu-create myapp 'login form with username and password'
```

### pygubu-register

Manages project registry.

**Usage:**
```bash
pygubu-register <command> [args]
```

**Commands:**
- `list`: List all projects
- `active <name>`: Set active project
- `scan <directory>`: Scan for projects
- `remove <name>`: Remove project

**Example:**
```bash
pygubu-register list
pygubu-register active myapp
pygubu-register scan ~/projects
```

### pygubu-status

Checks project sync status.

**Usage:**
```bash
pygubu-status [project]
```

**Example:**
```bash
pygubu-status myapp
```

### pygubu-validate

Validates project structure and files.

**Usage:**
```bash
pygubu-validate <project>
```

**Example:**
```bash
pygubu-validate myapp
```

---

## Python API Usage Examples

### Creating a Project Programmatically

```python
from pathlib import Path
from pygubuai.generator import generate_base_ui_xml_structure, generate_python_app_structure
from pygubuai.registry import Registry
from pygubuai.git_integration import init_git_repo

# Create project directory
project_path = Path("myapp")
project_path.mkdir(exist_ok=True)

# Generate UI XML
xml = generate_base_ui_xml_structure("myapp", [
    ("button", {"id": "submit_btn", "text": "Submit"}),
    ("entry", {"id": "name_entry"})
])
(project_path / "myapp.ui").write_text(xml)

# Generate Python code
code = generate_python_app_structure("myapp", ["on_submit"])
(project_path / "myapp.py").write_text(code)

# Register project
registry = Registry()
registry.add_project("myapp", project_path)

# Initialize Git
init_git_repo(project_path)
```

### Working with Registry

```python
from pygubuai.registry import Registry

registry = Registry()

# Add project
registry.add_project("myapp", "/path/to/myapp", description="My app")

# List projects
projects = registry.list_projects()
for name, info in projects.items():
    print(f"{name}: {info['path']}")

# Set active
registry.set_active("myapp")

# Get active
active = registry.get_active()
print(f"Active project: {active}")
```

### Error Handling

```python
from pygubuai.registry import Registry
from pygubuai.errors import ProjectNotFoundError, RegistryError

registry = Registry()

try:
    project = registry.get_project("nonexistent")
except ProjectNotFoundError as e:
    print(f"Error: {e}")
    print(f"Suggestion: {e.suggestion}")
except RegistryError as e:
    print(f"Registry error: {e}")
```

---

## Version Information

**Current Version:** 0.8.0

**Compatibility:**
- Python 3.9+
- pygubu >= 0.39
- tkinter (standard library)

**See Also:**
- [User Guide](USER_GUIDE.md)
- [Security Guide](SECURITY_GUIDE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
