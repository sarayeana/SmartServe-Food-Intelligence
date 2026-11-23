
USE smartserve_db;

-- ============================================================
-- 1. OVERALL FORECAST PERFORMANCE
-- ============================================================

SELECT
    COUNT(*) AS total_predictions,

    ROUND(AVG(ABS(prediction_error)), 2) AS mae,

    ROUND(
        SQRT(AVG(POWER(prediction_error, 2))),
        2
    ) AS rmse,

    ROUND(AVG(prediction_error), 2) AS mean_prediction_error,

    ROUND(
        AVG(ABS(prediction_error))
        / NULLIF(AVG(actual_sales_qty), 0) * 100,
        2
    ) AS mae_as_percentage_of_average_actual

FROM forecast_performance;


-- ============================================================
-- 2. FORECAST PERFORMANCE BY STORE
-- ============================================================

SELECT
    fp.store_id,
    s.store_name,

    COUNT(*) AS total_predictions,

    ROUND(AVG(ABS(fp.prediction_error)), 2) AS mae,

    ROUND(
        SQRT(AVG(POWER(fp.prediction_error, 2))),
        2
    ) AS rmse,

    ROUND(AVG(fp.prediction_error), 2) AS mean_prediction_error,

    ROUND(
        AVG(ABS(fp.prediction_error))
        / NULLIF(AVG(fp.actual_sales_qty), 0) * 100,
        2
    ) AS mae_percentage

FROM forecast_performance fp

JOIN dim_store s
    ON fp.store_id = s.store_id

GROUP BY
    fp.store_id,
    s.store_name

ORDER BY mae ASC;



-- ============================================================
-- 3. FORECAST PERFORMANCE BY PRODUCT
-- ============================================================

SELECT
    fp.product_id,
    p.product_name,
    p.category,

    COUNT(*) AS total_predictions,

    ROUND(AVG(ABS(fp.prediction_error)), 2) AS mae,

    ROUND(
        SQRT(AVG(POWER(fp.prediction_error, 2))),
        2
    ) AS rmse,

    ROUND(AVG(fp.prediction_error), 2) AS mean_prediction_error,

    ROUND(
        AVG(ABS(fp.prediction_error))
        / NULLIF(AVG(fp.actual_sales_qty), 0) * 100,
        2
    ) AS mae_percentage

FROM forecast_performance fp

JOIN dim_product p
    ON fp.product_id = p.product_id

GROUP BY
    fp.product_id,
    p.product_name,
    p.category

ORDER BY mae ASC;



-- ============================================================
-- 4. FORECAST ERROR TYPE ANALYSIS
-- ============================================================

SELECT
    error_type,

    COUNT(*) AS prediction_records,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM forecast_performance),
        2
    ) AS percentage_of_predictions,

    ROUND(AVG(ABS(prediction_error)), 2) AS average_absolute_error,

    ROUND(AVG(prediction_error), 2) AS average_prediction_error,

    ROUND(SUM(ABS(prediction_error)), 2) AS total_absolute_error

FROM forecast_performance

GROUP BY error_type

ORDER BY prediction_records DESC;




-- ============================================================
-- QUERY 5: FORECAST PERFORMANCE BY DEMAND LEVEL
-- ============================================================

SELECT
    demand_level,
    COUNT(*) AS total_predictions,
    ROUND(AVG(actual_sales_qty), 2) AS average_actual_demand,
    ROUND(AVG(predicted_sales_qty), 2) AS average_predicted_demand,
    ROUND(AVG(ABS(prediction_error)), 2) AS mae,
    ROUND(
        SQRT(AVG(POWER(prediction_error, 2))),
        2
    ) AS rmse,
    ROUND(AVG(prediction_error), 2) AS mean_prediction_error

FROM forecast_performance

GROUP BY demand_level

ORDER BY
    CASE demand_level
        WHEN 'Very Low' THEN 1
        WHEN 'Low' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'High' THEN 4
        WHEN 'Very High' THEN 5
        ELSE 6
    END;


-- ============================================================
-- QUERY 6: MONTHLY FORECAST PERFORMANCE
-- ============================================================

SELECT
    MONTH(full_date) AS month_number,
    MONTHNAME(full_date) AS month_name,
    COUNT(*) AS total_predictions,
    ROUND(AVG(actual_sales_qty), 2) AS average_actual_demand,
    ROUND(AVG(predicted_sales_qty), 2) AS average_predicted_demand,
    ROUND(AVG(ABS(prediction_error)), 2) AS mae,
    ROUND(
        SQRT(AVG(POWER(prediction_error, 2))),
        2
    ) AS rmse,
    ROUND(AVG(prediction_error), 2) AS mean_prediction_error

FROM forecast_performance

GROUP BY
    MONTH(full_date),
    MONTHNAME(full_date)

ORDER BY month_number;


-- ============================================================
-- QUERY 7: STORE AND PRODUCT FORECAST PERFORMANCE
-- ============================================================

SELECT
    fp.store_id,
    s.store_name,
    fp.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS total_predictions,
    ROUND(AVG(ABS(fp.prediction_error)), 2) AS mae,
    ROUND(
        SQRT(AVG(POWER(fp.prediction_error, 2))),
        2
    ) AS rmse,
    ROUND(AVG(fp.prediction_error), 2) AS mean_prediction_error

FROM forecast_performance fp

JOIN dim_store s
    ON fp.store_id = s.store_id

JOIN dim_product p
    ON fp.product_id = p.product_id

GROUP BY
    fp.store_id,
    s.store_name,
    fp.product_id,
    p.product_name,
    p.category

ORDER BY mae DESC

LIMIT 20;


-- ============================================================
-- QUERY 8: HIGHEST UNDERPREDICTION RISK
-- ============================================================

SELECT
    fp.store_id,
    s.store_name,
    fp.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS total_predictions,

    SUM(
        CASE
            WHEN fp.error_type = 'Underprediction'
            THEN 1
            ELSE 0
        END
    ) AS underprediction_records,

    ROUND(
        AVG(
            CASE
                WHEN fp.prediction_error < 0
                THEN ABS(fp.prediction_error)
                ELSE 0
            END
        ),
        2
    ) AS average_underprediction_per_record,

    ROUND(
        AVG(fp.prediction_error),
        2
    ) AS mean_prediction_error,

    ROUND(
        SUM(
            CASE
                WHEN fp.prediction_error < 0
                THEN ABS(fp.prediction_error)
                ELSE 0
            END
        ),
        2
    ) AS total_underprediction_units

FROM forecast_performance fp

JOIN dim_store s
    ON fp.store_id = s.store_id

JOIN dim_product p
    ON fp.product_id = p.product_id

GROUP BY
    fp.store_id,
    s.store_name,
    fp.product_id,
    p.product_name,
    p.category

HAVING underprediction_records > 0

ORDER BY total_underprediction_units DESC

LIMIT 20;
