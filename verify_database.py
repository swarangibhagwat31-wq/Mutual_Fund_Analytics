import sqlite3
from pathlib import Path

db_path = Path("bluestock_mf.db")

with sqlite3.connect(db_path) as conn:
    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """).fetchall()

    print("Tables in database:")
    for table in tables:
        print("-", table[0])