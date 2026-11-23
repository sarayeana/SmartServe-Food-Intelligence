# SmartServe — SQL Analytics

## 1. Overview

The SmartServe SQL Analytics component uses **MySQL** to store, validate, and analyze food-service sales and operational data.

It transforms the project's CSV datasets into a relational database and uses SQL queries to investigate business performance, including:

- Sales and revenue performance
- Store performance
- Product and category performance
- Inventory and stock management
- Food waste analysis
- Demand forecasting performance
- Store-product forecasting risks

The database supports the wider SmartServe Food Intelligence project, which combines Python, Machine Learning, SQL, Excel, and Power BI.

## 2. Technology Stack

- Database: MySQL
- Database management: MySQL Workbench
- Programming language: Python
- Database connector: mysql-connector-python
- Data processing: pandas
- Data format: CSV
- SQL features: Joins, aggregations, CTEs, window functions, ranking, and data validation

## 3. Database Structure

Database name: `smartserve_db`

The database contains 11 original data tables and one additional forecasting analytics table.

### Dimension tables

| Table | Description |
|---|---|
| dim_date | Calendar and date attributes |
| dim_store | Store information and locations |
| dim_product | Product details, categories, and pricing |
| dim_customer | Customer segments and loyalty information |
| dim_promotion | Promotion details and discount information |
| dim_holiday | Holiday information |
| dim_weather | Daily weather conditions by store |

### Fact tables

| Table | Description |
|---|---|
| fact_sales | Transaction-level sales records |
| fact_inventory | Daily inventory and stock movement |
| fact_preparation | Planned versus actual food preparation |
| fact_waste | Recorded food waste and associated costs |

### Forecasting analytics table

| Table | Description |
|---|---|
| forecast_performance | Historical actual demand, predicted demand, and forecasting errors |

The forecasting table connects to the date, store, and product dimensions through foreign keys.

## 4. Project Data

The database uses the project's generated CSV datasets.

Source directory:

`data/raw/`

The forecasting analytics data is loaded from:

`data/processed/business_intelligence/forecast_performance.csv`

### Dataset coverage

| Dataset | Records |
|---|---:|
| dim_date | 90 |
| dim_store | 5 |
| dim_product | 20 |
| dim_customer | 1,000 |
| dim_promotion | 8 |
| dim_holiday | 8 |
| dim_weather | 450 |
| fact_sales | 122,318 |
| fact_inventory | 9,000 |
| fact_preparation | 9,000 |
| fact_waste | 3,648 |
| forecast_performance | 9,000 |

Historical data covers January 1, 2025, through March 31, 2025.

## 5. Folder Structure

```text
sql/
│
├── README.md
├── create_database.sql
├── schema.sql
├── load_data.py
├── validate_database.py
├── create_analytics_tables.sql
├── load_forecast_data.py
│
└── queries/
    ├── 01_sales_analysis.sql
    ├── 02_store_performance.sql
    ├── 03_product_performance.sql
    ├── 04_inventory_analysis.sql
    ├── 05_food_waste_analysis.sql
    ├── 06_forecast_performance.sql
    └── 07_forecast_data_validation.sql
```

## 6. Database Setup

### Step 1 — Create the database

Open MySQL Workbench and execute:

`create_database.sql`

This creates the `smartserve_db` database.

### Step 2 — Create the database schema

Execute:

`schema.sql`

This creates the 11 dimension and fact tables, including their primary keys, foreign keys, and indexes.

### Step 3 — Load the original datasets

From the project root directory, execute:

```cmd
.venv\Scripts\python.exe sql\load_data.py
```

The script loads the CSV files from `data/raw/` into their corresponding MySQL tables.

The loader inserts dimension tables before fact tables to respect foreign-key dependencies.

### Step 4 — Validate the database

Execute:

```cmd
.venv\Scripts\python.exe sql\validate_database.py
```

The validation script checks expected record counts, table availability, primary-key nulls, and duplicate primary keys.

### Step 5 — Create the forecasting analytics table

Open MySQL Workbench and execute:

`create_analytics_tables.sql`

This creates the `forecast_performance` table and its relationships with the date, store, and product dimensions.

### Step 6 — Load forecasting records

From the project root directory, execute:

```cmd
.venv\Scripts\python.exe sql\load_forecast_data.py
```

The script loads the historical forecasting records from the processed business intelligence dataset.

### Step 7 — Validate forecasting data

Execute the queries in:

`queries/07_forecast_data_validation.sql`

These queries check date, store, and product coverage, missing values, and duplicate store-product-date combinations.

## 7. SQL Business Analysis

The project contains seven SQL analysis files.

### 01 — Sales Analysis

File: `queries/01_sales_analysis.sql`

Analysis includes:

- Overall sales KPIs
- Monthly sales performance
- Daily sales trends
- Payment method analysis
- Promotion performance

Key findings:

