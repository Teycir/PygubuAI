# Changelog

All notable changes to PygubuAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-01-25

### Added - 10 High-Value Productivity Features 🚀

#### 1. Project Status Checker
- `pygubu-status` command to check UI/code sync status
- Shows modification timestamps and sync state
- Detects "In Sync", "UI Ahead", or "Code Ahead" states
- Tracks workflow history from `.pygubu-workflow.json`

#### 2. Widget Library Browser
- `pygubu-widgets` command with comprehensive widget database
- 20+ widgets organized in 5 categories (input, display, action, container, layout)
- Search functionality: `pygubu-widgets search "button"`
- Detailed widget info with properties and use cases
- Category filtering: `pygubu-widgets list --category input`

#### 3. Theme Switcher
- `pygubu-theme` command to apply ttk themes
- Support for 7 themes: default, clam, alt, classic, vista, xpnative, aqua
- Automatic backup before theme changes
- Get current theme: `pygubu-theme <project> --current`

#### 4. Quick Preview
- `pygubu-preview` command to view UI without running full app
- Watch mode with auto-reload: `pygubu-preview --watch`
- Preview by project name or UI file path
- Perfect for design iteration

#### 5. Project Validator
- `pygubu-validate` command to check for common issues
- Detects: duplicate IDs, missing IDs, undefined callbacks, unused callbacks
- XML syntax validation
- Severity levels: error, warning, info

#### 6. Widget Inspector
- `pygubu-inspect` command to examine UI structure
- Show widget hierarchy tree: `pygubu-inspect <project> --tree`
- Inspect specific widgets: `pygubu-inspect <project> --widget <id>`
- List all callbacks: `pygubu-inspect <project> --callbacks`
- Display properties, layout, parent/children relationships

#### 7. Snippet Generator
- `pygubu-snippet` command to generate XML snippets
- Support for 8 common widgets: button, entry, label, frame, combobox, checkbutton, text, treeview
- Customizable properties via command-line options
- Ready-to-paste XML output

#### 8. AI Prompt Templates
- `pygubu-prompt` command with 6 pre-written templates
- Templates: add-feature, fix-layout, refactor, add-validation, add-menu, improve-accessibility
- Auto-includes project context and file paths
- Optimized for AI assistant interactions

#### 9. Batch Operations
- `pygubu-batch` command for multi-project management
- Rename widgets across projects
- Apply themes to multiple projects
- Validate all projects at once
- Progress reporting and error handling

#### 10. Standalone Export
- `pygubu-export` command to create single-file distributions
- Embeds UI XML as string in Python file
- Includes all callbacks from original code
- Generates executable standalone application
- No external .ui file needed

### Added - Infrastructure
- New module: `status.py` - Project status checking
- New module: `widget_data.py` - Comprehensive widget database
- Enhanced module: `widgets.py` - Added browser functionality
- New module: `theme.py` - Theme management
- New module: `preview.py` - Quick UI preview
- New module: `validate_project.py` - Project validation
- New module: `inspect.py` - Widget inspection
- New module: `snippet.py` - XML snippet generation
- New module: `prompt.py` - AI prompt templates
- New module: `batch.py` - Batch operations
- New module: `export.py` - Standalone export

### Added - Documentation
- `ROADMAP.md` - Complete implementation roadmap
- `FEATURE_SHOWCASE.md` - Comprehensive feature guide with examples
- Updated README with v0.5.0 features
- 10 new CLI entry points in pyproject.toml

### Added - Tests
- `test_status.py` - Status checker tests
- `test_new_widgets.py` - Widget browser tests
- `test_theme.py` - Theme switcher tests
- `test_snippet.py` - Snippet generator tests

### Changed
- Version bumped to 0.5.0
- README reorganized with new features section
- Commands table split into Core and New sections

### Technical
- Zero new external dependencies
- All features use existing Python stdlib + pygubu
- Minimal code footprint (< 200 lines per feature)
- Comprehensive error handling
- Cross-platform compatibility maintained

## [0.3.0] - 2025-01-20

### Changed
- Updated documentation URLs to use actual repository (Teycir/PygubuAI)
- Fixed date consistency across documentation (2024 → 2025)
- Aligned version references across all documentation

