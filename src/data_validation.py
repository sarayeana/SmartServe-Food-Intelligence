
import pandas as pd

from src.data_loader import load_all_data
from src.logger import get_logger

logger = get_logger(__name__)


def check_missing_values(datasets):
    """Identify missing values in every dataset."""

    print("\n1. MISSING VALUE CHECK")
    print("=" * 65)

    results = []

    for name, df in datasets.items():
        for column in df.columns:
            missing = df[column].isna().sum()

            results.append({
                "dataset": name,
                "column": column,
                "missing_count": missing,
                "missing_percent": round(
                    missing / len(df) * 100, 2
                ) if len(df) else 0,
            })

    report = pd.DataFrame(results)

    print(
        report[report["missing_count"] > 0]
        .to_string(index=False)
    )

    if report["missing_count"].sum() == 0:
        print("No missing values found.")

    return report


def check_duplicates(datasets):
    """Identify duplicate rows and duplicate primary keys."""

    print("\n2. DUPLICATE CHECK")
    print("=" * 65)

    primary_keys = {
    "dim_date": "date_id",
    "dim_store": "store_id",
    "dim_product": "product_id",
    "dim_customer": "customer_id",
    "dim_promotion": "promotion_id",
    "dim_holiday": "holiday_id",
    "dim_weather": "weather_id",
    "fact_sales": "sales_id",
    "fact_preparation": "preparation_id",
    "fact_inventory": "inventory_id",
    "fact_waste": "waste_id",
}

    results = []

    for name, df in datasets.items():

        duplicate_rows = df.duplicated().sum()

        key = primary_keys.get(name)

        duplicate_keys = (
            df[key].duplicated().sum()
            if key and key in df.columns
            else None
        )

        results.append({
            "dataset": name,
            "duplicate_rows": duplicate_rows,
            "duplicate_primary_keys": duplicate_keys,
        })

    report = pd.DataFrame(results)
    print(report.to_string(index=False))

    return report


def check_data_types(datasets):
    """Inspect data types and flag unexpected types."""

    print("\n3. DATA TYPE CHECK")
    print("=" * 65)

    for name, df in datasets.items():

        print(f"\n{name.upper()}")

        print(
            pd.DataFrame({
                "column": df.columns,
                "data_type": df.dtypes.astype(str).values,
            }).to_string(index=False)
        )


def check_invalid_values(datasets):
    """Check important numerical and categorical constraints."""

    print("\n4. INVALID VALUE CHECK")
    print("=" * 65)

    sales = datasets["fact_sales"]
    products = datasets["dim_product"]
    preparation = datasets["fact_preparation"]
    inventory = datasets["fact_inventory"]
    waste = datasets["fact_waste"]

    checks = {
        "Sales quantity <= 0": (sales["quantity"] <= 0).sum(),
        "Negative selling price": (sales["unit_price"] < 0).sum(),
        "Negative discount": (sales["discount_amount"] < 0).sum(),
        "Negative net sales": (sales["net_sales"] < 0).sum(),
        "Negative product cost": (products["unit_cost"] < 0).sum(),
        "Non-positive shelf life": (products["shelf_life_hours"] <= 0).sum(),
        "Non-positive preparation time": (products["preparation_time"] <= 0).sum(),
        "Negative planned quantity": (preparation["planned_qty"] < 0).sum(),
        "Negative actual quantity": (preparation["actual_qty"] < 0).sum(),
        "Negative inventory": (
            inventory[
                [
                    "opening_stock",
                    "received_qty",
                    "prepared_qty",
                    "sold_qty",
                    "closing_stock",
                ]
            ] < 0
        ).sum().sum(),
        "Non-positive waste quantity": (
            waste["quantity_wasted"] <= 0
        ).sum(),
        "Negative waste cost": (waste["waste_cost"] < 0).sum(),
    }

    for description, count in checks.items():
        status = "PASS" if count == 0 else "FAIL"
        print(f"{status} | {description}: {count}")

    return checks


