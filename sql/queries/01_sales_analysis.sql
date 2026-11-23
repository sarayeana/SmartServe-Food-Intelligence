
-- ============================================================
-- SMARTSERVE FOOD INTELLIGENCE
-- QUERY 01: SALES PERFORMANCE ANALYSIS
-- Database: smartserve_db
-- ============================================================

USE smartserve_db;


-- ============================================================
-- 1. OVERALL SALES KPIs
-- ============================================================

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_sales_records,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(gross_sales), 2) AS total_gross_sales,
    ROUND(SUM(discount_amount), 2) AS total_discounts,
    ROUND(SUM(net_sales), 2) AS total_net_revenue,
    ROUND(SUM(cost_amount), 2) AS total_cost,
    ROUND(SUM(profit_amount), 2) AS total_profit,
    ROUND(
        SUM(profit_amount) / NULLIF(SUM(net_sales), 0) * 100,
        2
    ) AS profit_margin_pct,
    ROUND(
        SUM(net_sales) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM fact_sales;


-- ============================================================
-- 2. MONTHLY SALES PERFORMANCE
-- ============================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS units_sold,
    ROUND(SUM(s.net_sales), 2) AS net_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit,
    ROUND(
        SUM(s.profit_amount) /
        NULLIF(SUM(s.net_sales), 0) * 100,
        2
    ) AS profit_margin_pct
FROM fact_sales s
JOIN dim_date d
    ON s.date_id = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- ============================================================
-- 3. DAILY SALES TREND
-- ============================================================

SELECT
    d.full_date,
    d.day_name,
    d.is_weekend,
    d.is_holiday,
    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS units_sold,
    ROUND(SUM(s.net_sales), 2) AS net_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit
FROM fact_sales s
JOIN dim_date d
    ON s.date_id = d.date_id
GROUP BY
    d.full_date,
    d.day_name,
    d.is_weekend,
    d.is_holiday
ORDER BY
    d.full_date;


-- ============================================================
-- 4. SALES PERFORMANCE BY PAYMENT METHOD
-- ============================================================

SELECT
    payment_method,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(net_sales), 2) AS net_revenue,
    ROUND(SUM(profit_amount), 2) AS total_profit
FROM fact_sales
GROUP BY payment_method
ORDER BY net_revenue DESC;


-- ============================================================
-- 5. PROMOTION PERFORMANCE
-- ============================================================

SELECT
    COALESCE(p.promotion_name, 'No Promotion') AS promotion_name,
    COALESCE(p.promotion_type, 'No Promotion') AS promotion_type,
    COUNT(DISTINCT s.order_id) AS total_orders,
    SUM(s.quantity) AS units_sold,
    ROUND(SUM(s.gross_sales), 2) AS gross_sales,
    ROUND(SUM(s.discount_amount), 2) AS total_discounts,
    ROUND(SUM(s.net_sales), 2) AS net_revenue,
    ROUND(SUM(s.profit_amount), 2) AS total_profit
FROM fact_sales s
LEFT JOIN dim_promotion p
    ON s.promotion_id = p.promotion_id
GROUP BY
    p.promotion_id,
    p.promotion_name,
    p.promotion_type
ORDER BY net_revenue DESC;
