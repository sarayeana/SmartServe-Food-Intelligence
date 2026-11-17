
"""
SmartServe Food Intelligence
Module: business_intelligence.py

Purpose:
Load and validate deployment datasets for business
intelligence reporting and Power BI preparation.

Usage:
    from src.business_intelligence import load_bi_datasets

    datasets = load_bi_datasets(project_root)

Run:
    .venv\\Scripts\\python.exe -m src.business_intelligence
"""

from pathlib import Path

import pandas as pd


def load_bi_datasets(project_root):
    """
    Load the four deployment datasets required for BI reporting.

    Parameters
    ----------
    project_root : str or Path
        SmartServe project root directory.

    Returns
    -------
    dict
        Dictionary containing the four loaded DataFrames.
    """

    deployment_dir = (
        Path(project_root)
        / "data"
        / "processed"
        / "deployment"
    )

    file_mapping = {
        "forecast_results": "historical_demand_predictions.csv",
        "store_performance": "store_forecast_performance.csv",
        "product_performance": "product_forecast_performance.csv",
        "inventory_recommendations": "inventory_recommendations.csv"
    }

    datasets = {}

    for dataset_name, filename in file_mapping.items():

        file_path = deployment_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required BI dataset not found: {file_path}"
            )

        dataset = pd.read_csv(file_path)

        if dataset.empty:
            raise ValueError(
                f"BI dataset is empty: {filename}"
            )

        datasets[dataset_name] = dataset

    # Validate historical forecast columns.
    required_forecast_columns = {
        "date_id",
        "full_date",
        "store_id",
        "product_id",
        "actual_sales_qty",
        "predicted_sales_qty"
    }

    missing_columns = (
        required_forecast_columns
        - set(datasets["forecast_results"].columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing forecast columns: {sorted(missing_columns)}"
        )

    # Validate inventory recommendation columns.
    required_inventory_columns = {
        "store_id",
        "product_id",
        "average_daily_demand",
        "safety_stock",
        "recommended_stock"
    }

    missing_columns = (
        required_inventory_columns
        - set(datasets["inventory_recommendations"].columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing inventory columns: {sorted(missing_columns)}"
        )

    # Convert forecast date.
    datasets["forecast_results"]["full_date"] = pd.to_datetime(
        datasets["forecast_results"]["full_date"],
        errors="coerce"
    )

    return datasets


def main():
    """
    Run a basic deployment dataset loading check.
    """

    project_root = Path(__file__).resolve().parent.parent

    datasets = load_bi_datasets(project_root)

    print("SMARTSERVE — BUSINESS INTELLIGENCE DATA VALIDATION")
    print("=" * 65)

    for name, dataset in datasets.items():

        print(f"\nDataset: {name}")
        print("Shape:", dataset.shape)
        print("Missing values:", dataset.isna().sum().sum())

    print("\nBUSINESS INTELLIGENCE DATA LOADING COMPLETED")



def prepare_daily_demand_analysis(forecast_results):
    """
    Aggregate historical actual and predicted demand by date.

    Parameters
    ----------
    forecast_results : pandas.DataFrame
        Historical prediction dataset.

    Returns
    -------
    pandas.DataFrame
        Daily actual demand, predicted demand,
        prediction error, and rolling averages.

    Usage
    -----
    from src.business_intelligence import prepare_daily_demand_analysis

    daily_demand = prepare_daily_demand_analysis(forecast_results)
    """

    required_columns = [
        "full_date",
        "actual_sales_qty",
        "predicted_sales_qty"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in forecast_results.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    daily_demand = (
        forecast_results
        .groupby("full_date", as_index=False)
        .agg(
            actual_demand=("actual_sales_qty", "sum"),
            predicted_demand=("predicted_sales_qty", "sum")
        )
        .sort_values("full_date")
        .reset_index(drop=True)
    )

    daily_demand["prediction_error"] = (
        daily_demand["predicted_demand"]
        - daily_demand["actual_demand"]
    )

    daily_demand["actual_7day_avg"] = (
        daily_demand["actual_demand"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    daily_demand["predicted_7day_avg"] = (
        daily_demand["predicted_demand"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    return daily_demand


if __name__ == "__main__":
    main()
