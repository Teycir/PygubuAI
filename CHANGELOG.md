# Changelog

All notable changes to PygubuAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [0.1.0] - 2024-10-30

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

[0.2.0]: https://github.com/yourusername/pygubuai/releases/tag/v0.2.0
[0.1.0]: https://github.com/yourusername/pygubuai/releases/tag/v0.1.0
[0.0.1]: https://github.com/yourusername/pygubuai/releases/tag/v0.0.1
