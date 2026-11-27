# SmartServe Food Intelligence

**An End-to-End Food Service Analytics, Demand Forecasting & Business Intelligence Project**

## Project Overview

SmartServe Food Intelligence is an end-to-end data analytics and machine learning project designed to improve operational decision-making in a multi-store food service business.

The project integrates Python, SQL, Machine Learning, Excel, and Power BI to analyze sales and operational performance, understand demand patterns, evaluate food waste, forecast product demand, and generate inventory recommendations.

Using a synthetic operational dataset representing five food service stores, the project demonstrates how data-driven insights can support revenue growth, inventory planning, demand management, and operational efficiency.

## Business Problem

Food service businesses face several interconnected operational challenges:

- Over-preparation can lead to excess inventory and food waste.
- Under-preparation can result in stockouts and missed sales opportunities.
- Demand varies across products, stores, weekdays, promotions, holidays, and weather conditions.
- Poor inventory planning can increase operational costs.
- Managers need reliable performance indicators to make informed decisions.

SmartServe addresses these challenges through integrated data analysis, demand forecasting, inventory recommendations, and business intelligence.

## Project Objectives

The project aims to:

- Analyze sales and operational performance.
- Identify revenue and profitability patterns.
- Evaluate store, product, and customer performance.
- Analyze food waste quantities, reasons, and costs.
- Develop a machine learning model for demand forecasting.
- Evaluate prediction performance across stores and products.
- Generate inventory and safety stock recommendations.
- Translate analytical results into actionable business recommendations.
- Build interactive Excel and Power BI reporting solutions.

## Solution Architecture

The project follows an end-to-end analytics workflow:

```text
Synthetic Data Generation
          ↓
Data Understanding
          ↓
Data Quality Assessment
          ↓
Data Cleaning and Preprocessing
          ↓
Exploratory Data Analysis
          ↓
Feature Engineering
          ↓
Demand Forecasting
          ↓
Model Deployment
          ↓
Inventory Recommendations
          ↓
SQL Business Analysis
          ↓
Excel Analytics
          ↓
Power BI Business Intelligence
          ↓
Business Recommendations
```

## Dataset Overview

The project uses a synthetic operational dataset representing a multi-store food service business.

### Dataset Characteristics

| Attribute | Details |
|---|---|
| Number of Stores | 5 |
| Number of Products | 20 |
| Number of Customers | 1,000 |
| Dataset Period | January–March 2025 |
| Duration | 90 Days |
| Total Records | 145,547 |

### Dataset Summary

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

### Data Model

The dataset contains interconnected dimension and fact tables representing:

- Stores
- Products
- Customers
- Dates
- Promotions
- Holidays
- Weather
- Sales
- Inventory
- Preparation
- Food waste

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, preprocessing, analysis and machine learning |
| Pandas & NumPy | Data manipulation and numerical analysis |
| Scikit-learn | Demand forecasting and model evaluation |
| Matplotlib & Seaborn | Exploratory data visualization |
| MySQL | Relational database and business analysis |
| Excel | PivotTable analysis, PivotCharts and interactive dashboard |
| Power BI | Interactive business intelligence dashboards |
| Jupyter Notebook | Analytical workflow and documentation |
| Git & GitHub | Version control and project management |

## Project Implementation

### 1. Data Understanding and Quality

- Examined the structure and relationships of the datasets.
- Assessed missing values, duplicates, and inconsistent records.
- Performed data validation and business-rule checks.
- Prepared datasets for downstream analysis.

### 2. Exploratory Data Analysis

Analyzed:

- Revenue and profitability trends.
- Store performance.
- Product and category performance.
- Customer segments.
- Promotion performance.
- Food waste patterns.
- Inventory and operational performance.

### 3. Demand Forecasting

Developed and evaluated machine learning models to estimate product demand.

The selected model was a Gradient Boosting Regressor.

**Model Performance**

| Metric | Result |
|---|---:|
| Mean Absolute Error (MAE) | 8.29 |
| Root Mean Squared Error (RMSE) | 10.86 |
| R² Score | 0.6391 |

The deployed model evaluation produced:

| Metric | Result |
|---|---:|
| MAE | 8.21 |
| RMSE | 10.61 |
| R² Score | 0.6198 |

The model outputs were used to support demand analysis and inventory recommendations.

*Forecast evaluation covers the January–March 2025 historical period. It should not be interpreted as an independent future-period validation.*

### 4. Model Deployment and Inventory Recommendations

The deployment workflow generates:

- Historical demand predictions.
- Actual versus predicted demand comparisons.
- Store-level forecast performance.
- Product-level forecast performance.
- Recommended stock quantities.
- Safety stock estimates.

