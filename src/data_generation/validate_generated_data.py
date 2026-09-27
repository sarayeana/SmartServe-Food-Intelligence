from pathlib import Path

import pandas as pd

from src.config import DATA_RAW
from src.logger import get_logger


logger = get_logger(__name__)


EXPECTED_FILES = {
    "dim_date.csv": 90,
    "dim_store.csv": 5,
    "dim_product.csv": 20,
    "dim_customer.csv": 1000,
    "dim_promotion.csv": 8,
    "dim_holiday.csv": 8,
    "dim_weather.csv": 450,
    "fact_sales.csv": None,
    "fact_preparation.csv": None,
    "fact_inventory.csv": 9000,
    "fact_waste.csv": None,
}


def load_csv(filename: str) -> pd.DataFrame:
    """Load a generated CSV file."""

    path = DATA_RAW / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}"
        )

    return pd.read_csv(path)


def check_files_and_rows() -> bool:
    """Check that expected files exist and row counts are valid."""

    print("\n1. FILE AND ROW COUNT CHECK")
    print("-" * 50)

    passed = True

    for filename, expected_rows in EXPECTED_FILES.items():

        try:
            df = load_csv(filename)
            actual_rows = len(df)

            if expected_rows is not None:
                status = actual_rows == expected_rows
            else:
                status = actual_rows > 0

            if status:
                print(
                    f"PASS  {filename:<25} "
                    f"{actual_rows:,} rows"
                )
            else:
                print(
                    f"FAIL  {filename:<25} "
                    f"{actual_rows:,} rows "
                    f"(expected {expected_rows:,})"
                )
                passed = False

        except FileNotFoundError as error:
            print(f"FAIL  {error}")
            passed = False

    return passed


def check_primary_keys() -> bool:
    """Check uniqueness of important dimension keys."""

    print("\n2. PRIMARY KEY CHECK")
    print("-" * 50)

    checks = {
        "dim_date.csv": "date_id",
        "dim_store.csv": "store_id",
        "dim_product.csv": "product_id",
        "dim_customer.csv": "customer_id",
        "dim_promotion.csv": "promotion_id",
        "dim_holiday.csv": "holiday_id",
        "fact_sales.csv": "sales_id",
        "fact_preparation.csv": "preparation_id",
        "fact_inventory.csv": "inventory_id",
        "fact_waste.csv": "waste_id",
    }

    passed = True

    for filename, key in checks.items():

        df = load_csv(filename)

        duplicate_count = df[key].duplicated().sum()

        if duplicate_count == 0:
            print(
                f"PASS  {filename:<25} "
                f"{key} is unique"
            )
        else:
            print(
                f"FAIL  {filename:<25} "
                f"{duplicate_count} duplicate {key} values"
            )
            passed = False

    return passed


def check_foreign_keys() -> bool:
    """Check important relationships between fact and dimension tables."""

    print("\n3. FOREIGN KEY CHECK")
    print("-" * 50)

    dates = load_csv("dim_date.csv")
    stores = load_csv("dim_store.csv")
    products = load_csv("dim_product.csv")
    customers = load_csv("dim_customer.csv")
    promotions = load_csv("dim_promotion.csv")

    sales = load_csv("fact_sales.csv")
    preparation = load_csv("fact_preparation.csv")
    inventory = load_csv("fact_inventory.csv")
    waste = load_csv("fact_waste.csv")

    passed = True

    checks = [
        (
            "Sales → Date",
            sales["date_id"],
            set(dates["date_id"]),
        ),
        (
            "Sales → Store",
            sales["store_id"],
            set(stores["store_id"]),
        ),
        (
            "Sales → Product",
            sales["product_id"],
            set(products["product_id"]),
        ),
        (
            "Sales → Customer",
            sales["customer_id"],
            set(customers["customer_id"]),
        ),
        (
            "Preparation → Date",
            preparation["date_id"],
            set(dates["date_id"]),
        ),
        (
            "Preparation → Store",
            preparation["store_id"],
            set(stores["store_id"]),
        ),
        (
            "Preparation → Product",
            preparation["product_id"],
            set(products["product_id"]),
        ),
        (
            "Inventory → Date",
            inventory["date_id"],
            set(dates["date_id"]),
        ),
        (
            "Inventory → Store",
            inventory["store_id"],
            set(stores["store_id"]),
        ),
        (
            "Inventory → Product",
            inventory["product_id"],
            set(products["product_id"]),
        ),
        (
            "Waste → Date",
            waste["date_id"],
            set(dates["date_id"]),
        ),
        (
            "Waste → Store",
            waste["store_id"],
            set(stores["store_id"]),
        ),
        (
            "Waste → Product",
            waste["product_id"],
            set(products["product_id"]),
        ),
    ]

    for name, values, valid_values in checks:

        invalid = ~values.isin(valid_values)

        invalid_count = invalid.sum()

        if invalid_count == 0:
            print(f"PASS  {name}")
        else:
            print(
                f"FAIL  {name}: "
                f"{invalid_count} invalid values"
            )
            passed = False

    # Promotion can legitimately be NULL.
    valid_promotions = (
        sales["promotion_id"].isna()
        | sales["promotion_id"].isin(
            set(promotions["promotion_id"])
        )
    )

    if valid_promotions.all():
        print("PASS  Sales → Promotion")
    else:
        invalid_count = (~valid_promotions).sum()
        print(
            f"FAIL  Sales → Promotion: "
            f"{invalid_count} invalid values"
        )
        passed = False

    return passed


