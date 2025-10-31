# Library Integrations Guide

## Overview

PygubuAI integrates three powerful libraries to enhance functionality:

1. **Rich** - Beautiful terminal output
2. **Pydantic** - Data validation and type safety
3. **SQLAlchemy** - Database for scalability

---

## Rich Terminal UI

### What is Rich?

Rich is a Python library for beautiful terminal output with colors, tables, progress bars, and more.

### Features in PygubuAI

**Enhanced Commands:**
- `pygubu-status` - Colored status tables
- `pygubu-widgets` - Formatted widget browser
- `pygubu-inspect` - Rich callback tables
- `pygubu-batch` - Progress bars (coming soon)
- `pygubu-validate` - Colored validation results (coming soon)

### Examples

**Before (Plain Text):**
```
Project: myapp
Status: In Sync
UI Modified: 2024-01-15T10:30:00
Code Modified: 2024-01-15T10:30:01
```

**After (Rich):**
```
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Component     ┃ Value               ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Status        │ In Sync             │
│ UI Modified   │ 2024-01-15T10:30:00 │
│ Code Modified │ 2024-01-15T10:30:01 │
└───────────────┴─────────────────────┘
```

### Installation

Rich is automatically installed with PygubuAI v0.5.1+:

```bash
pip install -e .
```

### Fallback Behavior

If Rich is not available, commands gracefully fall back to plain text output. No functionality is lost.

---

## Pydantic Data Validation

### What is Pydantic?

Pydantic provides data validation using Python type hints, ensuring data integrity throughout the application.

### Models in PygubuAI

**Core Models:**

```python
from pygubuai.models import ProjectConfig, RegistryData, WorkflowData

# Project configuration with validation
project = ProjectConfig(
    name="myapp",
    path="/path/to/myapp",
    ui_file="myapp.ui",
    py_file="myapp.py"
)

# Registry data with active project validation
registry = RegistryData(
    projects={"myapp": "/path/to/myapp"},
    active="myapp"
)

# Workflow tracking
workflow = WorkflowData(
    project="myapp",
    history=[
        WorkflowHistory(
            timestamp="2024-01-15T10:30:00",
            action="create",
            description="Created project"
        )
    ]
)
```

### Benefits

1. **Type Safety**: Catch errors at runtime
2. **Validation**: Automatic data validation
3. **Serialization**: Easy JSON conversion
4. **Documentation**: Self-documenting code
5. **IDE Support**: Better autocomplete

### Usage in Code

```python
from pygubuai.models import ProjectConfig
from pydantic import ValidationError

try:
    project = ProjectConfig(
        name="myapp",
        path="/nonexistent/path"  # Will raise ValidationError
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Migration Status

- ✅ Models defined in `src/pygubuai/models.py`
- 🔄 Registry migration in progress
- 🔄 Workflow migration in progress
- 🔄 Config migration in progress

---

## SQLAlchemy Database

### What is SQLAlchemy?

SQLAlchemy is a powerful SQL toolkit and ORM for Python, enabling efficient database operations.

### Use Cases in PygubuAI

**1. Project Management**
- Store thousands of projects efficiently
- Fast queries and filtering
- Relationship tracking

**2. Template Marketplace**
- Store custom templates
- Version control
- Ratings and downloads
- Search functionality

**3. Analytics**
- Widget usage statistics
- Project complexity metrics
- Performance tracking
- Usage trends

### Database Schema

```sql
-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    path TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSON
);

-- Templates table
CREATE TABLE templates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    author TEXT,
    version TEXT,
    downloads INTEGER DEFAULT 0,
    rating REAL DEFAULT 0.0,
    content TEXT,
    created_at TIMESTAMP
);

-- Workflow events
CREATE TABLE workflow_events (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    timestamp TIMESTAMP,
    action TEXT,
    description TEXT
);

-- Analytics
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    metric_name TEXT,
    metric_value REAL,
    recorded_at TIMESTAMP
);
```

### Commands

```bash
# Initialize database
pygubu-db init

