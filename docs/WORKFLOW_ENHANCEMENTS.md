# Workflow Enhancements

## Overview

The workflow module has been enhanced with three key improvements:

1. **Per-file hash tracking** - Tracks each UI file independently
2. **Configurable watch interval** - Customize polling frequency
3. **File pattern support** - Watch multiple file types

## Per-File Hash Tracking

Previously, the workflow tracked a single hash for all files, making it impossible to identify which specific file changed in multi-file projects.

**Now:** Each file is tracked independently in `file_hashes` dictionary.

```json
{
  "file_hashes": {
    "main.ui": "abc123...",
    "dialog.ui": "def456...",
    "settings.ui": "ghi789..."
  }
}
```

**Benefit:** Precise change detection - know exactly which file changed.

## Configurable Watch Interval

**Environment Variable:**
```bash
export PYGUBUAI_WATCH_INTERVAL=5.0  # Check every 5 seconds
pygubu-ai-workflow watch myapp
```

**Command Line:**
```bash
pygubu-ai-workflow watch myapp --interval 1.0  # Check every second
```

**Default:** 2.0 seconds

**Use Cases:**
- Fast iteration: `--interval 0.5`
- Battery saving: `--interval 10.0`
- Network drives: `--interval 5.0`

## File Pattern Support

Watch multiple file types beyond just `*.ui` files.

**Environment Variable:**
```bash
export PYGUBUAI_WATCH_PATTERNS="*.ui,*.xml,*.glade"
pygubu-ai-workflow watch myapp
```

**Command Line:**
```bash
pygubu-ai-workflow watch myapp --patterns "*.ui,*.xml"
```

**Default:** `*.ui`

**Use Cases:**
- Glade migration: `--patterns "*.ui,*.glade"`
- XML configs: `--patterns "*.ui,*.xml"`
- Custom formats: `--patterns "*.ui,*.custom"`

## Examples

### Fast Development Mode
```bash
pygubu-ai-workflow watch myapp --interval 0.5
```

### Multi-Format Project
```bash
export PYGUBUAI_WATCH_PATTERNS="*.ui,*.xml"
pygubu-ai-workflow watch myapp
```

### Battery-Efficient Mode
```bash
pygubu-ai-workflow watch myapp --interval 10.0
```

## Migration

Existing `.pygubu-workflow.json` files are automatically upgraded:
- Old `ui_hash` field is preserved for compatibility
- New `file_hashes` dictionary is added
- No manual migration needed

## Testing

New test coverage includes:
- `TestMultiFileTracking` - Per-file hash tracking
- `TestConfigurableWatch` - Environment variables and CLI args

Run tests:
```bash
python3 tests/test_workflow.py
```
