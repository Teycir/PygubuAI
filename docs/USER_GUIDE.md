# PygubuAI User Guide

Complete guide for using PygubuAI - AI-powered workflow tools for Pygubu.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands Reference](#commands-reference)
- [Features](#features)
- [Templates](#templates)
- [Workflows](#workflows)
- [Troubleshooting](#troubleshooting)

## Installation

### Recommended: pip install (Preferred)

```bash
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai
pip install -e .
```

This installs PygubuAI as a Python package with CLI commands available system-wide.

**Verify installation:**
```bash
pygubu-create --version
pygubu-register list
```

### Alternative: Shell script install

For systems where pip installation doesn't work:
```bash
./install.sh
```

This copies scripts to `~/bin/` or `/usr/local/bin/`.

### Development Setup

```bash
pip install -e ".[dev]"
make pre-commit-install
make test
```

### Uninstall

```bash
pip uninstall pygubuai  # For pip install
./uninstall.sh          # For shell script install
```

## Quick Start

### Create Your First Project

```bash
# Create a simple app
pygubu-create myapp 'login form with username and password'

# Navigate and run
cd myapp
python myapp.py
```

### Use Templates

```bash
# List available templates
pygubu-template list

# Create from template
pygubu-template myapp login
```

### Register Projects

```bash
# Scan for projects
pygubu-register scan ~/projects

# Set active project
pygubu-register active myapp

# List all projects
pygubu-register list
```

## Commands Reference

### pygubu-create

Create new projects from natural language descriptions.

**Syntax:**
```bash
pygubu-create <name> '<description>'
```

**Examples:**
```bash
pygubu-create todo 'todo app with entry, button, and list'
pygubu-create calc 'calculator with number pad and display'
pygubu-create form 'data entry form with name, email, and submit'
```

**Supported widgets:**
- Labels, Entries, Buttons
- Lists (Treeview), Text areas
- Dropdowns (Combobox), Checkboxes
- Sliders, Progress bars, Tabs

### pygubu-template

Create projects from pre-built templates.

**Syntax:**
```bash
pygubu-template <name> <template>
pygubu-template list
```

**Available templates:**
- `login` - Login form with username/password
- `crud` - CRUD interface with list and form
- `settings` - Settings dialog with tabs
- `dashboard` - Dashboard with metrics
- `wizard` - Multi-step wizard

**Examples:**
```bash
pygubu-template myapp login
pygubu-template admin crud
pygubu-template config settings
```

### pygubu-register

Manage project registry for AI context.

**Commands:**
```bash
pygubu-register list                    # List all projects
pygubu-register active <name>           # Set active project
pygubu-register add <path>              # Add project manually
pygubu-register scan <directory>        # Auto-discover projects
pygubu-register remove <name>           # Remove project
```

**Examples:**
```bash
pygubu-register scan ~/projects
pygubu-register active myapp
pygubu-register list
```

### pygubu-ai-workflow

Workflow automation and monitoring.

**Commands:**
```bash
pygubu-ai-workflow watch <project>      # Watch for UI changes
pygubu-ai-workflow status <project>     # Show project status
```

### tkinter-to-pygubu

Convert existing tkinter code to pygubu format.

**Syntax:**
```bash
tkinter-to-pygubu <file>.py
```

**Example:**
```bash
tkinter-to-pygubu legacy_app.py
```

## Features

### Natural Language UI Creation

Describe your UI in plain English:

```bash
pygubu-create app 'search interface with text entry, search button, and results list'
```

PygubuAI detects widgets and creates:
- `.ui` file (Pygubu XML)
- `.py` file (Python application)
- `README.md` (Documentation)

### Widget Detection

PygubuAI recognizes these patterns:

| Description | Detected Widget |
|-------------|----------------|
| "button", "submit", "click" | ttk.Button |
| "entry", "input", "field" | ttk.Entry |
| "list", "table", "tree" | ttk.Treeview |
| "dropdown", "select", "combo" | ttk.Combobox |
| "checkbox", "check" | ttk.Checkbutton |
| "text area", "multiline" | tk.Text |
| "label", "title", "heading" | ttk.Label |

### Context-Aware Generation

Special contexts trigger pre-configured layouts:

- **"login"** → username label, entry, password label, entry, button
- **"form"** → label, entry, entry, button
- **"search"** → entry, button, treeview

### Global Project Registry

All projects are tracked in `~/.pygubu-registry.json`:

```json
{
  "projects": [
    {
      "name": "myapp",
      "path": "/home/user/projects/myapp",
      "ui_file": "myapp.ui",
      "py_file": "myapp.py"
    }
  ],
  "active_project": "myapp"
}
```

This enables:
- Access projects from any directory
- AI context awareness across sessions
- Quick project switching

### AI Chat Integration

Use `@pygubu-context` prompt in AI chats for automatic context loading.

**Example conversation:**
```
You: @pygubu-context Add a menu bar to my project
AI: [Loads active project context and suggests changes]

You: Change button color to blue
AI: [Updates the active project's UI file]
```

## Templates

### Login Template

Creates a professional login form:
- Username label and entry
- Password label and entry (with show/hide)
- Login button
- Remember me checkbox

```bash
pygubu-template myapp login
```

### CRUD Template

Full CRUD interface:
- List view (Treeview)
- Add/Edit/Delete buttons
- Form fields
- Search functionality

```bash
pygubu-template admin crud
```

### Settings Template

Tabbed settings dialog:
- Multiple tabs (General, Advanced, About)
- Various input types
- Save/Cancel buttons

```bash
pygubu-template config settings
```

### Dashboard Template

Metrics dashboard:
- Multiple frames for widgets
- Labels for metrics
- Progress indicators

```bash
pygubu-template app dashboard
```

### Wizard Template

Multi-step wizard:
- Step navigation
- Back/Next/Finish buttons
- Progress indicator

```bash
pygubu-template setup wizard
```

## Workflows

### Collaborative Design Workflow

**Terminal 1: Watch for changes**
```bash
pygubu-ai-workflow watch myapp
```

**Terminal 2: Visual editing**
```bash
pygubu-designer myapp/myapp.ui
```

**AI Chat:**
```
"I added a menu bar in the designer, update the Python code"
```

The watch mode detects UI changes and prompts for code synchronization.

### Convert Existing App Workflow

```bash
# Convert legacy code
tkinter-to-pygubu old_app.py

# Register the project
cd old_app
pygubu-register add .

# Modernize with AI
# In AI chat: "Modernize the UI with ttk widgets"
```

### Iterative Development Workflow

```bash
# Create initial project
pygubu-create app 'simple calculator'

# Register it
pygubu-register active app

# Iterate with AI
# "Add memory functions"
# "Add scientific mode"
# "Improve layout"
```

## Troubleshooting

### Command not found

**Problem:** `pygubu-create: command not found`

**Solution:**
```bash
# Verify installation
pip list | grep pygubuai

# Reinstall
pip install -e .

# Check PATH
echo $PATH | grep -o "[^:]*bin"
```

### Import errors

**Problem:** `ModuleNotFoundError: No module named 'pygubu'`

**Solution:**
```bash
pip install pygubu pygubu-designer
```

### UI file not loading

**Problem:** `FileNotFoundError: myapp.ui`

**Solution:**
- Ensure you're in the project directory
- Check file exists: `ls *.ui`
- Verify path in Python file

### Registry issues

**Problem:** Projects not showing in registry

**Solution:**
```bash
# Rescan projects
pygubu-register scan ~/projects

# Manually add
pygubu-register add /path/to/project
```

### Windows compatibility

**Problem:** Scripts don't work on Windows

**Solution:**
- Use pip installation (preferred)
- Use Python directly: `python -m pygubuai.create`
- Check Python is in PATH

## Best Practices

1. **Use pip installation** - More reliable than shell scripts
2. **Register projects** - Enable AI context awareness
3. **Use templates** - Faster than creating from scratch
4. **Iterate with AI** - Describe changes in natural language
5. **Version control** - Commit both .ui and .py files
6. **Test frequently** - Run `python myapp.py` after changes

## Next Steps

- Read [Developer Guide](DEVELOPER_GUIDE.md) for contributing
- Check [Quick Reference](../pygubuai-quickref.txt) for command cheat sheet
- Explore [examples/](../examples/) for sample projects

---

**Need help?** Open an issue on GitHub or check the documentation.
