
-- ============================================================
-- SMARTSERVE FOOD INTELLIGENCE
-- DATABASE SCHEMA
-- MySQL 8.0+
-- ============================================================

USE smartserve_db;

-- ============================================================
-- 1. DIMENSION TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_id VARCHAR(20) PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day INT,
    day_name VARCHAR(20),
    day_of_week INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(100),
    season VARCHAR(50),
    UNIQUE KEY uq_dim_date_full_date (full_date)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_store (
    store_id VARCHAR(20) PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(100),
    area VARCHAR(100),
    store_type VARCHAR(50),
    opening_date DATE,
    seating_capacity INT,
    average_daily_customers INT,
    manager_region VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    size VARCHAR(50),
    unit_cost DECIMAL(12,2),
    selling_price DECIMAL(12,2),
    shelf_life_hours INT,
    preparation_time INT,
    active_flag BOOLEAN
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id VARCHAR(30) PRIMARY KEY,
    signup_date DATE,
    customer_segment VARCHAR(100),
    age_group VARCHAR(50),
    loyalty_member BOOLEAN,
    acquisition_channel VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_promotion (
    promotion_id VARCHAR(30) PRIMARY KEY,
    promotion_name VARCHAR(150),
    promotion_type VARCHAR(100),
    discount_percent DECIMAL(6,2),
    start_date DATE,
    end_date DATE,
    target_category VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_holiday (
    holiday_id VARCHAR(30) PRIMARY KEY,
    holiday_date DATE NOT NULL,
    holiday_name VARCHAR(150),
    holiday_type VARCHAR(100),
    INDEX idx_holiday_date (holiday_date)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_weather (
    weather_id VARCHAR(30) PRIMARY KEY,
    date_id VARCHAR(20) NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    temperature DECIMAL(6,2),
    rainfall DECIMAL(8,2),
    humidity DECIMAL(6,2),
    weather_condition VARCHAR(100),

    CONSTRAINT fk_weather_date
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),

    CONSTRAINT fk_weather_store
        FOREIGN KEY (store_id) REFERENCES dim_store(store_id),

    UNIQUE KEY uq_weather_date_store (date_id, store_id)
) ENGINE=InnoDB;

-- ============================================================
-- 2. FACT TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30),
    date_id VARCHAR(20) NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(30) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    promotion_id VARCHAR(30),
    quantity INT,
    unit_price DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    gross_sales DECIMAL(14,2),
    net_sales DECIMAL(14,2),
    cost_amount DECIMAL(14,2),
    profit_amount DECIMAL(14,2),
    payment_method VARCHAR(50),

    CONSTRAINT fk_sales_date
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),

    CONSTRAINT fk_sales_store
        FOREIGN KEY (store_id) REFERENCES dim_store(store_id),

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),

    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_id) REFERENCES dim_product(product_id),

    CONSTRAINT fk_sales_promotion
        FOREIGN KEY (promotion_id) REFERENCES dim_promotion(promotion_id),

    INDEX idx_sales_date (date_id),
    INDEX idx_sales_store (store_id),
    INDEX idx_sales_product (product_id),
    INDEX idx_sales_customer (customer_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id VARCHAR(30) PRIMARY KEY,
    date_id VARCHAR(20) NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    opening_stock INT,
    received_qty INT,
    prepared_qty INT,
    sold_qty INT,
    closing_stock INT,
    damaged_qty INT,
    expired_qty INT,
    stockout_flag BOOLEAN,

    CONSTRAINT fk_inventory_date
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),

    CONSTRAINT fk_inventory_store
        FOREIGN KEY (store_id) REFERENCES dim_store(store_id),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id) REFERENCES dim_product(product_id),

    INDEX idx_inventory_date (date_id),
    INDEX idx_inventory_store_product (store_id, product_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fact_preparation (
    preparation_id VARCHAR(30) PRIMARY KEY,
    date_id VARCHAR(20) NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    planned_qty INT,
    actual_qty INT,
    preparation_cost DECIMAL(14,2),
    preparation_time_minutes DECIMAL(10,2),

    CONSTRAINT fk_preparation_date
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),

    CONSTRAINT fk_preparation_store
        FOREIGN KEY (store_id) REFERENCES dim_store(store_id),

    CONSTRAINT fk_preparation_product
        FOREIGN KEY (product_id) REFERENCES dim_product(product_id),

    INDEX idx_preparation_date (date_id),
    INDEX idx_preparation_store_product (store_id, product_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fact_waste (
    waste_id VARCHAR(30) PRIMARY KEY,
    date_id VARCHAR(20) NOT NULL,
    store_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    waste_reason_id VARCHAR(100),
    quantity_wasted INT,
    unit_cost DECIMAL(12,2),
    waste_cost DECIMAL(14,2),

    CONSTRAINT fk_waste_date
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),

    CONSTRAINT fk_waste_store
        FOREIGN KEY (store_id) REFERENCES dim_store(store_id),

    CONSTRAINT fk_waste_product
        FOREIGN KEY (product_id) REFERENCES dim_product(product_id),

    INDEX idx_waste_date (date_id),
    INDEX idx_waste_store (store_id),
    INDEX idx_waste_product (product_id)
) ENGINE=InnoDB;
