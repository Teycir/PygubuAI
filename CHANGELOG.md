# Changelog

All notable changes to PygubuAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-XX (In Progress)

### Added
- **Package Structure**: Proper Python package with src layout
- **Error Handling**: Custom exception hierarchy with helpful messages
- **Thread Safety**: File locking for registry operations
- **Logging**: Python logging framework throughout
- **Version Management**: `--version` flag for all CLI commands
- **Help System**: `--help` flag for all CLI commands
- **Type Hints**: Type annotations for better IDE support
- **Development Tools**: CONTRIBUTING.md, .editorconfig
- **New Modules**: register.py, workflow.py in package
- **Additional Tests**: test_register.py, test_workflow.py

### Changed
- Migrated `pygubu-register` to package module
- Migrated `pygubu-template` to package module
- Migrated `pygubu-ai-workflow` to package module
- Updated all CLI scripts to use package modules
- Enhanced error messages with suggestions
- Improved input validation and sanitization

### Technical
- Thread-safe Registry class with fcntl locking
- Custom exception classes (ProjectNotFoundError, InvalidProjectError)
- Proper package entry points in pyproject.toml
- Development dependencies in optional [dev] group
- Comprehensive test coverage for new modules

## [0.1.0] - 2025-01-XX

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

[0.1.0]: https://github.com/yourusername/pygubuai/releases/tag/v0.1.0
[0.0.1]: https://github.com/yourusername/pygubuai/releases/tag/v0.0.1