def check_business_rules() -> bool:
    """Check basic business logic across the generated data."""

    print("\n4. BUSINESS RULE CHECK")
    print("-" * 50)

    sales = load_csv("fact_sales.csv")
    preparation = load_csv("fact_preparation.csv")
    inventory = load_csv("fact_inventory.csv")
    waste = load_csv("fact_waste.csv")

    passed = True

    # Sales quantities must be positive.
    if (sales["quantity"] > 0).all():
        print("PASS  Sales quantities are positive")
    else:
        print("FAIL  Sales contains non-positive quantities")
        passed = False

    # Prices and financial values must not be negative.
    financial_columns = [
        "unit_price",
        "discount_amount",
        "gross_sales",
        "net_sales",
        "cost_amount",
    ]

    for column in financial_columns:

        if (sales[column] >= 0).all():
            print(
                f"PASS  Sales {column} values are valid"
            )
        else:
            print(
                f"FAIL  Sales {column} contains negative values"
            )
            passed = False

    # Preparation quantities.
    if (preparation["planned_qty"] > 0).all():
        print("PASS  Planned preparation quantities are positive")
    else:
        print("FAIL  Invalid planned preparation quantities")
        passed = False

    if (preparation["actual_qty"] > 0).all():
        print("PASS  Actual preparation quantities are positive")
    else:
        print("FAIL  Invalid actual preparation quantities")
        passed = False

    # Inventory quantities cannot be negative.
    inventory_columns = [
        "opening_stock",
        "received_qty",
        "prepared_qty",
        "sold_qty",
        "closing_stock",
    ]

    for column in inventory_columns:

        if (inventory[column] >= 0).all():
            print(
                f"PASS  Inventory {column} values are valid"
            )
        else:
            print(
                f"FAIL  Inventory {column} contains negative values"
            )
            passed = False

    # Waste quantities and costs must be positive.
    if (waste["quantity_wasted"] > 0).all():
        print("PASS  Waste quantities are positive")
    else:
        print("FAIL  Invalid waste quantities")
        passed = False

    if (waste["waste_cost"] >= 0).all():
        print("PASS  Waste costs are valid")
    else:
        print("FAIL  Negative waste costs detected")
        passed = False

    return passed


def print_summary() -> None:
    """Print a concise dataset summary."""

    print("\n5. DATASET SUMMARY")
    print("-" * 50)

    files = [
        "dim_date.csv",
        "dim_store.csv",
        "dim_product.csv",
        "dim_customer.csv",
        "dim_promotion.csv",
        "dim_holiday.csv",
        "dim_weather.csv",
        "fact_sales.csv",
        "fact_preparation.csv",
        "fact_inventory.csv",
        "fact_waste.csv",
    ]

    total_rows = 0

    for filename in files:

        df = load_csv(filename)

        print(
            f"{filename:<25} {len(df):>10,} rows"
        )

        total_rows += len(df)

    print("-" * 50)
    print(
        f"{'TOTAL':<25} {total_rows:>10,} rows"
    )


def main() -> None:
    """Run all prototype data quality checks."""

    logger.info(
        "Starting generated data validation"
    )

    checks = [
        check_files_and_rows(),
        check_primary_keys(),
        check_foreign_keys(),
        check_business_rules(),
    ]

    print_summary()

    if all(checks):
        print("\n" + "=" * 50)
        print("ALL PROTOTYPE DATA CHECKS PASSED")
        print("=" * 50)

        logger.info(
            "All prototype data checks passed"
        )

    else:
        print("\n" + "=" * 50)
        print("SOME DATA CHECKS FAILED")
        print("=" * 50)

        logger.error(
            "One or more prototype data checks failed"
        )


if __name__ == "__main__":
    main()
