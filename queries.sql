
-- =====================================================
-- Mutual Fund Analytics: 10 Analytical SQL Queries
-- Database: bluestock_mf.db
-- =====================================================

-- Q1. Top 5 fund houses by latest available AUM
WITH latest_aum_date AS (
    SELECT MAX(date_key) AS date_key
    FROM fact_aum
)
SELECT
    a.fund_house,
    a.aum_crore,
    a.aum_lakh_crore,
    a.num_schemes
FROM fact_aum a
JOIN latest_aum_date d
    ON a.date_key = d.date_key
ORDER BY a.aum_crore DESC
LIMIT 5;


-- Q2. Average NAV per month
SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav), 4) AS average_nav,
    COUNT(*) AS nav_records
FROM fact_nav n
JOIN dim_date d
    ON n.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- Q3. SIP year-over-year growth
-- Uses monthly_sip_inflows.csv directly if loaded as a table.
SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;


-- Q4. Number of transactions by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_transaction_amount
FROM fact_transactions
GROUP BY state
ORDER BY transaction_count DESC;


-- Q5. Funds with expense ratio below 1%
SELECT
    amfi_code,
    scheme_name,
    fund_house,
    category,
    sub_category,
    plan,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
  AND expense_ratio_pct IS NOT NULL
ORDER BY expense_ratio_pct ASC;


-- Q6. Top 5 funds by assets under management
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    p.aum_crore,
    p.return_1yr_pct,
    p.return_3yr_pct,
    p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.fund_key = f.fund_key
WHERE p.aum_crore IS NOT NULL
ORDER BY p.aum_crore DESC
LIMIT 5;


-- Q7. Best 5 funds by 3-year return
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    p.return_3yr_pct,
    p.benchmark_3yr_pct,
    p.alpha
FROM fact_performance p
JOIN dim_fund f
    ON p.fund_key = f.fund_key
WHERE p.return_3yr_pct IS NOT NULL
ORDER BY p.return_3yr_pct DESC
LIMIT 5;


-- Q8. Investor transactions by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr,
    ROUND(AVG(amount_inr), 2) AS average_amount_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;


-- Q9. Investor transactions by age group
SELECT
    age_group,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM fact_transactions
GROUP BY age_group
ORDER BY transaction_count DESC;


-- Q10. Funds with the highest 5-year returns
SELECT
    f.scheme_name,
    f.fund_house,
    f.category,
    p.return_5yr_pct,
    p.sharpe_ratio,
    p.max_drawdown_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.fund_key = f.fund_key
WHERE p.return_5yr_pct IS NOT NULL
ORDER BY p.return_5yr_pct DESC
LIMIT 5;
