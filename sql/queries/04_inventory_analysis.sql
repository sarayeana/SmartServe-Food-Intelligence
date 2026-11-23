
USE smartserve_db;

-- ============================================================
-- 1. OVERALL INVENTORY PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) AS total_inventory_records,
    COUNT(DISTINCT store_id) AS total_stores,
    COUNT(DISTINCT product_id) AS total_products,
    SUM(opening_stock) AS total_opening_stock,
    SUM(received_qty) AS total_received_quantity,
    SUM(prepared_qty) AS total_prepared_quantity,
    SUM(sold_qty) AS total_sold_quantity,
    SUM(closing_stock) AS total_closing_stock,
    SUM(damaged_qty) AS total_damaged_quantity,
    SUM(expired_qty) AS total_expired_quantity,
    SUM(stockout_flag) AS total_stockout_records,
    ROUND(
        SUM(stockout_flag) / COUNT(*) * 100, 2
    ) AS stockout_record_pct
FROM fact_inventory;


-- ============================================================
-- 2. STOCKOUT ANALYSIS BY STORE AND PRODUCT
-- ============================================================

SELECT
    i.store_id,
    st.store_name,
    i.product_id,
    p.product_name,
    COUNT(*) AS inventory_days,
    SUM(i.stockout_flag) AS stockout_days,
    ROUND(
        SUM(i.stockout_flag) / COUNT(*) * 100, 2
    ) AS stockout_rate_pct,
    SUM(i.sold_qty) AS total_units_sold,
    SUM(i.closing_stock) AS total_closing_stock
FROM fact_inventory i
JOIN dim_store st
    ON i.store_id = st.store_id
JOIN dim_product p
    ON i.product_id = p.product_id
GROUP BY
    i.store_id,
    st.store_name,
    i.product_id,
    p.product_name
ORDER BY
    stockout_rate_pct DESC,
    stockout_days DESC;


-- ============================================================
-- 3. PREPARATION PLANNING VS ACTUAL PREPARATION
-- ============================================================

SELECT
    st.store_id,
    st.store_name,
    p.product_id,
    p.product_name,
    SUM(pr.planned_qty) AS total_planned_quantity,
    SUM(pr.actual_qty) AS total_actual_quantity,
    SUM(pr.actual_qty - pr.planned_qty) AS preparation_difference,
    ROUND(
        SUM(pr.actual_qty - pr.planned_qty) /
        NULLIF(SUM(pr.planned_qty), 0) * 100,
        2
    ) AS preparation_variance_pct,
    ROUND(
        SUM(pr.preparation_cost), 2
    ) AS total_preparation_cost,
    ROUND(
        AVG(pr.preparation_time_minutes), 2
    ) AS avg_preparation_time_minutes
FROM fact_preparation pr
JOIN dim_store st
    ON pr.store_id = st.store_id
JOIN dim_product p
    ON pr.product_id = p.product_id
GROUP BY
    st.store_id,
    st.store_name,
    p.product_id,
    p.product_name
ORDER BY
    ABS(preparation_difference) DESC;


-- ============================================================
-- 4. DAMAGED AND EXPIRED INVENTORY ANALYSIS
-- ============================================================

SELECT
    st.store_id,
    st.store_name,
    p.product_id,
    p.product_name,
    SUM(i.damaged_qty) AS total_damaged_quantity,
    SUM(i.expired_qty) AS total_expired_quantity,
    SUM(i.damaged_qty + i.expired_qty) AS total_loss_quantity,
    SUM(i.sold_qty) AS total_units_sold,
    ROUND(
        SUM(i.damaged_qty + i.expired_qty) /
        NULLIF(
            SUM(i.sold_qty + i.damaged_qty + i.expired_qty),
            0
        ) * 100,
        2
    ) AS inventory_loss_rate_pct
FROM fact_inventory i
JOIN dim_store st
    ON i.store_id = st.store_id
JOIN dim_product p
    ON i.product_id = p.product_id
GROUP BY
    st.store_id,
    st.store_name,
    p.product_id,
    p.product_name
ORDER BY
    total_loss_quantity DESC;
