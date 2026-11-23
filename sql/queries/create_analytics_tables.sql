
USE smartserve_db;

-- ============================================================
-- FORECAST PERFORMANCE ANALYTICS TABLE
-- Column definitions match the existing dimension tables.
-- ============================================================

CREATE TABLE IF NOT EXISTS forecast_performance (
    date_id VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    full_date DATE NOT NULL,
    store_id VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL,
    product_id VARCHAR(20) COLLATE utf8mb4_unicode_ci NOT NULL,

    actual_sales_qty INT NOT NULL,
    predicted_sales_qty DOUBLE NOT NULL,
    prediction_error DOUBLE NOT NULL,
    absolute_error DOUBLE NOT NULL,

    error_type VARCHAR(30),
    demand_level VARCHAR(30),

    INDEX idx_forecast_date (full_date),
    INDEX idx_forecast_store (store_id),
    INDEX idx_forecast_product (product_id),

    CONSTRAINT fk_forecast_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    CONSTRAINT fk_forecast_store
        FOREIGN KEY (store_id)
        REFERENCES dim_store(store_id),

    CONSTRAINT fk_forecast_product
        FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
