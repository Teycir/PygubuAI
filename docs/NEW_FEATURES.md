# PygubuAI New Features Guide

## Quick Reference for Recent Improvements

### 1. Environment Variable Configuration

Control PygubuAI behavior without modifying code:

```bash
# Custom registry location
export PYGUBUAI_REGISTRY_PATH=/custom/path/registry.json

# Custom AI context directory
export PYGUBUAI_AI_CONTEXT_DIR=/custom/prompts

# Debug logging
export PYGUBUAI_LOG_LEVEL=DEBUG

# Use as normal
pygubu-create myapp "login form"
```

**Available Variables:**
- `PYGUBUAI_REGISTRY_PATH` - Override registry file location
- `PYGUBUAI_AI_CONTEXT_DIR` - Override AI context directory
- `PYGUBUAI_LOG_LEVEL` - Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### 2. User Configuration File

Create `~/.pygubuai/config.json` to customize settings:

```json
{
  "registry_path": "~/my-projects/registry.json",
  "ai_context_dir": "~/.my-ai/prompts",
  "default_window_size": {
    "width": 800,
    "height": 600
  },
  "default_padding": 30
}
```

**Configuration Priority:**
1. Environment variables (highest)
2. User config file
3. Default values (lowest)

### 3. Custom Templates

Create your own templates in `~/.pygubuai/templates/`:

```bash
# Create template directory
mkdir -p ~/.pygubuai/templates

# Create custom template
cat > ~/.pygubuai/templates/dashboard.json << 'EOF'
{
  "description": "Dashboard with metrics and charts",
  "widgets": [
    {
      "type": "label",
      "text": "Dashboard",
      "id": "title_label"
    },
    {
      "type": "labelframe",
      "text": "Metrics",
      "id": "metrics_frame"
    },
    {
      "type": "progressbar",
      "text": "",
      "id": "progress_bar"
    },
    {
      "type": "button",
      "text": "Refresh",
      "id": "refresh_btn",
      "properties": {
        "command": "on_refresh"
      }
    }
  ],
  "callbacks": ["on_refresh"]
}
EOF

# Use your custom template
pygubu-template myapp dashboard
```

**Template Format:**
- `description` (required): Template description
- `widgets` (required): Array of widget definitions
- `callbacks` (optional): Array of callback function names

**Widget Definition:**
- `type` (required): Widget type (label, button, entry, etc.)
- `text` (optional): Widget text/label
- `id` (required): Unique widget identifier
- `properties` (optional): Additional widget properties

### 4. Structured Logging

Enable detailed logging for debugging:

```bash
# Enable debug logging
export PYGUBUAI_LOG_LEVEL=DEBUG

# Run commands with detailed output
pygubu-create myapp "test app"
pygubu-ai-workflow watch myapp
```

**Log Levels:**
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

**Programmatic Usage:**
```python
from pygubuai.logging_config import get_logger

logger = get_logger(__name__)
logger.debug("Detailed debug info")
logger.info("User-facing message")
logger.warning("Warning condition")
logger.error("Error occurred")
```

### 5. Programmatic API

Use PygubuAI features in your own Python code:

#### Configuration
```python
from pygubuai.config import Config

config = Config()

# Get values with defaults
registry_path = config.get("registry_path")
custom_value = config.get("custom_key", "default_value")

# Modify and save
config.config["new_setting"] = "value"
config.save()
```

#### Template Registry
```python
from pygubuai.template_discovery import get_template_registry

registry = get_template_registry()

# List all templates (built-in + user)
templates = registry.list_templates()
for name, description, source in templates:
    print(f"{name}: {description} ({source})")

# Get specific template
template = registry.get_template("login")

# Register new template programmatically
custom_template = {
    "description": "My custom template",
    "widgets": [
        {"type": "label", "text": "Hello", "id": "hello_label"}
    ],
    "callbacks": []
}
registry.register_template("custom", custom_template)

# Save template to user directory
registry.save_user_template("mytemplate", custom_template)
```