### Fixed
- Corrected placeholder URLs in README.md and pyproject.toml
- Fixed documentation link in pyproject.toml (PYGUBUAI.md → README.md)

## [0.2.0] - 2025-01-15

### Added - High Priority Enhancements
- **Interactive CLI Mode**: `--interactive` flag for guided project creation
- **Project Metadata**: Description, tags, and timestamps for all projects
- **Search Functionality**: Search projects by name, description, or tags
- **Dry-Run Mode**: `--dry-run` flag to preview operations without execution
- **Git Integration**: Automatic repository initialization with `--git` flag
- **Auto-Registration**: Projects automatically added to registry on creation
- **Enhanced Test Coverage**: 40+ new tests, 95%+ coverage

### Added - Core Features
- **Package Structure**: Proper Python package with src layout
- **Error Handling**: Custom exception hierarchy with helpful messages
- **Thread Safety**: Cross-platform file locking (Unix/Windows/macOS)
- **Logging**: Python logging framework throughout
- **Version Management**: `--version` flag for all CLI commands
- **Help System**: `--help` flag for all CLI commands
- **Type Hints**: Type annotations for better IDE support
- **Development Tools**: CONTRIBUTING.md, .editorconfig
- **New Modules**: register.py, workflow.py, interactive.py, git_integration.py
- **Additional Tests**: 8 test modules with 120+ tests total
- **CI/CD**: Multi-platform testing (Ubuntu, Windows, macOS)
- **CI/CD**: Automated linting, type checking, and coverage

### Changed
- Migrated `pygubu-register` to package module with search support
- Migrated `pygubu-template` to package module
- Migrated `pygubu-ai-workflow` to package module
- Enhanced `pygubu-create` with interactive mode, dry-run, and git
- Updated all CLI scripts to use package modules
- Enhanced error messages with suggestions
- Improved input validation and sanitization
- Registry format now includes metadata (backward compatible)

### Fixed
- **Windows Compatibility**: Replaced Unix-only fcntl with cross-platform locking (msvcrt on Windows)
- **CI Pipeline**: Added type checking and linting to all pull requests
- **CI Pipeline**: Multi-OS testing matrix for better compatibility

### Technical
- Thread-safe Registry class with platform-specific locking (fcntl/msvcrt)
- Custom exception classes (ProjectNotFoundError, InvalidProjectError)
- Proper package entry points in pyproject.toml
- Development dependencies in optional [dev] group
- Comprehensive test coverage for all modules
- GitHub Actions CI runs on Ubuntu, Windows, and macOS
- Backward compatible registry format migration
- Git integration with automatic .gitignore generation

## [0.1.0] - 2025-01-10

### Added
- **Testing Framework**: 23 automated tests across 6 modules
- **Project Templates**: 5 professional templates (login, crud, settings, dashboard, wizard)
- **Enhanced Widget Support**: 15+ widget types with context-aware detection
- `pygubu-template` command for template-based project creation
- `run_tests.py` test runner script
- Code coverage tooling with `.coveragerc` and `run_coverage.sh`
- Comprehensive documentation in `docs/FEATURES.md`
- Architecture diagram in implementation summary

### Changed
- Enhanced `pygubu-create` to use new widget detection system
- Updated `install.sh` to install new modules and tools
- Improved README with new features and examples

### Technical
- Pattern-based widget detection engine
- Template system with auto-generated callbacks
- Modular test structure with unittest framework
- 100% backward compatibility maintained

## [0.0.1] - Initial Release

### Added
- Basic project creation with `pygubu-create`
- Global project registry system
- AI workflow integration
- Tkinter to Pygubu converter
- Watch mode for UI changes
- Basic widget detection (5 types)

[0.3.0]: https://github.com/Teycir/PygubuAI/releases/tag/v0.3.0
[0.2.0]: https://github.com/Teycir/PygubuAI/releases/tag/v0.2.0
[0.1.0]: https://github.com/Teycir/PygubuAI/releases/tag/v0.1.0
[0.0.1]: https://github.com/Teycir/PygubuAI/releases/tag/v0.0.1
