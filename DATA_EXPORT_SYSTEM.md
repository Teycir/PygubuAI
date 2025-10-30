# Data Export System - PygubuAI v0.6.1

## Overview

Add data export capabilities (PDF, CSV, JSON) to PygubuAI projects with simple commands and automatic UI integration.

## Features

### 1. Export Formats
- **PDF** - Professional reports with reportlab
- **CSV** - Spreadsheet-compatible data
- **JSON** - Structured data export
- **Excel** - XLSX format (optional)

### 2. Auto-Integration
- Add export buttons to existing UIs
- Generate export callbacks automatically
- Template-based export functions

### 3. Export Templates
- Table export (from Treeview)
- Form export (from Entry widgets)
- Custom data export

---

## Commands

### Add Export Capability

```bash
# Add export to project
pygubu-export add <project> --format csv,pdf,json

# Add export button to UI
pygubu-export add-button <project> --format csv

# Generate export code
pygubu-export generate <project> --widget treeview1
```

### Export Data

```bash
# Export from running app (future)
pygubu-export run <project> --output data.csv
```

---

## Usage Examples

### Example 1: Add CSV Export to CRUD App

```bash
# Create CRUD app
pygubu-template myapp crud

# Add CSV export
pygubu-export add myapp --format csv

# Adds export button and callback automatically
```

### Example 2: PDF Reports

```bash
# Add PDF export
pygubu-export add dashboard --format pdf

# Generates report with charts/tables
```

### Example 3: Multi-Format Export

```bash
# Support multiple formats
pygubu-export add myapp --format csv,json,pdf

# User can choose format at runtime
```

---

## Implementation

### Module: `src/pygubuai/data_export.py`

```python
def add_export_capability(project, formats):
    """Add export to project"""
    # Add export button to UI
    # Generate export callbacks
    # Add format selection

def generate_export_code(project, widget_id, format):
    """Generate export code for widget"""
    # Detect widget type
    # Generate appropriate export function

def export_treeview_to_csv(treeview_id):
    """Export Treeview data to CSV"""

def export_to_pdf(data, output):
    """Export data to PDF"""
```

---

## Dependencies

**Optional (installed on demand):**
- reportlab (PDF)
- openpyxl (Excel)

**Built-in:**
- csv (CSV)
- json (JSON)

---

## Status

**Planned for v0.6.1** - 2-3 days implementation
