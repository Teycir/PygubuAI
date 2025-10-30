# Quick Start Guide

## Create Your First Project

```bash
pygubu-create myapp 'login form with username, password, and submit button'
cd myapp
python myapp.py
```

## Register and Manage Projects

```bash
# Register current project
pygubu-register add .

# Scan for all projects
pygubu-register scan ~/projects

# List registered projects
pygubu-register list

# Set active project
pygubu-register active myapp
```

## Edit UI Visually

```bash
pygubu-designer myapp.ui
```

## Convert Existing Tkinter Code

```bash
tkinter-to-pygubu old_app.py
```

## Watch for Changes

```bash
pygubu-ai-workflow watch myapp
```

## AI Integration

In your AI chat, use:
- `@pygubu-context` to load project context
- "Add a menu bar to my project"
- "Change button colors to blue"
- "Show my active pygubu project"

## Next Steps

- Read [full documentation](../PYGUBUAI.md)
- Explore [examples](../examples/)
- Check [command reference](COMMANDS.md)
