# PygubuAI 🤖

AI-powered workflow tools for [Pygubu](https://github.com/alejandroautalan/pygubu) - Build Tkinter UIs with natural language and visual design.

## What is PygubuAI?

PygubuAI adds AI-assisted development tools on top of Pygubu, enabling:
- 🗣️ Natural language UI creation
- 🔄 Seamless visual-to-code synchronization  
- 🌍 Global project management across all AI chats
- 🔧 Automatic tkinter-to-pygubu conversion
- 📊 Project tracking and context awareness

## Quick Start

```bash
# Clone
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai

# Install
./install.sh

# Create your first AI-powered project
pygubu-create myapp 'login form with username and password'
```

## Features

### 🎨 Natural Language UI Creation
```bash
pygubu-create todo 'todo app with entry, button, and list'
```
Describe your UI in plain English, get a working Tkinter app!

**NEW:** Enhanced with 15+ widget types including dropdowns, sliders, tabs, and more!

### 🎯 Project Templates
```bash
pygubu-template myapp login    # Login form
pygubu-template myapp crud     # CRUD interface
pygubu-template myapp settings # Settings dialog
```
Instant professional UIs from pre-built templates!

### 🌍 Global Project Registry
```bash
pygubu-register scan ~/projects  # Find all pygubu projects
pygubu-register active myapp     # Set active project
```
Access any project from any AI chat session.

### 🔄 Convert Existing Code
```bash
tkinter-to-pygubu old_app.py
```
Migrate legacy tkinter code to pygubu format.

### 🤖 AI Chat Integration
In ANY conversation with your AI assistant:
- "Add a button to my project"
- "Change the color scheme"
- "Show my pygubu projects"

Use `@pygubu-context` prompt for automatic context loading.

### 👁️ Watch Mode
```bash
pygubu-ai-workflow watch myapp
```
Auto-detects UI changes and prompts for code sync.

## Installation

### Prerequisites
- Python 3.9+
- [Pygubu](https://github.com/alejandroautalan/pygubu) and [Pygubu Designer](https://github.com/alejandroautalan/pygubu-designer)

### Recommended: pip install
```bash
git clone https://github.com/yourusername/pygubuai.git
cd pygubuai
pip install -e .
```

### Alternative: Shell script install
```bash
./install.sh  # Installs to ~/bin/ or /usr/local/bin/
```

### Development Setup
```bash
make dev  # or: pip install -e ".[dev]"
make test
```

### Uninstall
```bash
./uninstall.sh  # For shell script install
pip uninstall pygubuai  # For pip install
```

## Commands

| Command | Description |
|---------|-------------|
| `pygubu-create <name> '<desc>'` | Create new project from description |
| `pygubu-template <name> <template>` | Create from template (login, crud, etc.) |
| `pygubu-template list` | List all available templates |
| `pygubu-register list` | Show all registered projects |
| `pygubu-register active <name>` | Set active project |
| `pygubu-register scan <dir>` | Auto-discover projects |
| `tkinter-to-pygubu <file>.py` | Convert tkinter to pygubu |
| `pygubu-ai-workflow watch <proj>` | Watch for UI changes |
| `python3 run_tests.py` | Run test suite |

## Documentation

### User Guides
- [Complete Documentation](PYGUBUAI.md) - Full user guide
- [Features Guide](docs/FEATURES.md) - Testing, Templates, Widgets
- [Quick Reference](pygubuai-quickref.txt) - Command cheat sheet
- [Demo Guide](DEMO.md) - Quick examples

### Developer Docs
- [Architecture](docs/ARCHITECTURE.md) - System design and diagrams
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Recent improvements
- [Changelog](CHANGELOG.md) - Version history

### Testing
```bash
# Run tests
make test

# Run with coverage
make coverage

# Lint code
make lint
```

## Examples

### Create a Calculator
```bash
pygubu-create calc 'calculator with number pad and display'
pygubu-register active calc
```

Then in AI chat: "Add memory functions"

### Convert Existing App
```bash
tkinter-to-pygubu legacy_app.py
pygubu-register add .
```

Then: "Modernize the UI with ttk widgets"

### Collaborative Design
```bash
# Terminal 1: Watch for changes
pygubu-ai-workflow watch myapp

# Terminal 2: Visual editing
pygubu-designer myapp/myapp.ui

# AI Chat: "I added a menu bar, update the code"
```

## How It Works

1. **Project Registry**: `~/.pygubu-registry.json` tracks all projects
2. **AI Context**: `~/.amazonq/prompts/pygubu-context.md` provides context to AI
3. **Workflow Tracking**: Each project has `.pygubu-workflow.json` for history
4. **Auto-sync**: Tools detect changes and prompt for updates

## Requirements

### Runtime
- Python 3.9+
- pygubu >= 0.39
- pygubu-designer >= 0.42
- tkinter (usually included with Python)

### Development (Optional)
- coverage >= 7.0 (for code coverage)

```bash
pip install -e ".[dev]"  # Install with dev dependencies
```

## Contributing

Contributions welcome! This project extends Pygubu with AI workflow tools.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

Quick start:
1. Fork the repo
2. Create feature branch
3. Add your tool/enhancement
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
- [Documentation](PYGUBUAI.md)

---

**Made with ❤️ for seamless AI-human collaboration in Tkinter development**
