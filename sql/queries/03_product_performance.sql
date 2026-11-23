
-- ============================================================
-- SMARTSERVE FOOD INTELLIGENCE
-- QUERY 03: PRODUCT PERFORMANCE ANALYSIS
-- Database: smartserve_db
-- ============================================================

USE smartserve_db;


-- ============================================================
-- 1. OVERALL PRODUCT PERFORMANCE
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,

    SUM(s.quantity) AS units_sold,
    COUNT(DISTINCT s.order_id) AS total_orders,

    ROUND(SUM(s.gross_sales), 2) AS gross_sales,
    ROUND(SUM(s.discount_amount), 2) AS total_discounts,
    ROUND(SUM(s.net_sales), 2) AS net_revenue,
    ROUND(SUM(s.cost_amount), 2) AS total_cost,
    ROUND(SUM(s.profit_amount), 2) AS total_profit,

    ROUND(
        SUM(s.profit_amount) /
        NULLIF(SUM(s.net_sales), 0) * 100,
        2
    ) AS profit_margin_pct,

    ROUND(
        SUM(s.net_sales) /
        NULLIF(SUM(s.quantity), 0),
        2
    ) AS revenue_per_unit

FROM dim_product p

JOIN fact_sales s
    ON p.product_id = s.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory

ORDER BY net_revenue DESC;


-- ============================================================
-- 2. PRODUCT REVENUE AND PROFIT RANKING
-- ============================================================

WITH product_summary AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,

        SUM(s.quantity) AS units_sold,

        ROUND(SUM(s.net_sales), 2) AS net_revenue,
        ROUND(SUM(s.profit_amount), 2) AS total_profit

    FROM dim_product p

    JOIN fact_sales s
        ON p.product_id = s.product_id

    GROUP BY
        p.product_id,
        p.product_name,
        p.category
)

SELECT
    product_id,
    product_name,
    category,
    units_sold,
    net_revenue,
    total_profit,

    DENSE_RANK() OVER (
        ORDER BY net_revenue DESC
    ) AS revenue_rank,

    DENSE_RANK() OVER (
        ORDER BY total_profit DESC
    ) AS profit_rank

FROM product_summary

ORDER BY revenue_rank;


-- ============================================================
-- 3. PRODUCT CATEGORY PERFORMANCE
-- ============================================================

SELECT
    p.category,

    COUNT(DISTINCT p.product_id) AS total_products,
    SUM(s.quantity) AS units_sold,
    COUNT(DISTINCT s.order_id) AS total_orders,

    ROUND(SUM(s.net_sales), 2) AS net_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit,

    ROUND(
        SUM(s.profit_amount) /
        NULLIF(SUM(s.net_sales), 0) * 100,
        2
    ) AS profit_margin_pct

FROM dim_product p

JOIN fact_sales s
    ON p.product_id = s.product_id

GROUP BY p.category

ORDER BY net_revenue DESC;


-- ============================================================
-- 4. MONTHLY PRODUCT CATEGORY PERFORMANCE
-- ============================================================

SELECT
    p.category,
    d.month,
    d.month_name,

    SUM(s.quantity) AS units_sold,

    ROUND(SUM(s.net_sales), 2) AS net_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit

FROM fact_sales s

JOIN dim_product p
    ON s.product_id = p.product_id

JOIN dim_date d
    ON s.date_id = d.date_id

GROUP BY
    p.category,
    d.month,
    d.month_name

ORDER BY
    p.category,
    d.month;
