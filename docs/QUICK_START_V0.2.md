# PygubuAI v0.2 Quick Start Guide

Quick reference for new features in PygubuAI v0.2.

## 🎨 Interactive Mode

Create projects with guided prompts:

```bash
pygubu-create --interactive
```

Prompts you for:
- Project name
- Description
- Template selection
- Git initialization

## 🔍 Search Projects

Find projects by name, description, or tags:

```bash
# Search by keyword
pygubu-register search "login"
pygubu-register search "production"

# List with full metadata
pygubu-register list --metadata
```

## 🏷️ Project Metadata

Add metadata when creating or registering projects:

```bash
# Create with metadata
pygubu-create myapp "login form" \
  --tags "web,production" \
  --git

# Register with metadata
pygubu-register add /path/to/project \
  --description "My application" \
  --tags "web,production"
```

## 👁️ Dry-Run Mode

Preview operations without making changes:

```bash
# Preview project creation
pygubu-create myapp "login form" --dry-run

# Shows what would be created without actually creating files
```

## 🔧 Git Integration

Automatic git repository initialization:

```bash
# Create project with git
pygubu-create myapp "login form" --git
```

Creates:
- Git repository
- .gitignore file (Python/Tkinter optimized)
- Initial commit

## 🚀 Combined Usage

Use multiple features together:

```bash
# Interactive with git
pygubu-create --interactive --git

# Create with all options
pygubu-create myapp "login form" \
  --git \
  --tags "web,auth" \
  --template login

# Dry-run before committing
pygubu-create myapp "complex app" --dry-run
# Review output, then run without --dry-run
pygubu-create myapp "complex app" --git
```

## 📊 Project Management

Enhanced project management:

```bash
# Add project with full metadata
pygubu-register add . \
  --description "User authentication system" \
  --tags "production,security"

# Search your projects
pygubu-register search "auth"

# View detailed project list
pygubu-register list --metadata
```

## 🔄 Workflow Example

Complete workflow with new features:

```bash
# 1. Create project interactively with git
pygubu-create --interactive --git

# 2. Search for similar projects
pygubu-register search "login"

# 3. Set as active project
pygubu-register active myapp

# 4. Start development
cd myapp
python myapp.py
```

## 📝 Quick Reference

| Feature | Command | Description |
|---------|---------|-------------|
| Interactive | `--interactive` | Guided project creation |
| Dry-run | `--dry-run` | Preview without creating |
| Git init | `--git` | Initialize git repository |
| Tags | `--tags "a,b"` | Add project tags |
| Search | `search "query"` | Find projects |
| Metadata | `--metadata` | Show full project info |

## 🆕 What's New in v0.2

- ✅ Interactive CLI mode
- ✅ Project metadata (description, tags, timestamps)
- ✅ Search functionality
- ✅ Dry-run mode
- ✅ Git integration
- ✅ Auto-registration
- ✅ 40+ new tests

## 📚 More Information

- [Full User Guide](USER_GUIDE.md)
- [Implementation Details](ENHANCEMENTS_IMPLEMENTED.md)
- [Enhancement Roadmap](ENHANCEMENTS.md)

---

*PygubuAI v0.2 - Making Tkinter development easier with AI*
