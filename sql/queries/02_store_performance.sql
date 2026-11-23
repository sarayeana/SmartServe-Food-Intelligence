
-- ============================================================
-- SMARTSERVE FOOD INTELLIGENCE
-- QUERY 02: STORE PERFORMANCE ANALYSIS
-- Database: smartserve_db
-- ============================================================

USE smartserve_db;


-- ============================================================
-- 1. OVERALL STORE PERFORMANCE
-- ============================================================

SELECT
    st.store_id,
    st.store_name,
    st.city,
    st.area,
    st.store_type,

    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS total_units_sold,

    ROUND(SUM(s.net_sales), 2) AS total_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit,

    ROUND(
        SUM(s.profit_amount) /
        NULLIF(SUM(s.net_sales), 0) * 100,
        2
    ) AS profit_margin_pct,

    ROUND(
        SUM(s.net_sales) /
        NULLIF(COUNT(DISTINCT s.order_id), 0),
        2
    ) AS average_order_value,

    COUNT(DISTINCT s.date_id) AS active_sales_days,

    ROUND(
        SUM(s.net_sales) /
        NULLIF(COUNT(DISTINCT s.date_id), 0),
        2
    ) AS average_daily_revenue

FROM dim_store st
JOIN fact_sales s
    ON st.store_id = s.store_id

GROUP BY
    st.store_id,
    st.store_name,
    st.city,
    st.area,
    st.store_type

ORDER BY total_revenue DESC;


-- ============================================================
-- 2. STORE REVENUE AND PROFIT RANKING
-- ============================================================

WITH store_summary AS (
    SELECT
        st.store_id,
        st.store_name,
        COUNT(DISTINCT s.order_id) AS total_orders,
        ROUND(SUM(s.net_sales), 2) AS total_revenue,
        ROUND(SUM(s.profit_amount), 2) AS total_profit

    FROM dim_store st
    JOIN fact_sales s
        ON st.store_id = s.store_id

    GROUP BY
        st.store_id,
        st.store_name
)

SELECT
    store_id,
    store_name,
    total_orders,
    total_revenue,
    total_profit,

    DENSE_RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank,

    DENSE_RANK() OVER (
        ORDER BY total_profit DESC
    ) AS profit_rank

FROM store_summary

ORDER BY revenue_rank;


-- ============================================================
-- 3. STORE PERFORMANCE BY MONTH
-- ============================================================

SELECT
    st.store_id,
    st.store_name,
    d.month,
    d.month_name,

    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS units_sold,

    ROUND(SUM(s.net_sales), 2) AS total_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit

FROM fact_sales s

JOIN dim_store st
    ON s.store_id = st.store_id

JOIN dim_date d
    ON s.date_id = d.date_id

GROUP BY
    st.store_id,
    st.store_name,
    d.month,
    d.month_name

ORDER BY
    st.store_id,
    d.month;


-- ============================================================
-- 4. STORE WEEKDAY VS WEEKEND PERFORMANCE
-- ============================================================

SELECT
    st.store_id,
    st.store_name,

    CASE
        WHEN d.is_weekend = 1 THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,

    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS units_sold,

    ROUND(SUM(s.net_sales), 2) AS total_revenue,

    ROUND(
        SUM(s.net_sales) /
        NULLIF(COUNT(DISTINCT d.full_date), 0),
        2
    ) AS average_daily_revenue

FROM fact_sales s

JOIN dim_store st
    ON s.store_id = st.store_id

JOIN dim_date d
    ON s.date_id = d.date_id

GROUP BY
    st.store_id,
    st.store_name,
    d.is_weekend

ORDER BY
    st.store_id,
    d.is_weekend DESC;
