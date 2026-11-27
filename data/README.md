# SmartServe Data Directory

This directory contains the synthetic operational datasets used throughout the SmartServe Food Intelligence project.

The datasets support data understanding, data quality assessment, exploratory data analysis, preprocessing, demand forecasting, inventory optimization, and business intelligence.

## 1. Data Pipeline

The project follows a structured data pipeline:

```text
Raw Data
   ↓
Data Validation
   ↓
Preprocessing
   ↓
Processed Data
   ↓
Feature Engineering
   ↓
Machine Learning and Deployment
   ↓
Business Intelligence
```

## 2. Raw Data

The `raw/` directory contains the original generated operational datasets before cleaning and preprocessing.

The datasets include:

- `dim_date.csv`
- `dim_store.csv`
- `dim_product.csv`
- `dim_customer.csv`
- `dim_promotion.csv`
- `dim_holiday.csv`
- `dim_weather.csv`
- `fact_sales.csv`
- `fact_preparation.csv`
- `fact_inventory.csv`
- `fact_waste.csv`

Raw data is preserved as the original source for reproducibility and validation.

## 3. Processed Data

The `processed/` directory contains datasets prepared through the data cleaning and preprocessing pipeline.

Processing activities include:

- Data type correction
- Missing-value assessment and handling
- Duplicate record detection
- Category standardization
- Date standardization
- Referential integrity validation
- Business-rule validation
- Feature engineering

Processed datasets are used for exploratory analysis, machine learning, SQL analytics, and downstream business intelligence.

## 4. Machine Learning and Deployment Data

The project includes engineered features and model outputs used for demand forecasting and inventory decision support.

The deployment datasets are stored in:

`processed/deployment/`

Key exported files include:

- `historical_demand_predictions.csv`
- `inventory_recommendations.csv`
- `product_forecast_performance.csv`
- `store_forecast_performance.csv`

These datasets support:

- Historical demand prediction analysis
- Actual versus predicted demand comparison
- Forecast performance evaluation
- Store-level and product-level performance analysis
- Inventory and safety stock recommendations

## 5. Dataset Overview

The final synthetic dataset represents a multi-store food service business operating across five stores.

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
| **Total** | **145,547** |

### Dataset Period

- Start date: January 1, 2025
- End date: March 31, 2025
- Duration: 90 days

## 6. Data Generation Strategy

The SmartServe dataset is a realistic synthetic operational dataset designed to simulate the activities of a multi-store food service business.

The data-generation process models relationships between:

```text
Stores
Products
Customers
Promotions
Holidays
Weather
       ↓
     Sales
       ↓
 Preparation
       ↓
 Inventory
       ↓
     Waste
```

The generated datasets contain related operational records and dimensions to support integrated business analysis.

## 7. Data Quality

Data quality was assessed through dedicated validation and preprocessing activities.

The quality checks covered:

- Missing values
- Duplicate records
- Inconsistent categories
- Invalid numeric values
- Date consistency
- Referential integrity
- Business-rule validation

The duplicate-record validation identified zero duplicate rows, and the final business validation reported zero issues.

Data-quality limitations identified during analysis are retained where necessary for consistency across the project's Python, SQL, and Power BI outputs.

## 8. Important

The raw, processed, and deployment datasets represent different stages of the project pipeline.

```text
Raw Data
   ↓
Data Quality Assessment
   ↓
Preprocessing
   ↓
Processed Data
   ↓
Feature Engineering
   ↓
Demand Forecasting
   ↓
Model Deployment
   ↓
Inventory Recommendations
   ↓
Business Intelligence
```

This structure supports reproducibility, traceability, maintainability, and consistent analytical results across the SmartServe project.