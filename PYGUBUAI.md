# PygubuAI - AI-Powered Tkinter Development

AI-integrated workflow for building Tkinter applications with Pygubu designer.

## 🚀 Quick Start

```bash
# Create a new project
~/pygubu-create myapp 'login form with username and password'

# Register existing projects
~/pygubu-register scan ~/projects

# Set active project
~/pygubu-register active myapp

# Open designer
~/pygubu-designer myapp/myapp.ui
```

## 🤖 AI Workflow

### In ANY chat, say:
- "Work on my pygubu project"
- "Add a button to the UI"
- "Change the color scheme"
- "Show my projects"

AI automatically loads your active project and makes changes!

## 📦 Installation

```bash
# Install pygubu
cd ~/Repos/pygubu
python3 -m venv venv
venv/bin/pip install -e .
venv/bin/pip install pygubu-designer

# Tools are in ~/
~/pygubu-create
~/pygubu-register
~/pygubu-designer
~/pygubu-ai-workflow
~/tkinter-to-pygubu
```

## 🛠️ Commands

### Create Projects
```bash
# AI-powered creation
~/pygubu-create <name> '<description>'

# Examples
~/pygubu-create todo 'todo app with entry, button, and list'
~/pygubu-create login 'login form with username and password'
```

### Manage Projects
```bash
# List all projects
~/pygubu-register list

# Set active project
~/pygubu-register active <name>

# Show active project
~/pygubu-register info

# Auto-scan directory
~/pygubu-register scan ~/projects

# Register specific project
~/pygubu-register add /path/to/project
```

### Convert Existing Code
```bash
# Convert tkinter to pygubu
~/tkinter-to-pygubu myapp.py

# Creates:
# - myapp_pygubu.ui
# - myapp_pygubu.py
```

### AI Workflow
```bash
# Watch for UI changes
~/pygubu-ai-workflow watch myapp

# Create with AI tracking
~/pygubu-ai-workflow create myapp 'description'
```

### Design
```bash
# Open designer
~/pygubu-designer myapp.ui

# Open active project
~/pygubu-register info | grep ui_files
```

## 🎯 Workflow Examples

### Example 1: New Project
```bash
# Create
~/pygubu-create calculator 'calculator with number pad and display'

# Set active
~/pygubu-register active calculator

# In any chat: "Add memory buttons to my calculator"
```

### Example 2: Convert Existing
```bash
# You have old_app.py
~/tkinter-to-pygubu old_app.py

# Register
~/pygubu-register add .

# In any chat: "Modernize the UI"
```

### Example 3: Collaborative Design
```bash
# Start watch mode
~/pygubu-ai-workflow watch myapp

# Open designer
~/pygubu-designer myapp/myapp.ui

# Edit visually, save
# In chat: "I added a logout button, update the code"
```

## 📁 File Structure

```
~/.pygubu-registry.json          # Global project registry
~/.amazonq/prompts/pygubu-context.md  # AI context prompt

project/
├── project.ui                   # UI definition
├── project.py                   # Python code
├── .ai-context.json            # AI metadata
└── .pygubu-workflow.json       # Workflow tracking
```

## 🎨 Features

✅ **Natural Language UI Creation** - Describe what you want, AI generates it  
✅ **Global Project Registry** - Access any project from any chat  
✅ **Visual + Code Sync** - Edit visually, AI updates code  
✅ **Auto-detection** - Watches for UI changes  
✅ **Convert Existing** - Migrate tkinter apps to pygubu  
✅ **Context Tracking** - AI remembers your project state  

## 💡 AI Integration

### Use the saved prompt:
```
@pygubu-context Show my active project
```

### Or just say:
- "Add validation to my form"
- "Change button colors to blue"
- "Add a menu bar"
- "Create a settings dialog"

AI reads `~/.pygubu-registry.json` and loads your active project automatically!

## 🔧 Advanced

### Custom Widgets
Edit `~/Repos/pygubu/src/pygubu/widgets/` to add custom widgets.

### Themes
Projects support bootstrap themes via pygubu's theming module.

### Plugins
Pygubu supports: customtkinter, tkcalendar, tksheet, ttkwidgets, and more.

## 📚 Resources

- [Pygubu Wiki](https://github.com/alejandroautalan/pygubu/wiki)
- [Pygubu Designer](https://github.com/alejandroautalan/pygubu-designer)
- [TkDocs](http://www.tkdocs.com)

## 🎮 Example: Number Guessing Game

```bash
~/pygubu-create number_game 'number guessing game with entry and button'
~/pygubu-register active number_game
```

Then in chat: "Add hints and attempt counter"

AI updates both UI and logic!

---

**Made with ❤️ for seamless AI-human collaboration**
