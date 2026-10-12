from pathlib import Path

import pandas as pd


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def inspect_csv_files():
    """Load and inspect all CSV files in the raw data folder."""

    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/raw.")
        print("Please add the provided datasets before running this script.")
        return

    print(f"Found {len(csv_files)} CSV file(s).")

    for file_path in csv_files:
        print("\n" + "=" * 60)
        print(f"File: {file_path.name}")
        print("=" * 60)

        try:
            df = pd.read_csv(file_path)

            print("\nShape (rows, columns):")
            print(df.shape)

            print("\nData types:")
            print(df.dtypes)

            print("\nFirst five rows:")
            print(df.head())

            print("\nMissing values per column:")
            print(df.isna().sum())

            print("\nDuplicate rows:")
            print(df.duplicated().sum())

        except Exception as error:
            print(f"Could not read {file_path.name}: {error}")


if __name__ == "__main__":
    inspect_csv_files()