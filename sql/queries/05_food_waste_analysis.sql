
USE smartserve_db;

-- ============================================================
-- 1. OVERALL FOOD WASTE PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) AS total_waste_records,
    COUNT(DISTINCT store_id) AS total_stores,
    COUNT(DISTINCT product_id) AS total_products,
    SUM(quantity_wasted) AS total_quantity_wasted,
    ROUND(SUM(waste_cost), 2) AS total_waste_cost,
    ROUND(AVG(quantity_wasted), 2) AS avg_quantity_per_record,
    ROUND(AVG(waste_cost), 2) AS avg_waste_cost_per_record
FROM fact_waste;


-- ============================================================
-- 2. FOOD WASTE BY REASON
-- ============================================================

SELECT
    waste_reason_id AS waste_reason,
    COUNT(*) AS waste_records,
    SUM(quantity_wasted) AS total_quantity_wasted,
    ROUND(SUM(waste_cost), 2) AS total_waste_cost,
    ROUND(
        SUM(waste_cost) /
        NULLIF(
            (SELECT SUM(waste_cost) FROM fact_waste),
            0
        ) * 100,
        2
    ) AS percentage_of_total_waste_cost
FROM fact_waste
GROUP BY waste_reason_id
ORDER BY total_waste_cost DESC;


-- ============================================================
-- 3. FOOD WASTE BY STORE
-- ============================================================

SELECT
    st.store_id,
    st.store_name,
    COUNT(w.waste_id) AS waste_records,
    SUM(w.quantity_wasted) AS total_quantity_wasted,
    ROUND(SUM(w.waste_cost), 2) AS total_waste_cost,
    ROUND(
        SUM(w.waste_cost) /
        NULLIF(SUM(w.quantity_wasted), 0),
        2
    ) AS average_cost_per_wasted_unit
FROM fact_waste w
JOIN dim_store st
    ON w.store_id = st.store_id
GROUP BY
    st.store_id,
    st.store_name
ORDER BY total_waste_cost DESC;


-- ============================================================
-- 4. FOOD WASTE BY PRODUCT
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(w.waste_id) AS waste_records,
    SUM(w.quantity_wasted) AS total_quantity_wasted,
    ROUND(SUM(w.waste_cost), 2) AS total_waste_cost,
    ROUND(
        SUM(w.waste_cost) /
        NULLIF(SUM(w.quantity_wasted), 0),
        2
    ) AS average_cost_per_wasted_unit
FROM fact_waste w
JOIN dim_product p
    ON w.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_waste_cost DESC;


-- ============================================================
-- 5. MONTHLY FOOD WASTE TREND
-- ============================================================

SELECT
    d.month,
    d.month_name,
    COUNT(w.waste_id) AS waste_records,
    SUM(w.quantity_wasted) AS total_quantity_wasted,
    ROUND(SUM(w.waste_cost), 2) AS total_waste_cost,
    ROUND(
        AVG(w.waste_cost),
        2
    ) AS average_waste_cost_per_record
FROM fact_waste w
JOIN dim_date d
    ON w.date_id = d.date_id
GROUP BY
    d.month,
    d.month_name
ORDER BY d.month;
