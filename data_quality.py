import pandas as pd
from pathlib import Path

# ==================================================
# 1. PROJECT PATHS
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# 2. MANAGER-PROVIDED DATASETS
# ==================================================

FILES = {
    "investor_transactions": (
        "1788499980509-304c1255-08_investor_transactions.csv"
    ),
    "portfolio_holdings": (
        "1788499982117-e3d6ab98-09_portfolio_holdings.csv"
    ),
    "benchmark_indices": (
        "1788499982615-f9647ab2-10_benchmark_indices.csv"
    ),
    "fund_master": (
        "1788499983024-b042c300-01_fund_master.csv"
    ),
    "nav_history": (
        "1788499983331-4389156d-02_nav_history.csv"
    ),
    "aum_by_fund_house": (
        "1788499984134-b0cbf625-03_aum_by_fund_house.csv"
    ),
    "monthly_sip_inflows": (
        "1788499984405-d702a6c6-04_monthly_sip_inflows.csv"
    ),
    "category_inflows": (
        "1788499984721-4b860901-05_category_inflows.csv"
    ),
    "industry_folio_count": (
        "1788499985036-da4a0c4a-06_industry_folio_count.csv"
    ),
    "scheme_performance": (
        "1788499985420-bb134abf-07_scheme_performance.csv"
    ),
}

# ==================================================
# 3. LOAD THE DATASETS
# ==================================================

datasets = {}

for dataset_name, filename in FILES.items():

    file_path = RAW_DATA_DIR / filename

    if file_path.exists():
        try:
            df = pd.read_csv(file_path)
            datasets[dataset_name] = df

            print("\n" + "=" * 60)
            print(f"DATASET: {dataset_name}")
            print("=" * 60)

            print("Shape:", df.shape)

            print("\nColumns:")
            print(df.columns.tolist())

            print("\nData types:")
            print(df.dtypes)

            print("\nFirst five rows:")
            print(df.head())

        except Exception as error:
            print(f"Could not read {filename}: {error}")

    else:
        print(f"\nFILE NOT FOUND: {filename}")

# ==================================================
# 4. EXPLORE FUND MASTER
# ==================================================

if "fund_master" in datasets:

    fund_master = datasets["fund_master"]

    print("\n" + "=" * 60)
    print("FUND MASTER EXPLORATION")
    print("=" * 60)

    for column in fund_master.columns:

        column_lower = column.lower()

        if any(
            word in column_lower
            for word in [
                "fund_house",
                "fund house",
                "category",
                "subcategory",
                "sub_category",
                "risk",
            ]
        ):

            print(f"\nColumn: {column}")

            print(
                "Number of unique values:",
                fund_master[column].nunique()
            )

            print("Unique values:")
            print(fund_master[column].dropna().unique())

# ==================================================
# 5. DATA QUALITY CHECKS
# ==================================================

summary_rows = []

for dataset_name, df in datasets.items():

    print("\n" + "=" * 60)
    print(f"DATA QUALITY: {dataset_name}")
    print("=" * 60)

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    print("\nMissing values by column:")
    print(df.isnull().sum())

    print("\nTotal missing values:", missing_values)
    print("Duplicate rows:", duplicate_rows)
    print("Empty dataset:", df.empty)

    summary_rows.append({
        "dataset": dataset_name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "total_missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "is_empty": df.empty,
    })

# ==================================================
# 6. SCHEME CODE VALIDATION
# ==================================================

print("\n" + "=" * 60)
print("SCHEME CODE VALIDATION")
print("=" * 60)