# Run migrations
pygubu-db migrate

# Backup database
pygubu-db backup

# Restore from backup
pygubu-db restore backup.db

# Database statistics
pygubu-db stats
```

### Template Marketplace

```bash
# Publish template
pygubu-template publish mytemplate

# Search templates
pygubu-template search "login form"

# Install template
pygubu-template install template-123

# Rate template
pygubu-template rate template-123 5
```

### Analytics

```bash
# Project analytics
pygubu-analytics project myapp

# Widget usage statistics
pygubu-analytics widgets

# Usage trends
pygubu-analytics trends

# Export analytics
pygubu-analytics export --format csv
```

### Installation

SQLAlchemy is optional and installed separately:

```bash
pip install -e ".[db]"
```

### Migration from JSON

Existing JSON-based projects are automatically migrated:

```bash
pygubu-db migrate --from-json
```

The migration:
1. Reads existing JSON files
2. Validates with Pydantic models
3. Inserts into database
4. Keeps JSON as backup

### Backward Compatibility

JSON files remain supported. The database is optional:

- Without database: Uses JSON files (current behavior)
- With database: Uses SQLAlchemy for better performance

---

## Integration Timeline

### v0.5.1 (Week 1) - Rich
- ✅ Rich dependency added
- ✅ Enhanced status command
- ✅ Enhanced widgets command
- ✅ Enhanced inspect command
- 🔄 Batch progress bars
- 🔄 Validation colors

### v0.6.0 (Week 2-3) - Pydantic
- ✅ Models defined
- 🔄 Registry migration
- 🔄 Workflow migration
- 🔄 Config migration
- 🔄 Export validation

### v0.7.0 (Week 4-7) - SQLAlchemy
- 🔄 Database infrastructure
- 🔄 Template marketplace
- 🔄 Analytics system
- 🔄 Migration tools

---

## Performance Impact

### Rich
- **Overhead**: Minimal (<5ms per command)
- **Benefit**: Better UX, no performance loss

### Pydantic
- **Overhead**: ~1-2ms per validation
- **Benefit**: Prevents data corruption, worth the cost

### SQLAlchemy
- **Overhead**: Initial connection ~10ms
- **Benefit**: 10-100x faster queries for large datasets
- **Comparison**:
  - JSON: O(n) for searches
  - SQLAlchemy: O(log n) with indexes

---

## Testing

### Rich Tests
```bash
# Test with Rich
pip install rich
make test

# Test without Rich
pip uninstall rich
make test
```

### Pydantic Tests
```bash
pytest tests/test_models.py -v
```

### SQLAlchemy Tests
```bash
pytest tests/test_database.py -v
```

---

## Troubleshooting

### Rich Not Working

**Problem**: No colored output

**Solution**:
```bash
# Check if Rich is installed
pip list | grep rich

# Reinstall if needed
pip install rich>=13.0
```

### Pydantic Validation Errors

**Problem**: ValidationError on existing data

**Solution**:
```bash
# Run migration script
python -m pygubuai.migrate_data

# Or manually fix data
pygubu-register validate
```

### Database Issues

**Problem**: Database locked or corrupted

**Solution**:
```bash
# Restore from backup
pygubu-db restore ~/.pygubuai/backups/latest.db

# Or rebuild from JSON
pygubu-db rebuild --from-json
```

---

## Best Practices

### Using Rich
- Always provide fallback for plain text
- Use consistent color scheme
- Don't overuse colors

### Using Pydantic
- Define models for all data structures
- Use validators for complex logic
- Handle ValidationError gracefully

### Using SQLAlchemy
- Use indexes for frequently queried fields
- Batch operations for better performance
- Regular backups

---

## Contributing

When adding new features:

1. **Rich**: Add colored output with fallback
2. **Pydantic**: Define models for new data
3. **SQLAlchemy**: Update schema and migrations

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## Resources

- [Rich Documentation](https://rich.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PygubuAI Architecture](../ARCHITECTURE.md)
