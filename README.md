# PygubuAI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The first AI-native workflow system for visual UI development - Build Tkinter applications by simply describing what you want in plain English.

## The Problem

Building Tkinter GUIs traditionally requires:

```python
# 50+ lines of boilerplate for a simple login form
import tkinter as tk
from tkinter import ttk

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        
        self.label_user = ttk.Label(master, text="Username:")
        self.label_user.grid(row=0, column=0, sticky="w")
        self.entry_user = ttk.Entry(master)
        self.entry_user.grid(row=0, column=1)
        # ... 40 more lines ...
```

You need to:
- Memorize Tkinter API (200+ widget methods)
- Write repetitive boilerplate for every UI element
- Manually manage layout (grid/pack/place)
- Keep UI and logic tightly coupled
- Start from scratch for each new project

## The PygubuAI Solution

Just say this in any AI assistant:

```
pygubuai create a login form with username, password, and submit button
```

You get:
- `login.ui` - Visual XML definition (editable in Pygubu Designer)
- `login.py` - Clean Python code with proper separation
- Automatic project registration
- Ready to run in 3 seconds

### Real-World Example

**Scenario**: You need to add a "Remember Me" checkbox to your login form.

**Traditional Way** (5-10 minutes):
1. Open Python file
2. Find the right place in grid layout
3. Write: `self.remember_var = tk.BooleanVar()...`
4. Add: `self.check_remember = ttk.Checkbutton(...)...`
5. Configure grid position
6. Update callback logic
7. Test and debug layout issues

**PygubuAI Way** (30 seconds):
```
pygubuai add a remember me checkbox to my login form
```

AI automatically:
- Updates the .ui XML with proper positioning
- Adds Python variable and widget reference
- Maintains existing layout structure
- Preserves all your custom logic

### Cross-AI Project Memory

**Scenario**: You start a project in Amazon Q at work, continue in Kilo Code at home.

**Traditional Way**: 
- Manually track project locations
- Remember file structures
- Re-explain context to each AI
- Copy-paste previous conversations

**PygubuAI Way**:
```
# At work (Amazon Q)
pygubuai create a settings dialog with theme selector

# At home (Kilo Code) - different AI, same project
pygubuai add a font size slider to my settings dialog
```

Global registry (`~/.pygubu-registry.json`) tracks all projects. Any AI assistant instantly knows:
- Where your projects are
- What you're working on
- Project structure and history
- No context loss between sessions or tools

## Key Innovations

### 1. AI-Native Architecture

Traditional tools adapt AI to existing workflows. PygubuAI inverts this:

- **Trigger Word System**: "pygubuai" activates specialized GUI development mode in any AI
- **Context Injection**: AI assistants learn Pygubu patterns through tool-specific prompts
- **Global State**: Projects persist across tools and sessions via shared registry
- **Bidirectional Sync**: Visual changes auto-update code, natural language updates both

### 2. Visual-Code Harmony

Edit your UI in Pygubu Designer (drag-and-drop), then:

```bash
pygubu-ai-workflow watch myapp
```

AI detects changes and asks: "I see you added a button. Should I update the Python code?"

No manual synchronization. No code regeneration. Just seamless updates.

### 3. Zero-Config Multi-AI Support

One setup works everywhere:

```bash
bash scripts/setup-amazonq.sh scan ~/Repos
bash scripts/setup-kilocode.sh scan ~/Repos
```

Now "pygubuai" works in Amazon Q, Kilo Code, Roo Code, and Cline. Switch tools freely without reconfiguration.

## Quick Start

```bash
# Install
git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI
pip install -e .

# Enable for your AI tools (one-time setup)
bash scripts/setup-amazonq.sh scan ~/Repos
bash scripts/setup-kilocode.sh scan ~/Repos
bash scripts/setup-roocode.sh scan ~/Repos
bash scripts/setup-cline.sh scan ~/Repos
```

Then in any AI assistant:

```
pygubuai create a todo app with add, delete, and list
pygubuai add a search bar to my todo app
pygubuai show my projects
```

No commands to memorize. No syntax to learn. Just natural conversation.

## Features

### Natural Language UI Creation

In any AI assistant:
```
pygubuai create a calculator with number pad and operations
pygubuai add a history panel to my calculator
pygubuai change the submit button to green
```

Supports 15+ widgets: buttons, entries, labels, dropdowns, sliders, tabs, tables, text areas, checkboxes, radio buttons, and more.

### Project Templates

```bash
pygubu-template myapp login      # Username/password form
pygubu-template myapp crud       # Create/Read/Update/Delete interface
pygubu-template myapp settings   # Tabbed settings dialog
```

### Legacy Code Migration

```bash
tkinter-to-pygubu old_app.py
```

Converts existing Tkinter code to Pygubu format. Preserves logic, modernizes UI structure.

### Visual-Code Sync

```bash
pygubu-ai-workflow watch myapp
```

Edit UI in Pygubu Designer. AI detects changes and updates Python code automatically.

### Multi-AI Support

Works with Amazon Q, Kilo Code, Roo Code, and Cline. One setup, all tools:

```bash
bash scripts/setup-amazonq.sh scan ~/Repos
bash scripts/setup-kilocode.sh scan ~/Repos
```

## Installation

