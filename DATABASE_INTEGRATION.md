# Database Integration - PygubuAI v0.7.0

## Overview

Add SQLite/PostgreSQL database support to PygubuAI projects with automatic CRUD code generation.

## Features

### 1. Database Initialization
- SQLite (zero-config)
- PostgreSQL (production-ready)
- Automatic schema creation

### 2. CRUD Templates
- Enhanced CRUD template with DB backend
- Auto-generated models
- Query builders

### 3. ORM Integration
- Simple ORM wrapper
- No external dependencies for SQLite
- Optional psycopg2 for PostgreSQL

---

## Commands

```bash
# Initialize database
pygubu-db init <project> --type sqlite

# Add table
pygubu-db add-table <project> users name:str email:str age:int

# Generate CRUD UI
pygubu-template <project> crud-db --table users

# Migrate schema
pygubu-db migrate <project>
```

---

## Usage Examples

### Example 1: Todo App with SQLite

```bash
# Create project
pygubu-create todo "todo app"

# Initialize database
pygubu-db init todo --type sqlite

# Add tasks table
pygubu-db add-table todo tasks title:str done:bool

# Generate CRUD UI
pygubu-template todo crud-db --table tasks
```

### Example 2: Inventory System

```bash
pygubu-db init inventory --type sqlite
pygubu-db add-table inventory products name:str price:float stock:int
pygubu-template inventory crud-db --table products
```

---

## Implementation

### Module: `src/pygubuai/database.py`

```python
class DatabaseHelper:
    def __init__(self, db_path, db_type='sqlite'):
        self.db_path = db_path
        self.db_type = db_type
    
    def create_table(self, name, schema):
        """Create table with schema"""
    
    def generate_crud_code(self, table_name):
        """Generate CRUD operations"""
    
    def add_to_project(self, project_name):
        """Integrate DB into project"""
```

---

## Status

**Planned for v0.7.0** - 5-6 days implementation
