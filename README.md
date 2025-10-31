# PygubuAI

[![CI](https://github.com/Teycir/PygubuAI/workflows/CI/badge.svg)](https://github.com/Teycir/PygubuAI/actions)
[![codecov](https://codecov.io/gh/Teycir/PygubuAI/branch/main/graph/badge.svg)](https://codecov.io/gh/Teycir/PygubuAI)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered workflow tools for [Pygubu](https://github.com/alejandroautalan/pygubu) - Build Tkinter UIs with natural language and visual design.

## What is PygubuAI?

PygubuAI adds AI-assisted development tools on top of Pygubu, enabling:
- Natural language UI creation
- Seamless visual-to-code synchronization  
- Global project management across all AI chats
- Automatic tkinter-to-pygubu conversion
- Project tracking and context awareness

## Quick Start

```bash
# Clone
git clone https://github.com/Teycir/PygubuAI.git
cd PygubuAI

# Install
./install.sh

# Create your first AI-powered project
pygubu-create myapp 'login form with username and password'
```

## Features

### Natural Language UI Creation
```bash
pygubu-create todo 'todo app with entry, button, and list'
```
Describe your UI in plain English, get a working Tkinter app!

**NEW:** Enhanced with 15+ widget types including dropdowns, sliders, tabs, and more!

### Project Templates
```bash
pygubu-template myapp login    # Login form
pygubu-template myapp crud     # CRUD interface
pygubu-template myapp settings # Settings dialog
```
Instant professional UIs from pre-built templates!

### Global Project Registry
```bash
pygubu-register scan ~/projects  # Find all pygubu projects
pygubu-register active myapp     # Set active project
```
Access any project from any AI chat session.

### Convert Existing Code
```bash
tkinter-to-pygubu old_app.py
```
Migrate legacy tkinter code to pygubu format.

### AI Chat Integration
In ANY conversation with your AI assistant:
- "Add a button to my project"
- "Change the color scheme"
- "Show my pygubu projects"

Use `@pygubu-context` prompt for automatic context loading.

### Watch Mode
```bash
pygubu-ai-workflow watch myapp
```
Auto-detects UI changes and prompts for code sync.

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

### Alternative: Shell Script (DEPRECATED)

**⚠️ This method is deprecated and will be removed in v0.5.0**

Only use if pip installation doesn't work on your system:

```bash
./install.sh  # Installs to ~/bin/ or /usr/local/bin/
```

**Migration:** Switch to `pip install -e .` before v0.5.0

### Development Setup

```bash
pip install -e ".[dev]"  # Install with dev dependencies
make test-fast           # Run fast tests (<1 min)
make test                # Run all tests
make test-coverage       # Run with coverage report
make lint                # Run linters
```

**Testing:** See [Testing Quick Ref](docs/TESTING_QUICK_REF.md) for testing guide.

### Uninstall

```bash
pip uninstall pygubuai  # For pip install (recommended)
./uninstall.sh          # For shell script install
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

### New in v0.5.0 🎉
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

### Getting Started
- **[Onboarding](docs/ONBOARDING.md)** - Get started in 15 minutes
- **[Quick Status](docs/QUICK_STATUS.md)** - Project status at a glance
- **[Feature Showcase](docs/FEATURE_SHOWCASE.md)** - v0.5.0 features with examples
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage guide

### Development
- **[Implementation Plan](docs/IMPLEMENTATION_PLAN.md)** - Detailed tasks and timelines
- **[Progress Tracker](docs/PROGRESS_TRACKER.md)** - Day-to-day tracking
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Architecture and API reference
- **[Developer Quick Ref](docs/DEVELOPER_QUICK_REF.md)** - Fast lookup for common tasks
- **[Testing Quick Ref](docs/TESTING_QUICK_REF.md)** - Testing guide and commands

### Technical
- **[Library Integrations](docs/LIBRARY_INTEGRATIONS.md)** - Rich, Pydantic, SQLAlchemy guide
- **[Documentation Map](docs/DOCS_MAP.md)** - Visual guide to all docs

### Project Info
- **[Roadmap](ROADMAP.md)** - Long-term plan (v0.5-v1.0)
- **[Architecture](ARCHITECTURE.md)** - System design and module structure
- **[Changelog](CHANGELOG.md)** - Version history
- **[Contributing](CONTRIBUTING.md)** - How to contribute
- **[Examples](examples/)** - Sample projects

## What's New 🚀

### v0.5.1 - Rich Terminal UI (In Progress)

**Beautiful CLI Output:**
- ✅ Colored status tables with Rich
- ✅ Formatted widget browser
- ✅ Enhanced inspect command
- 🔄 Progress bars for batch operations
- 🔄 Colored validation results

**New Dependencies:**
- `rich>=13.0` - Beautiful terminal output
- `pydantic>=2.0` - Data validation (models ready)

### v0.5.0 - 10 High-Value Productivity Features

1. **Project Status** - Check UI/code sync status instantly
2. **Widget Browser** - Discover 20+ widgets with categories
3. **Theme Switcher** - Apply ttk themes with one command
4. **Quick Preview** - View UI without running full app
5. **Project Validator** - Find issues before they break
6. **Widget Inspector** - Examine UI structure and properties
7. **Snippet Generator** - Generate XML for quick insertion
8. **AI Prompts** - Pre-written templates for common tasks
9. **Batch Operations** - Manage multiple projects efficiently
10. **Standalone Export** - Bundle UI into single Python file

**See [Feature Showcase](docs/FEATURE_SHOWCASE.md) for detailed examples!**

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
- rich >= 13.0 (v0.5.1+)
- pydantic >= 2.0 (v0.5.1+)

### Development (Optional)
- coverage >= 7.0 (for code coverage)

```bash
pip install -e ".[dev]"  # Install with dev dependencies
pip install -e ".[db]"   # Install with database support (v0.7.0+)
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
