
USE smartserve_db;

-- ============================================================
-- 1. FORECAST DATA COVERAGE
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT date_id) AS unique_dates,
    COUNT(DISTINCT store_id) AS unique_stores,
    COUNT(DISTINCT product_id) AS unique_products,
    MIN(full_date) AS first_date,
    MAX(full_date) AS last_date
FROM forecast_performance;


-- ============================================================
-- 2. CHECK MISSING VALUES
-- ============================================================

SELECT
    SUM(date_id IS NULL) AS missing_date_ids,
    SUM(full_date IS NULL) AS missing_dates,
    SUM(store_id IS NULL) AS missing_store_ids,
    SUM(product_id IS NULL) AS missing_product_ids,
    SUM(actual_sales_qty IS NULL) AS missing_actuals,
    SUM(predicted_sales_qty IS NULL) AS missing_predictions
FROM forecast_performance;


-- ============================================================
-- 3. CHECK DUPLICATE DATE-STORE-PRODUCT COMBINATIONS
-- ============================================================

SELECT
    date_id,
    store_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM forecast_performance
GROUP BY date_id, store_id, product_id
HAVING COUNT(*) > 1;