def check_referential_integrity(datasets):
    """Check fact table references against dimension tables."""

    print("\n5. REFERENTIAL INTEGRITY CHECK")
    print("=" * 65)

    relationships = [
        ("fact_sales", "date_id", "dim_date", "date_id"),
        ("fact_sales", "store_id", "dim_store", "store_id"),
        ("fact_sales", "product_id", "dim_product", "product_id"),
        ("fact_sales", "customer_id", "dim_customer", "customer_id"),
        ("fact_preparation", "date_id", "dim_date", "date_id"),
        ("fact_preparation", "store_id", "dim_store", "store_id"),
        ("fact_preparation", "product_id", "dim_product", "product_id"),
        ("fact_inventory", "date_id", "dim_date", "date_id"),
        ("fact_inventory", "store_id", "dim_store", "store_id"),
        ("fact_inventory", "product_id", "dim_product", "product_id"),
        ("fact_waste", "date_id", "dim_date", "date_id"),
        ("fact_waste", "store_id", "dim_store", "store_id"),
        ("fact_waste", "product_id", "dim_product", "product_id"),
    ]

    results = []

    for fact, fact_column, dimension, dimension_column in relationships:

        fact_values = datasets[fact][fact_column]
        valid_values = set(datasets[dimension][dimension_column])

        invalid_count = (~fact_values.isin(valid_values)).sum()

        results.append({
            "relationship": f"{fact}.{fact_column} -> {dimension}.{dimension_column}",
            "invalid_references": invalid_count,
            "status": "PASS" if invalid_count == 0 else "FAIL",
        })

    # Promotion IDs are optional, so NULL is permitted.
    sales = datasets["fact_sales"]
    valid_promotions = set(datasets["dim_promotion"]["promotion_id"])

    invalid_promotions = (
        sales["promotion_id"].notna()
        & ~sales["promotion_id"].isin(valid_promotions)
    ).sum()

    results.append({
        "relationship": "fact_sales.promotion_id -> dim_promotion.promotion_id",
        "invalid_references": invalid_promotions,
        "status": "PASS" if invalid_promotions == 0 else "FAIL",
    })

    report = pd.DataFrame(results)
    print(report.to_string(index=False))

    return report


def check_business_rules(datasets):
    """Check consistency of financial and operational calculations."""

    print("\n6. BUSINESS RULE CHECK")
    print("=" * 65)

    sales = datasets["fact_sales"]
    inventory = datasets["fact_inventory"]
    waste = datasets["fact_waste"]

    # Financial calculations.
    gross_difference = (
        sales["gross_sales"]
        - sales["quantity"] * sales["unit_price"]
    ).abs()

    net_difference = (
        sales["net_sales"]
        - (sales["gross_sales"] - sales["discount_amount"])
    ).abs()

    profit_difference = (
        sales["profit_amount"]
        - (sales["net_sales"] - sales["cost_amount"])
    ).abs()

    # Inventory equation before waste is applied.
    inventory_difference = (
        inventory["opening_stock"]
        + inventory["received_qty"]
        + inventory["prepared_qty"]
        - inventory["sold_qty"]
        - inventory["closing_stock"]
    )

    checks = {
        "Gross sales calculation errors": (gross_difference > 0.01).sum(),
        "Net sales calculation errors": (net_difference > 0.01).sum(),
        "Profit calculation errors": (profit_difference > 0.01).sum(),
        "Inventory balance errors before waste": (
            inventory_difference != 0
        ).sum(),
        "Waste cost calculation errors": (
            (
                waste["waste_cost"]
                - waste["quantity_wasted"] * waste["unit_cost"]
            ).abs() > 0.01
        ).sum(),
        "Stockout flag inconsistencies": (
            inventory["stockout_flag"].astype(bool)
            != (
                inventory["sold_qty"]
                > (
                    inventory["opening_stock"]
                    + inventory["received_qty"]
                    + inventory["prepared_qty"]
                )
            )
        ).sum(),
    }

    for description, count in checks.items():
        status = "PASS" if count == 0 else "FAIL"
        print(f"{status} | {description}: {count}")

    return checks


def run_all_checks():
    """Execute all data validation checks."""

    logger.info("Starting SmartServe data validation")

    datasets = load_all_data()

    missing_report = check_missing_values(datasets)
    duplicate_report = check_duplicates(datasets)

    check_data_types(datasets)

    invalid_report = check_invalid_values(datasets)
    integrity_report = check_referential_integrity(datasets)
    business_report = check_business_rules(datasets)

    print("\n" + "=" * 65)
    print("SMARTSERVE DATA VALIDATION SUMMARY")
    print("=" * 65)

    print(
        "Missing values:",
        int(missing_report["missing_count"].sum())
    )

    print(
        "Duplicate rows:",
        int(duplicate_report["duplicate_rows"].sum())
    )

    print(
        "Duplicate primary keys:",
        int(
            duplicate_report["duplicate_primary_keys"]
            .fillna(0).sum()
        )
    )

    print(
        "Invalid-value issues:",
        sum(invalid_report.values())
    )

    print(
        "Referential-integrity issues:",
        int(integrity_report["invalid_references"].sum())
    )

    print(
        "Business-rule issues:",
        sum(business_report.values())
    )

    logger.info("SmartServe data validation completed")

    return {
        "missing": missing_report,
        "duplicates": duplicate_report,
        "invalid_values": invalid_report,
        "referential_integrity": integrity_report,
        "business_rules": business_report,
    }


if __name__ == "__main__":
    run_all_checks()
