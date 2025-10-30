# Command Reference

## pygubu-create

Create a new Pygubu project from natural language description.

### Usage
```bash
pygubu-create <project_name> '<description>'
pygubu-create --interactive  # Interactive mode
```

### Examples
```bash
pygubu-create todo 'todo app with entry, button, and list'
pygubu-create calc 'calculator with number pad and display'
pygubu-create notes 'note taking app with text area'
```

### Options
- `--interactive, -i`: Launch interactive project creator
- `--no-register`: Don't register project globally
- `--help, -h`: Show help message

---

## pygubu-register

Manage global project registry.

### Usage
```bash
pygubu-register <command> [args]
```

### Commands

#### add
Register a project
```bash
pygubu-register add <path>
pygubu-register add .  # Current directory
```

#### list
Show all registered projects
```bash
pygubu-register list
```

#### active
Set or show active project
```bash
pygubu-register active <project_name>
pygubu-register active  # Show current active
```

#### scan
Auto-discover projects in directory
```bash
pygubu-register scan ~/projects
pygubu-register scan .
```

#### info
Show detailed info about active project
```bash
pygubu-register info
```

#### remove
Unregister a project
```bash
pygubu-register remove <project_name>
```

---

## pygubu-ai-workflow

AI workflow automation tools.

### Usage
```bash
pygubu-ai-workflow <command> [args]
```

### Commands

#### watch
Watch for UI changes and prompt for sync
```bash
pygubu-ai-workflow watch <project_name>
```

#### sync
Synchronize UI and code
```bash
pygubu-ai-workflow sync <project_name>
```

#### history
Show project workflow history
```bash
pygubu-ai-workflow history <project_name>
```

---

## tkinter-to-pygubu

Convert legacy tkinter code to Pygubu format.

### Usage
```bash
tkinter-to-pygubu <input_file.py> [output_dir]
```

### Examples
```bash
tkinter-to-pygubu old_app.py
tkinter-to-pygubu legacy.py converted/
```

### Options
- `--preview`: Show conversion preview without writing files
- `--force`: Overwrite existing files
