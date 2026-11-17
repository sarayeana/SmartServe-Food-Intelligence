
"""
SmartServe Food Intelligence
Module: forecasting.py

Purpose:
Prepare daily demand data and generate historical demand features
required by the trained forecasting model.

Features:
- Daily store-product demand aggregation
- Historical lag features
- Historical rolling mean features
- Missing-value indicators

Usage:
    from src.forecasting import aggregate_daily_demand

    daily_demand = aggregate_daily_demand(
        sales_data,
        date_data
    )

Run:
    .venv\Scripts\python.exe -m src.forecasting
"""

from pathlib import Path

import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)


def aggregate_daily_demand(
    sales_data: pd.DataFrame,
    date_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Aggregate transaction-level sales into daily
    store-product demand.

    Args:
        sales_data: Transaction-level sales records.
        date_data: Date dimension containing date_id and full_date.

    Returns:
        pd.DataFrame: Daily demand by date, store, and product.

    Raises:
        ValueError: If required columns are missing.
    """

    required_sales_columns = {
        "date_id",
        "store_id",
        "product_id",
        "quantity"
    }

    required_date_columns = {
        "date_id",
        "full_date"
    }

    missing_sales = (
        required_sales_columns - set(sales_data.columns)
    )

    missing_dates = (
        required_date_columns - set(date_data.columns)
    )

    if missing_sales:
        raise ValueError(
            f"Sales dataset missing columns: {sorted(missing_sales)}"
        )

    if missing_dates:
        raise ValueError(
            f"Date dataset missing columns: {sorted(missing_dates)}"
        )

    logger.info("Starting daily demand aggregation")

    daily_demand = (
        sales_data
        .groupby(
            ["date_id", "store_id", "product_id"],
            as_index=False
        )
        .agg(
            sales_qty=("quantity", "sum")
        )
    )

    daily_demand = daily_demand.merge(
        date_data[["date_id", "full_date"]],
        on="date_id",
        how="left",
        validate="many_to_one"
    )

    daily_demand["full_date"] = pd.to_datetime(
        daily_demand["full_date"]
    )

    if daily_demand["full_date"].isna().any():
        raise ValueError(
            "Some daily demand records have unmatched dates."
        )

    daily_demand = daily_demand.sort_values(
        ["store_id", "product_id", "full_date"]
    ).reset_index(drop=True)

    logger.info(
        "Daily demand aggregation completed: %s records",
        len(daily_demand)
    )

    return daily_demand


def create_historical_demand_features(
    daily_demand: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate historical lag and rolling demand features.

    Historical features are calculated independently for
    each store-product combination.

    Args:
        daily_demand: Daily demand dataset.

    Returns:
        pd.DataFrame: Daily demand with historical features.
    """

    required_columns = {
        "store_id",
        "product_id",
        "full_date",
        "sales_qty"
    }

    missing_columns = (
        required_columns - set(daily_demand.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    logger.info("Creating historical demand features")

    featured_data = daily_demand.copy()

    featured_data["full_date"] = pd.to_datetime(
        featured_data["full_date"]
    )

    featured_data = featured_data.sort_values(
        ["store_id", "product_id", "full_date"]
    ).reset_index(drop=True)

    grouped_sales = featured_data.groupby(
        ["store_id", "product_id"]
    )["sales_qty"]

    # Historical lag features
    for lag in [1, 7, 14, 28]:

        column_name = f"sales_lag_{lag}"

        featured_data[column_name] = (
            grouped_sales.shift(lag)
        )

        featured_data[f"{column_name}_missing"] = (
            featured_data[column_name].isna().astype(int)
        )

    # Historical rolling mean features
    for window in [7, 14, 28]:

        column_name = f"sales_rolling_mean_{window}"

        featured_data[column_name] = (
            featured_data
            .groupby(["store_id", "product_id"])["sales_qty"]
            .transform(
                lambda series: (
                    series.shift(1)
                    .rolling(window=window, min_periods=window)
                    .mean()
                )
            )
        )

        featured_data[f"{column_name}_missing"] = (
            featured_data[column_name].isna().astype(int)
        )

    logger.info(
        "Historical demand feature generation completed"
    )

    return featured_data




def prepare_deployment_features(
    forecasting_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Prepare raw forecasting data for model feature engineering.

    Calculate store operating days and remove identifiers,
    target columns, and unused date columns.
    """

    logger.info("Preparing deployment model features")

    data = forecasting_data.copy()

    required_columns = [
        "full_date",
        "opening_date"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing deployment columns: {missing_columns}"
        )

    data["full_date"] = pd.to_datetime(
        data["full_date"],
        errors="coerce"
    )

    data["opening_date"] = pd.to_datetime(
        data["opening_date"],
        errors="coerce"
    )

    if (
        data["full_date"].isna().any()
        or data["opening_date"].isna().any()
    ):
        raise ValueError(
            "Invalid or missing date values found."
        )

    data["store_operating_days"] = (
        data["full_date"] - data["opening_date"]
    ).dt.days

    excluded_columns = [
        "date_id",
        "full_date",
        "store_id",
        "product_id",
        "sales_qty",
        "opening_date",
        "weather_weather_id"
    ]

    model_features = data.drop(
        columns=excluded_columns,
        errors="ignore"
    )

    if model_features.columns.duplicated().any():
        raise ValueError(
            "Duplicate feature columns found."
        )

    logger.info(
        "Deployment features prepared | Records: %s | Features: %s",
        len(model_features),
        len(model_features.columns)
    )

    return model_features


def main() -> None:
    """
    Validate that the forecasting module can be imported.
    """

    logger.info("Forecasting module is ready for use.")

    print("SMARTSERVE FORECASTING MODULE")
    print("=" * 55)
    print("Daily demand aggregation function available.")
    print("FORECASTING MODULE VALIDATION COMPLETED")


if __name__ == "__main__":
    main()