#### Logging
```python
from pygubuai.logging_config import setup_logging, get_logger

# Setup with custom level
logger = setup_logging("myapp", level=logging.DEBUG)

# Or use convenience function
logger = get_logger(__name__)
logger.info("Application started")
```

### 6. Enhanced Error Handling

Better error messages with context:

```bash
# Before
ERROR: Project not found

# After
ERROR: Project 'myapp' not found. Available: login, dashboard, settings
```

All errors now include:
- Clear error description
- Contextual information
- Suggestions for resolution
- Proper logging with stack traces (in DEBUG mode)

## Examples

### Example 1: Development Environment Setup

```bash
# Set up development environment
export PYGUBUAI_LOG_LEVEL=DEBUG
export PYGUBUAI_REGISTRY_PATH=~/dev/pygubu-registry.json

# Create custom templates directory
mkdir -p ~/.pygubuai/templates

# Create project
pygubu-create devapp "development test app"
```

### Example 2: Production Environment

```bash
# Production settings
export PYGUBUAI_REGISTRY_PATH=/var/lib/pygubu/registry.json
export PYGUBUAI_LOG_LEVEL=WARNING

# Use in production
pygubu-create prodapp "production app"
```

### Example 3: Custom Template Workflow

```bash
# Create template
cat > ~/.pygubuai/templates/report.json << 'EOF'
{
  "description": "Report viewer with filters",
  "widgets": [
    {"type": "label", "text": "Report Viewer", "id": "title"},
    {"type": "combobox", "text": "", "id": "filter_combo"},
    {"type": "treeview", "text": "", "id": "report_table"},
    {"type": "button", "text": "Export", "id": "export_btn",
     "properties": {"command": "on_export"}}
  ],
  "callbacks": ["on_export"]
}
EOF

# Use template
pygubu-template myreport report

# Verify
cd myreport
python3 myreport.py
```

### Example 4: CI/CD Integration

```yaml
# .github/workflows/build.yml
env:
  PYGUBUAI_REGISTRY_PATH: ${{ github.workspace }}/registry.json
  PYGUBUAI_LOG_LEVEL: INFO

steps:
  - name: Create UI
    run: |
      pygubu-create testapp "test application"
      cd testapp
      python3 testapp.py --test
```

## Migration from Previous Versions

All new features are backward compatible. No changes required to existing code.

**Optional Upgrades:**
1. Replace direct Config.DEFAULT access with Config.get()
2. Use get_logger() instead of logging.getLogger()
3. Use template registry instead of direct TEMPLATES access

**Before:**
```python
from pygubuai.config import Config
registry_path = Config.DEFAULT["registry_path"]
```

**After:**
```python
from pygubuai.config import Config
config = Config()
registry_path = config.get("registry_path")
```

## Troubleshooting

### Debug Mode
```bash
export PYGUBUAI_LOG_LEVEL=DEBUG
pygubu-create myapp "test app"
```

### Check Configuration
```python
from pygubuai.config import Config
config = Config()
print(config.config)
```

### List Available Templates
```python
from pygubuai.template_discovery import get_template_registry
registry = get_template_registry()
for name, desc, source in registry.list_templates():
    print(f"{name}: {desc} ({source})")
```

### Verify Environment Variables
```bash
env | grep PYGUBUAI
```

## Performance Notes

- Template discovery runs once at startup
- Configuration is cached after first load
- Logging overhead is minimal at INFO level
- User templates are validated on load

## Security Considerations

- User templates are validated before use
- Configuration files should have appropriate permissions
- Environment variables take precedence for security
- No credentials should be stored in config files

## Further Reading

- [User Guide](USER_GUIDE.md) - Complete usage guide
- [Developer Guide](DEVELOPER_GUIDE.md) - API reference and architecture
- [Improvement Plan](../IMPROVEMENT_PLAN.md) - Technical details
- [Improvements Summary](../IMPROVEMENTS_SUMMARY.md) - Complete changelog

## Support

For issues or questions:
1. Check logs with `PYGUBUAI_LOG_LEVEL=DEBUG`
2. Verify configuration with `Config().config`
3. List templates with template registry
4. Review documentation in `docs/`
