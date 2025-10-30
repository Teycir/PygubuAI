# TODO - PygubuAI Improvements

## Phase 1: Core Fixes (DONE ✅)
- [x] Restructure as proper Python package (src/pygubuai/)
- [x] Add error handling and validation
- [x] Input sanitization for project names
- [x] Thread-safe registry with file locking
- [x] Logging framework
- [x] Version management (--version flag)
- [x] Uninstall script
- [x] Update CI to use pytest
- [x] Fix pyproject.toml for proper installation

## Phase 2: Migrate Remaining Tools (DONE ✅)
- [x] Migrate `pygubu-register` to package
- [x] Migrate `pygubu-template` to package
- [x] Migrate `pygubu-ai-workflow` to package
- [x] Add --version to all commands
- [x] Add --help to all commands
- [x] Update shell scripts to use package modules
- [x] Add tests for new modules
- [ ] Migrate `tkinter-to-pygubu` to package (deferred)

## Phase 3: Testing (IN PROGRESS)
- [x] Update tests for new package structure
- [x] Add tests for register module
- [x] Add tests for workflow module
- [x] All 30 tests passing
- [ ] Add integration tests
- [ ] Test pip installation in CI
- [ ] Test uninstall script
- [ ] Add pre-commit hooks

## Phase 4: Documentation (TODO)
- [ ] Consolidate docs (5 files → 1-2)
- [ ] Update README with new installation
- [ ] Add API documentation
- [ ] Add troubleshooting guide

## Phase 5: Type Safety (TODO)
- [ ] Add type hints to all modules
- [ ] Add mypy configuration
- [ ] Run mypy in CI

## Phase 6: Polish (TODO)
- [ ] Better error messages
- [ ] Progress indicators for long operations
- [ ] Colored output
- [ ] Shell completion scripts
- [ ] Windows support testing

## Quick Wins (Can do anytime)
- [x] Add .editorconfig
- [x] Add CONTRIBUTING.md with setup instructions
- [ ] Add .pre-commit-config.yaml
- [ ] Add issue templates
- [ ] Add PR template
- [ ] Add security policy
- [ ] Add GitHub Actions badge to README
