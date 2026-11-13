
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


def validate_business_rules(data: dict) -> pd.DataFrame:
    """
    Validate basic SmartServe business rules.
    """

    issues = []

    def record_issue(dataset, rule, count):
        if count > 0:
            issues.append({
                "dataset": dataset,
                "business_rule": rule,
                "invalid_count": int(count)
            })

    # Sales quantity must be positive
    if "fact_sales" in data:
        df = data["fact_sales"]

        if "quantity" in df.columns:
            record_issue(
                "fact_sales",
                "Sales quantity must be greater than zero",
                (df["quantity"] <= 0).sum()
            )

    # Product selling price must be positive
    if "dim_product" in data:
        df = data["dim_product"]

        if "selling_price" in df.columns:
            record_issue(
                "dim_product",
                "Selling price must be greater than zero",
                (df["selling_price"] <= 0).sum()
            )

    # Preparation quantities must be non-negative
    if "fact_preparation" in data:
        df = data["fact_preparation"]

        for column in ["planned_qty", "actual_qty"]:
            if column in df.columns:
                record_issue(
                    "fact_preparation",
                    f"{column} must be non-negative",
                    (df[column] < 0).sum()
                )

    # Inventory closing stock must be non-negative
    if "fact_inventory" in data:
        df = data["fact_inventory"]

        if "closing_stock" in df.columns:
            record_issue(
                "fact_inventory",
                "Closing stock must be non-negative",
                (df["closing_stock"] < 0).sum()
            )

    # Waste quantity must be positive
    if "fact_waste" in data:
        df = data["fact_waste"]

        if "quantity_wasted" in df.columns:
            record_issue(
                "fact_waste",
                "Waste quantity must be greater than zero",
                (df["quantity_wasted"] <= 0).sum()
            )

    report = pd.DataFrame(
        issues,
        columns=[
            "dataset",
            "business_rule",
            "invalid_count"
        ]
    )

    logger.info(
        "Business rule validation completed. Issues found: %s",
        len(report)
    )

    return report
