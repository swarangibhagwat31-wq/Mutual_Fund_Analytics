
import pandas as pd
from pathlib import Path

data_dir = Path("data/processed")

funds = pd.read_csv(data_dir / "fund_master.csv", dtype={"amfi_code": str})
nav = pd.read_csv(data_dir / "nav_history.csv", dtype={"amfi_code": str})

# Normalize codes to avoid mismatches caused by spaces or formatting
fund_codes = set(funds["amfi_code"].str.strip())
nav_codes = set(nav["amfi_code"].str.strip())

missing_codes = sorted(nav_codes - fund_codes)

print("Unique fund master codes:", len(fund_codes))
print("Unique NAV codes:", len(nav_codes))
print("NAV codes missing from fund master:", len(missing_codes))
print("First 20 missing codes:", missing_codes[:20])

missing_nav = nav[nav["amfi_code"].str.strip().isin(missing_codes)]
print("\nRows affected:", len(missing_nav))
print(missing_nav.head(10))

missing_nav.to_csv(
    data_dir / "nav_codes_missing_from_fund_master.csv",
    index=False
)

print("\nMissing-code report saved in data/processed/")