- Net revenue: 49,384,617.90
- Total profit: 25,486,012.90
- Profit margin: 51.61%
- Average order value: 403.74
- March generated the highest monthly revenue.

### 02 — Store Performance

File: `queries/02_store_performance.sql`

Analysis includes:

- Overall store performance
- Store revenue and profit rankings
- Monthly store performance
- Weekday versus weekend performance

Key findings:

- ST004 generated the highest revenue and profit.
- ST003 had the lowest revenue and profit.
- All five stores generated higher average daily revenue on weekends.

### 03 — Product Performance

File: `queries/03_product_performance.sql`

Analysis includes:

- Product-level sales and profitability
- Product revenue and profit rankings
- Category performance
- Monthly category performance

Key findings:

- Beef Burger generated the highest product revenue.
- Mocha generated the highest total product profit.
- Cappuccino recorded the highest units sold.
- Beverage products contributed the largest category revenue.
- Food had the lowest category profit margin.

### 04 — Inventory Analysis

File: `queries/04_inventory_analysis.sql`

Analysis includes:

- Inventory movement and stock reconciliation
- Stockout analysis
- Planned versus actual preparation
- Damaged and expired inventory analysis

Key findings:

- Inventory movement reconciled across opening stock, receipts, preparation, sales, and closing stock.
- No stockout events were recorded in the inventory dataset.
- Actual preparation exceeded planned preparation across the analyzed store-product combinations.
- The inventory damage and expiry fields contained zero recorded quantities.

Note: Zero stockout, damage, or expiry values in these particular fields should not be interpreted as proof that shortages or waste never occurred. Food waste is recorded separately in `fact_waste`.

### 05 — Food Waste Analysis

File: `queries/05_food_waste_analysis.sql`

Analysis includes:

- Overall waste KPIs
- Waste by reason
- Waste by store
- Waste by product
- Monthly waste trends

Key findings:

- Total recorded waste: 11,687 units.
- Total recorded waste cost: 951,885.00.
- Overproduction represented 94.49% of recorded waste cost.
- ST004 had the highest store-level waste cost.
- March had the highest monthly waste cost.

### 06 — Forecast Performance

File: `queries/06_forecast_performance.sql`

Analysis includes:

- Overall forecast performance
- Forecast performance by store
- Forecast performance by product
- Forecast error types
- Forecast performance by demand level
- Monthly forecast performance
- Store-product forecast performance
- Highest underprediction risk

Key findings:

- Historical prediction MAE: 8.21 units.
- Historical prediction RMSE: 10.61 units.
- Very high demand had the highest MAE at 19.31 units.
- ST003 had the lowest store-level MAE.
- ST004 had the highest store-level MAE.
- Several beverage products at ST004 and ST001 showed repeated underprediction.

### 07 — Forecast Data Validation

File: `queries/07_forecast_data_validation.sql`

Validation includes:

- Total forecasting records
- Date, store, and product coverage
- Missing values
- Duplicate date-store-product combinations

Validation confirmed 9,000 records covering 90 dates, five stores, and 20 products, with no missing key or prediction values and no duplicate combinations.

## 8. Key SQL Techniques Demonstrated

The SQL component demonstrates practical relational database and analytical SQL skills:

- Database and table creation
- Primary and foreign keys
- Index creation
- Data loading and validation
- INNER JOIN operations
- GROUP BY and aggregate functions
- Common Table Expressions (CTEs)
- Window functions
- DENSE_RANK()
- Conditional aggregation
- CASE expressions
- Date-based analysis
- Forecast error calculations
- Data integrity checks

## 9. Overall Business Insights

The SQL analysis identifies several operational priorities:

1. Improve preparation planning for high- and very-high-demand periods.
2. Investigate forecasting weaknesses at ST004 and ST001.
3. Maintain sufficient inventory for high-revenue products.
4. Reduce overproduction to address the largest source of recorded food waste.
5. Adjust staffing and preparation capacity to accommodate higher weekend revenue.
6. Monitor product profitability alongside revenue and sales volume.

## 10. Important Analytical Limitations

- The dataset covers only three months, so findings should not be treated as evidence of long-term seasonality.
- The forecasting evaluation uses historical prediction records from January–March 2025, not an independent future holdout period.
- Recorded zero stockout, damaged, and expired inventory values do not establish that no operational losses occurred.
- Promotion revenue does not establish incremental promotional impact without a suitable comparison group.
- Forecast-based inventory recommendations require operational validation before implementation.

## 11. Reproducibility

To reproduce the SQL workflow:

1. Install and configure MySQL.
2. Install the project's Python dependencies.
3. Create the database.
4. Execute the database schema.
5. Load the original CSV datasets.
6. Run database validation.
7. Create the forecasting analytics table.
8. Load forecasting records.
9. Run forecasting data validation.
10. Execute the seven SQL analysis files in MySQL Workbench.

All Python commands should be executed from the project root directory with the project virtual environment.
