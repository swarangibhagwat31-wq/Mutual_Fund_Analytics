
import sqlite3
from pathlib import Path
import re

PROJECT = Path.cwd()
DB_PATH = PROJECT / "bluestock_mf.db"
SQL_PATH = PROJECT / "queries.sql"

print("Starting SQL query runner...")
print("Database exists:", DB_PATH.exists())
print("SQL file exists:", SQL_PATH.exists())

sql_text = SQL_PATH.read_text(encoding="utf-8")

# Remove full-line SQL comments before splitting queries.
sql_text = re.sub(r"(?m)^\s*--.*$", "", sql_text)

queries = [
    q.strip()
    for q in sql_text.split(";")
    if q.strip()
]

print("Queries detected:", len(queries))

with sqlite3.connect(DB_PATH) as conn:
    for i, query in enumerate(queries, start=1):
        print(f"\n{'=' * 50}")
        print(f"QUERY {i}")

        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()

            print("Columns:", [c[0] for c in cursor.description or []])
            for row in rows[:10]:
                print(row)

            print("Rows returned:", len(rows))

        except sqlite3.Error as error:
            print("SQL ERROR:", error)

print("\nSQL query runner finished.")



