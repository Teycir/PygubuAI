"""Database integration for PygubuAI projects"""
import sqlite3
from pathlib import Path
from typing import Dict, List, Any
from .registry import Registry

class DatabaseHelper:
    """Helper for database operations"""
    
    def __init__(self, db_path: str, db_type: str = 'sqlite'):
        self.db_path = db_path
        self.db_type = db_type
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        if self.db_type == 'sqlite':
            self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def create_table(self, name: str, schema: Dict[str, str]):
        """Create table with schema"""
        columns = []
        for col_name, col_type in schema.items():
            sql_type = self._map_type(col_type)
            columns.append(f"{col_name} {sql_type}")
        
        sql = f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY, {', '.join(columns)})"
        
        conn = self.connect()
        conn.execute(sql)
        conn.commit()
        conn.close()
    
    def _map_type(self, py_type: str) -> str:
        """Map Python type to SQL type"""
        mapping = {
            'str': 'TEXT',
            'int': 'INTEGER',
            'float': 'REAL',
            'bool': 'INTEGER'
        }
        return mapping.get(py_type, 'TEXT')
    
    def generate_crud_code(self, table_name: str, schema: Dict[str, str]) -> str:
        """Generate CRUD operations code"""
        columns = list(schema.keys())
        
        code = f'''
    def load_{table_name}(self):
        """Load {table_name} from database"""
        conn = sqlite3.connect('{self.db_path}')
        cursor = conn.execute("SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def add_{table_name}(self, {', '.join(columns)}):
        """Add new {table_name}"""
        conn = sqlite3.connect('{self.db_path}')
        conn.execute(
            "INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})",
            ({', '.join(columns)})
        )
        conn.commit()
        conn.close()
    
    def update_{table_name}(self, id, {', '.join(columns)}):
        """Update {table_name}"""
        conn = sqlite3.connect('{self.db_path}')
        conn.execute(
            "UPDATE {table_name} SET {', '.join([f'{c}=?' for c in columns])} WHERE id=?",
            ({', '.join(columns)}, id)
        )
        conn.commit()
        conn.close()
    
    def delete_{table_name}(self, id):
        """Delete {table_name}"""
        conn = sqlite3.connect('{self.db_path}')
        conn.execute("DELETE FROM {table_name} WHERE id=?", (id,))
        conn.commit()
        conn.close()
'''
        return code

def init_database(project_name: str, db_type: str = 'sqlite'):
    """Initialize database for project"""
    registry = Registry()
    project_path = registry.get_project(project_name)
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")
    
    db_path = Path(project_path) / f"{project_name}.db"
    helper = DatabaseHelper(str(db_path), db_type)
    helper.connect()
    
    return str(db_path)

def add_table(project_name: str, table_name: str, schema: Dict[str, str]):
    """Add table to project database"""
    registry = Registry()
    project_path = registry.get_project(project_name)
    if not project_path:
        raise ValueError(f"Project '{project_name}' not found")
    
    db_path = Path(project_path) / f"{project_name}.db"
    helper = DatabaseHelper(str(db_path))
    helper.create_table(table_name, schema)
    
    # Add CRUD code to project
    py_file = Path(project_path) / f"{project_name}.py"
    if py_file.exists():
        code = py_file.read_text()
        crud_code = helper.generate_crud_code(table_name, schema)
        
        if "def run(self):" in code:
            code = code.replace("def run(self):", f"{crud_code}\n\n    def run(self):")
            py_file.write_text(code)

def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: pygubu-db <command> <project> [options]")
        print("Commands:")
        print("  init <project> [--type sqlite|postgres]")
        print("  add-table <project> <table> <col:type> ...")
        sys.exit(1)
    
    command = sys.argv[1]
    project = sys.argv[2]
    
    if command == "init":
        db_type = "sqlite"
        if "--type" in sys.argv:
            idx = sys.argv.index("--type")
            if idx + 1 < len(sys.argv):
                db_type = sys.argv[idx + 1]
        
        try:
            db_path = init_database(project, db_type)
            print(f"✓ Initialized {db_type} database for '{project}'")
            print(f"  Database: {db_path}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif command == "add-table":
        if len(sys.argv) < 4:
            print("Usage: pygubu-db add-table <project> <table> <col:type> ...")
            sys.exit(1)
        
        table_name = sys.argv[3]
        schema = {}
        
        for arg in sys.argv[4:]:
            if ':' in arg:
                col, typ = arg.split(':')
                schema[col] = typ
        
        try:
            add_table(project, table_name, schema)
            print(f"✓ Added table '{table_name}' to '{project}'")
            print(f"  Columns: {', '.join(schema.keys())}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
