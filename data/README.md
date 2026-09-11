# SmartServe Data Directory

This directory contains the datasets used throughout the SmartServe Food Intelligence project.

The data is organized into three stages:

```text
raw
 ↓
processed
 ↓
ml
```

---

## 1. Raw Data

The `raw/` directory contains the original generated operational datasets before cleaning and preprocessing.

Expected datasets include:

* `dim_date.csv`
* `dim_store.csv`
* `dim_product.csv`
* `dim_customer.csv`
* `dim_promotion.csv`
* `dim_holiday.csv`
* `dim_weather.csv`
* `fact_sales.csv`
* `fact_preparation.csv`
* `fact_inventory.csv`
* `fact_waste.csv`

These datasets will be generated using the project's Python data-generation pipeline.

Raw data should not be manually modified.

---

## 2. Processed Data

The `processed/` directory contains cleaned and standardized datasets.

Typical processing steps include:

* Data type correction
* Missing-value handling
* Duplicate removal
* Category standardization
* Invalid-value handling
* Date standardization
* Referential integrity checks
* Business-rule validation

The processed datasets will be used for SQL analysis, exploratory analysis, and downstream modeling.

---

## 3. Machine Learning Data

The `ml/` directory contains datasets prepared specifically for machine learning.

Expected datasets include:

* `demand_features.csv`
* `waste_features.csv`

These datasets will contain engineered features required for:

* Demand forecasting
* Waste-risk prediction
* Inventory optimization

Machine-learning datasets will be generated from validated and processed operational data.

---

## Data Generation Strategy

The SmartServe dataset is a realistic synthetic operational dataset designed to simulate a multi-store food service business.

The data-generation process will model relationships between:

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

The dataset will first be generated at a small prototype scale for validation.

### Prototype

* 5 stores
* 20 products
* 1,000 customers
* 3 months of data

After the business rules and relationships are validated, the dataset will be scaled to the final project size.

### Final Dataset

* 15 stores
* 80 products
* Approximately 50,000 customers
* 2022–2026 project period

The final row counts of the fact tables will depend on the realistic generation logic rather than an arbitrary target.

---

## Data Quality

The raw dataset may contain controlled data-quality issues to simulate real-world operational data.

Examples include:

* Missing values
* Duplicate records
* Inconsistent text categories
* Invalid numeric values
* Date-format inconsistencies
* Referential integrity issues
* Business-rule violations

These issues will be identified during the data-quality phase and addressed during preprocessing.

---

## Important

The raw, processed, and machine-learning datasets should be treated as different stages of the data pipeline.

```text
Raw Data
   ↓
Validation
   ↓
Preprocessing
   ↓
Processed Data
   ↓
Feature Engineering
   ↓
ML Data
```

This separation makes the project reproducible, auditable, and easier to maintain.
