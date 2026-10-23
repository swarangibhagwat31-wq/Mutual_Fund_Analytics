
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import sqlite3

PROJECT = Path.cwd()
CSV_PATH = PROJECT / "data" / "processed" / "monthly_sip_inflows.csv"
DB_PATH = PROJECT / "bluestock_mf.db"

df = pd.read_csv(CSV_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}")

# Replace only this SIP table; other tables remain untouched.
df.to_sql(
    "monthly_sip_inflows",
    engine,
    if_exists="replace",
    index=False
)

engine.dispose()

# Verify that SQLite row count matches the source CSV.
with sqlite3.connect(DB_PATH) as conn:
    db_count = conn.execute(
        "SELECT COUNT(*) FROM monthly_sip_inflows"
    ).fetchone()[0]

print("CSV rows:", len(df))
print("SQLite rows:", db_count)

if len(df) == db_count:
    print("SIP data loaded and row counts match.")
else:
    print("ERROR: Row counts do not match.")