Key deployment outputs are exported as CSV files for further analysis and reporting.

### 5. SQL Business Analysis

A MySQL relational database was developed to support structured business analysis.

Implementation includes:

- Database and table creation.
- Primary and foreign key relationships.
- Data loading and validation.
- Analytical SQL queries.
- Sales, store, product, inventory, waste, and forecast analysis.

**Database validation:**
- 11 original operational tables.
- 145,547 records loaded and validated.
- 9,000 forecast performance records loaded.

### 6. Excel Analytics

An Excel analytics workbook was developed using PivotTables, PivotCharts, KPI cards, slicers, and a date timeline.

The workbook includes:

- Executive Dashboard.
- Sales Analysis.
- Store Analysis.
- Product Analysis.
- Waste Analysis.
- Forecast Analysis.

The Executive Dashboard provides interactive business performance reporting with dynamic KPI values and connected analytical filters.

### 7. Power BI Business Intelligence

An interactive Power BI report was developed with six analytical pages:

1. Executive Overview
2. Demand Analysis
3. Forecast Performance
4. Store & Product Analysis
5. Inventory Decision Support
6. Business Recommendations

The dashboard supports business performance monitoring and operational decision-making.

## Key Business Findings

### Sales Performance

| KPI | Result |
|---|---:|
| Total Revenue | ৳49,384,617.90 |
| Total Profit | ৳25,486,012.90 |
| Total Orders | 122,318 |
| Units Sold | 296,663 |
| Profit Margin | 51.61% |
| Average Order Value | ৳403.74 |

### Food Waste Performance

| KPI | Result |
|---|---:|
| Waste Records | 3,648 |
| Waste Units | 11,687 |
| Total Waste Cost | ৳951,885 |
| Overproduction Waste Cost | ৳899,430 |

Overproduction accounts for approximately 94.49% of total recorded waste cost, making it an important area for operational improvement.

### Forecast Performance

| KPI | Result |
|---|---:|
| Forecast Records | 9,000 |
| Mean Absolute Error | 8.21 |
| Root Mean Squared Error | 10.61 |
| Mean Prediction Error | +0.15 |

Forecast performance varies across stores and products, highlighting opportunities for more targeted demand planning.

## Repository Structure

```text
SmartServe-Food-Intelligence/
│
├── config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
│
├── src/
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Data_Quality.ipynb
│   ├── 03_Exploratory_Data_Analysis.ipynb
│   ├── 04_Data_Preprocessing.ipynb
│   ├── 05_Demand_Forecasting_Model_Development.ipynb
│   ├── 06_Model_Deployment_and_Forecasting.ipynb
│   └── 07_Business_Intelligence_and_Decision_Support.ipynb
│
├── sql/
│   ├── README.md
│   ├── schema.sql
│   ├── create_database.sql
│   ├── load_data.py
│   ├── validate_database.py
│   └── queries/
│
├── models/
│
├── excel/
│   └── SmartServe_Excel_Analytics.xlsx
│
├── powerbi/
│   └── SmartServe_Business_Intelligence.pbix
│
├── tests/
│
└── documentation/
```

## Project Deliverables

| Deliverable | Status |
|---|---|
| Synthetic operational datasets | Completed |
| Data understanding and quality assessment | Completed |
| Exploratory data analysis | Completed |
| Data preprocessing | Completed |
| Demand forecasting model | Completed |
| Model deployment workflow | Completed |
| Inventory recommendations | Completed |
| MySQL database and analysis | Completed |
| Excel analytics workbook | Completed |
| Power BI dashboard | Completed |
| Business recommendations | Completed |

## Business Value

SmartServe demonstrates how an integrated analytics solution can help food service businesses:

- Understand revenue and profitability.
- Identify underperforming stores and products.
- Monitor food waste and its financial impact.
- Improve demand planning through predictive modeling.
- Support inventory and safety stock decisions.
- Monitor business performance through interactive dashboards.
- Translate data analysis into operational recommendations.

## Project Limitations

- The dataset is synthetic and represents a simulated business environment.
- Historical forecast evaluation covers the same three-month project period, not an independent future test period.
- Inventory recommendations should be operationally validated before implementation.
- Business impact estimates should be interpreted as analytical decision support rather than measured real-world savings.

## Project Status

**Core project implementation completed.**

The project includes seven analytical notebooks, reusable Python modules, a MySQL database, a demand forecasting and deployment workflow, an Excel analytics workbook, and a six-page Power BI report.

Additional documentation, testing, and portfolio presentation improvements may continue as part of project refinement.

---

**SmartServe Food Intelligence — Turning Operational Data into Business Decisions.**