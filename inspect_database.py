
import sqlite3
import pandas as pd
from pathlib import Path

project_dir = Path.cwd()
db_path = project_dir / "bluestock_mf.db"
processed_dir = project_dir / "data" / "processed"

# 1. Inspect database tables and their columns
with sqlite3.connect(db_path) as conn:
    tables = pd.read_sql_query("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """, conn)

    print("DATABASE TABLES AND COLUMNS")

    for table_name in tables["name"]:
        info = conn.execute(
            f'PRAGMA table_info("{table_name}")'
        ).fetchall()

        print(f"\nTable: {table_name}")
        for column in info:
            print(f"  {column[1]} ({column[2]})")

# 2. Inspect processed CSV files
print("\n\nPROCESSED CSV FILES")

for csv_path in sorted(processed_dir.glob("*.csv")):
    df = pd.read_csv(csv_path, nrows=5)
    print(f"\nFile: {csv_path.name}")
    print("Columns:", df.columns.tolist())

import sqlite3
from pathlib import Path

db_path = Path.cwd() / "bluestock_mf.db"

with sqlite3.connect(db_path) as conn:
    tables = [
        "dim_date",
        "dim_fund",
        "fact_aum",
        "fact_nav",
        "fact_performance",
        "fact_transactions"
    ]

    print("\nDATABASE ROW COUNTS")
    for table in tables:
        count = conn.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]
        print(f"{table}: {count}")