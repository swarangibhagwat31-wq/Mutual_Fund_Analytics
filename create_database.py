
import sqlite3
from pathlib import Path

# Project folder: current working directory
project_dir = Path.cwd()

schema_path = project_dir / "sql" / "schema.sql"
db_path = project_dir / "bluestock_mf.db"

if not schema_path.exists():
    raise FileNotFoundError(
        f"schema.sql not found at: {schema_path}"
    )

# Create the SQLite database and execute the schema
with sqlite3.connect(db_path) as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    schema_sql = schema_path.read_text(encoding="utf-8")
    conn.executescript(schema_sql)

    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

print("Database created at:", db_path)
print("\nTables created:")
for table in tables:
    print("-", table[0])
