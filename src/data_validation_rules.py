
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


# Columns that should not contain negative values
NON_NEGATIVE_COLUMNS = {
    "fact_sales": [
        "quantity",
        "net_sales",
        "cost_amount",
        "profit_amount"
    ],
    "fact_preparation": [
        "planned_qty",
        "actual_qty",
        "preparation_cost",
        "preparation_time_minutes"
    ],
    "fact_inventory": [
        "opening_stock",
        "received_qty",
        "prepared_qty",
        "sold_qty",
        "closing_stock",
        "damaged_qty",
        "expired_qty"
    ],
    "fact_waste": [
        "quantity_wasted",
        "unit_cost",
        "waste_cost"
    ],
    "dim_product": [
        "selling_price",
        "unit_cost",
        "preparation_time"
    ]
}


def validate_non_negative_values(
    data: dict
) -> pd.DataFrame:
    """
    Identify negative values in specified business columns.
    """

    issues = []

    for dataset_name, columns in NON_NEGATIVE_COLUMNS.items():

        if dataset_name not in data:
            continue

        df = data[dataset_name]

        for column in columns:

            if column not in df.columns:
                continue

            invalid_count = int((df[column] < 0).sum())

            if invalid_count > 0:

                issues.append({
                    "dataset": dataset_name,
                    "column": column,
                    "invalid_count": invalid_count
                })

                logger.warning(
                    "%s contains %s negative values in %s.",
                    dataset_name,
                    invalid_count,
                    column
                )

    report = pd.DataFrame(
        issues,
        columns=["dataset", "column", "invalid_count"]
    )

    logger.info(
        "Numerical validation completed. Issues found: %s",
        len(report)
    )

    return report
