

PRAGMA foreign_keys = ON;

-- 1. Fund master dimension
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_key INTEGER PRIMARY KEY,
    amfi_code TEXT UNIQUE NOT NULL,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- 2. Date dimension
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date TEXT UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER
);

-- 3. NAV fact table
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    nav REAL NOT NULL CHECK (nav > 0),
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    UNIQUE (fund_key, date_key)
);

-- 4. Investor transactions fact table
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    investor_id TEXT,
    fund_key INTEGER,
    date_key INTEGER,
    transaction_type TEXT,
    amount_inr REAL CHECK (amount_inr > 0),
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- 5. Scheme performance fact table
CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id INTEGER PRIMARY KEY,
    fund_key INTEGER NOT NULL,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    FOREIGN KEY (fund_key) REFERENCES dim_fund(fund_key),
    UNIQUE (fund_key)
);

-- 6. AUM fact table
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY,
    date_key INTEGER NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    UNIQUE (date_key, fund_house)
);

