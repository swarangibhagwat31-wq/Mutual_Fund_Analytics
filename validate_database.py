
import sqlite3
from pathlib import Path

DB = Path.cwd() / "bluestock_mf.db"

with sqlite3.connect(DB) as conn:
    checks = {
        "Funds without a matching fund key in NAV": """
            SELECT COUNT(*)
            FROM fact_nav n
            LEFT JOIN dim_fund f ON n.fund_key = f.fund_key
            WHERE f.fund_key IS NULL
        """,
        "NAV records without a matching date": """
            SELECT COUNT(*)
            FROM fact_nav n
            LEFT JOIN dim_date d ON n.date_key = d.date_key
            WHERE d.date_key IS NULL
        """,
        "Transactions without a matching fund": """
            SELECT COUNT(*)
            FROM fact_transactions t
            LEFT JOIN dim_fund f ON t.fund_key = f.fund_key
            WHERE f.fund_key IS NULL
        """,
        "Transactions without a matching date": """
            SELECT COUNT(*)
            FROM fact_transactions t
            LEFT JOIN dim_date d ON t.date_key = d.date_key
            WHERE d.date_key IS NULL
        """
    }

    print("DATABASE VALIDATION")
    for label, query in checks.items():
        count = conn.execute(query).fetchone()[0]
        print(f"{label}: {count}")