### Prerequisites
- Python 3.9+
- [Pygubu](https://github.com/alejandroautalan/pygubu) and [Pygubu Designer](https://github.com/alejandroautalan/pygubu-designer)

### Recommended Method: pip install

**This is the preferred installation method:**

```bash
git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI
pip install -e .
```

Verify installation:
```bash
pygubu-create --version
pygubu-register list
```

### Enable Natural Language Trigger

One-time setup:

```bash
# Scan all projects
bash scripts/setup-amazonq.sh scan ~/Repos
bash scripts/setup-kilocode.sh scan ~/Repos
bash scripts/setup-roocode.sh scan ~/Repos
bash scripts/setup-cline.sh scan ~/Repos

# Or mark specific directory
bash scripts/setup-amazonq.sh mark /path/to/project

# Or mark PygubuAI repo only
bash scripts/setup-amazonq.sh self
```

See [MULTI_AI_SETUP.md](MULTI_AI_SETUP.md) for details.



### Development Setup

```bash
pip install -e ".[dev]"  # Install with dev dependencies
make test-fast           # Run fast tests (<1 min)
make test                # Run all tests
make test-coverage       # Run with coverage report
make lint                # Run linters
```



### Uninstall

```bash
pip uninstall pygubuai
```

## Commands

### Core Commands
| Command | Description |
|---------|-------------|
| `pygubu-create <name> '<desc>' [--dry-run]` | Create new project from description |
| `pygubu-template <name> <template>` | Create from template (login, crud, etc.) |
| `pygubu-register list` | Show all registered projects |
| `pygubu-register active <name>` | Set active project |
| `tkinter-to-pygubu <file>.py` | Convert tkinter to pygubu |
| `pygubu-ai-workflow watch <proj>` | Watch for UI changes |

### Advanced Commands
| Command | Description |
|---------|-------------|
| `pygubu-status [project]` | Check UI/code sync status |
| `pygubu-widgets list [--category]` | Browse widget library |
| `pygubu-theme <project> <theme>` | Apply ttk theme |
| `pygubu-preview <project> [--watch]` | Quick UI preview |
| `pygubu-validate <project>` | Check for issues |
| `pygubu-inspect <project> [--widget]` | Examine UI structure |
| `pygubu-snippet <widget> [text]` | Generate XML snippets |
| `pygubu-prompt <template> [project]` | AI prompt templates |
| `pygubu-batch <command> [args]` | Batch operations |
| `pygubu-export <project>` | Export to standalone file |

## Documentation

All documentation is in the [docs/](docs/) folder:

- **[User Guide](docs/USER_GUIDE.md)** - Complete usage guide
- **[Feature Showcase](docs/FEATURE_SHOWCASE.md)** - All features with examples
- **[Multi-AI Setup](MULTI_AI_SETUP.md)** - Configure for Amazon Q, Kilo Code, Roo Code, Cline
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Architecture and API reference
- **[Security Guide](docs/SECURITY_GUIDE.md)** - Security best practices
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Architecture](ARCHITECTURE.md)** - System design
- **[Changelog](CHANGELOG.md)** - Version history
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Examples](examples/)** - Sample projects



## Examples

See [examples/](examples/) for 6 complete working applications:

1. **Number Game** - Beginner-friendly guessing game
2. **Todo App** - Task manager with dynamic lists
3. **Calculator** - Grid layout with operations
4. **Login Form** - Professional form with validation
5. **Settings Dialog** - Tabbed interface with multiple widgets
6. **Data Viewer** - Advanced table with search and filtering

Each example includes `.ui` file, Python code, and detailed README.

### Running Examples

```bash
# Install pygubu first
pip install pygubu

# Run any example
./run_example.sh calculator
./run_example.sh todo_app
./run_example.sh login_form

# Or manually
cd examples/calculator && python3 calculator.py
```

See [examples/RUN_EXAMPLES.md](examples/RUN_EXAMPLES.md) for detailed instructions.

## Architecture

PygubuAI creates a continuous feedback loop:

```
You: "pygubuai create a login form"
  |
  v
AI detects trigger -> Loads Pygubu context -> Generates .ui + .py files
  |
  v
You edit in Pygubu Designer (visual drag-and-drop)
  |
  v
Watch mode detects changes -> AI updates Python code
  |
  v
You: "pygubuai add validation logic"
  |
  v
AI modifies Python, preserves UI structure
```

**Key Components:**

1. **Trigger Word**: "pygubuai" activates specialized mode in any AI assistant
2. **Global Registry**: `~/.pygubu-registry.json` tracks all projects across all AI sessions
3. **Project Markers**: `.pygubuai` files mark GUI project directories
4. **Context Injection**: Tool-specific prompts (`.amazonq/`, `.kilocode/`, etc.) teach AI Pygubu patterns
5. **Workflow Tracking**: `.pygubu-workflow.json` maintains change history per project

**Why It Works:**

Traditional approach: You adapt to tools.
PygubuAI approach: Tools adapt to you.

AI becomes your GUI development partner, not just a code generator. It remembers your projects, understands visual design tools, and maintains context across sessions and AI platforms.

## Requirements

### Runtime
- Python 3.9+
- pygubu >= 0.39
- pygubu-designer >= 0.42
- tkinter (usually included with Python)
- rich >= 13.0
- pydantic >= 2.0
- filelock >= 3.0

### Development
- pytest >= 7.0
- pytest-cov >= 4.0
- coverage >= 7.0
- black >= 23.0
- flake8 >= 6.0
- mypy >= 1.0

```bash
pip install -e ".[dev]"  # Install with dev dependencies
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repo
2. Create feature branch
3. Add tests for your changes
4. Submit PR

## License

MIT License - See [LICENSE](LICENSE)

PygubuAI is built on top of [Pygubu](https://github.com/alejandroautalan/pygubu) by Alejandro Autalán, also MIT licensed.

## Credits

- **Pygubu**: Alejandro Autalán - https://github.com/alejandroautalan/pygubu
- **PygubuAI Tools**: AI-assisted development workflow extensions

## Links

- [Pygubu](https://github.com/alejandroautalan/pygubu)
- [Pygubu Designer](https://github.com/alejandroautalan/pygubu-designer)

---

**Made for seamless AI-human collaboration in Tkinter development**
