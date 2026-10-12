from pathlib import Path

import pandas as pd
import requests


PROJECT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

SCHEMES = {
    "HDFC_Top_100_Direct": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841",
}


def fetch_nav(scheme_name, scheme_code):
    """Fetch NAV history for one mutual fund scheme."""

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nFetching {scheme_name} ({scheme_code})...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        payload = response.json()

        if payload.get("status") != "SUCCESS":
            print(f"API did not return SUCCESS for {scheme_name}.")
            return

        metadata = payload.get("meta", {})
        nav_records = payload.get("data", [])

        if not nav_records:
            print(f"No NAV records returned for {scheme_name}.")
            return

        df = pd.DataFrame(nav_records)

        output_path = RAW_DATA_DIR / f"{scheme_name}_nav.csv"
        df.to_csv(output_path, index=False)

        print(f"Saved {len(df)} NAV records to {output_path}")
        print(f"Fund name: {metadata.get('scheme_name', 'Not provided')}")
        print("\nFirst five NAV records:")
        print(df.head())

    except (requests.RequestException, ValueError) as error:
        print(f"Could not fetch {scheme_name}: {error}")


if __name__ == "__main__":
    for name, code in SCHEMES.items():
        fetch_nav(name, code)