if "fund_master" in datasets and "nav_history" in datasets:

    fund_master = datasets["fund_master"]
    nav_history = datasets["nav_history"]

    # Detect likely scheme-code columns
    def find_scheme_code_column(df):

        possible_names = [
            "scheme_code",
            "scheme code",
            "amfi_code",
            "amfi code",
            "amfi_scheme_code",
            "scheme_id",
        ]

        normalized_columns = {
            str(column).strip().lower(): column
            for column in df.columns
        }

        for name in possible_names:
            if name in normalized_columns:
                return normalized_columns[name]

        for column in df.columns:
            name = str(column).strip().lower()

            if "scheme" in name and "code" in name:
                return column

        return None

    fund_code_column = find_scheme_code_column(fund_master)
    nav_code_column = find_scheme_code_column(nav_history)

    print("Fund master scheme-code column:", fund_code_column)
    print("NAV history scheme-code column:", nav_code_column)

    if fund_code_column and nav_code_column:

        fund_codes = set(
            fund_master[fund_code_column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        nav_codes = set(
            nav_history[nav_code_column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        matching_codes = fund_codes.intersection(nav_codes)
        missing_nav_codes = fund_codes - nav_codes
        extra_nav_codes = nav_codes - fund_codes

        print("\nUnique codes in fund_master:", len(fund_codes))
        print("Unique codes in nav_history:", len(nav_codes))
        print("Matching scheme codes:", len(matching_codes))

        print("\nFund master codes without NAV records:")
        print(sorted(missing_nav_codes))

        print("\nNAV codes absent from fund_master:")
        print(sorted(extra_nav_codes))

    else:
        print(
            "Scheme-code columns could not be identified automatically."
        )
        print("Check the column names printed above.")

else:
    print(
        "Both fund_master and nav_history are required "
        "for scheme-code validation."
    )

# ==================================================
# 7. CHECK FETCHED NAV FILES
# ==================================================

NAV_FILES = [
    "HDFC_Top_100_Direct_nav.csv",
    "SBI_Bluechip_nav.csv",
    "ICICI_Bluechip_nav.csv",
    "Nippon_Large_Cap_nav.csv",
    "Axis_Bluechip_nav.csv",
    "Kotak_Bluechip_nav.csv",
]

print("\n" + "=" * 60)
print("FETCHED NAV FILE CHECKS")
print("=" * 60)

for filename in NAV_FILES:

    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        print(f"\nNAV FILE NOT FOUND: {filename}")
        continue

    try:
        nav_df = pd.read_csv(file_path)

        print(f"\nFile: {filename}")
        print("Rows and columns:", nav_df.shape)
        print("Columns:", nav_df.columns.tolist())

        print("Missing values:")
        print(nav_df.isnull().sum())

        print("Duplicate rows:", nav_df.duplicated().sum())

        # Detect the NAV column
        nav_column = next(
            (
                column
                for column in nav_df.columns
                if str(column).strip().lower() == "nav"
            ),
            None,
        )

        if nav_column:

            nav_values = pd.to_numeric(
                nav_df[nav_column],
                errors="coerce"
            )

            print(
                "Missing/non-numeric NAV values:",
                int(nav_values.isna().sum())
            )

            print(
                "Zero or negative NAV values:",
                int((nav_values <= 0).sum())
            )

        # Detect a date column
        date_column = next(
            (
                column
                for column in nav_df.columns
                if str(column).strip().lower() in [
                    "date",
                    "nav_date",
                    "nav date",
                ]
            ),
            None,
        )

        if date_column:

            dates = pd.to_datetime(
                nav_df[date_column],
                errors="coerce",
                dayfirst=True
            )

            print(
                "Invalid/unparseable dates:",
                int(dates.isna().sum())
            )

    except Exception as error:
        print(f"Could not inspect {filename}: {error}")

# ==================================================
# 8. SAVE THE SUMMARY REPORT
# ==================================================

if summary_rows:

    summary_df = pd.DataFrame(summary_rows)

    report_path = REPORT_DIR / "day1_data_quality_summary.csv"

    summary_df.to_csv(report_path, index=False)

    print("\n" + "=" * 60)
    print("DATA QUALITY SUMMARY SAVED")
    print("=" * 60)

    print("Report location:", report_path)

    print("\nSummary:")
    print(summary_df.to_string(index=False))

print("\nStep 9 checks completed.")