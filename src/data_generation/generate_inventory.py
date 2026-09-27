import random

import pandas as pd

from src.config import DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory, set_random_seed


logger = get_logger(__name__)


def generate_inventory() -> pd.DataFrame:
    """
    Generate the SmartServe inventory fact table.

    Inventory is generated at store/product/date level.

    Returns:
        DataFrame containing inventory information.
    """

    logger.info("Starting inventory data generation")

    set_random_seed(RANDOM_SEED)

    dates = pd.read_csv(DATA_RAW / "dim_date.csv")
    stores = pd.read_csv(DATA_RAW / "dim_store.csv")
    products = pd.read_csv(DATA_RAW / "dim_product.csv")

    sales = pd.read_csv(DATA_RAW / "fact_sales.csv")
    preparation = pd.read_csv(
        DATA_RAW / "fact_preparation.csv"
    )

    # Aggregate daily sales.
    daily_sales = (
        sales.groupby(
            ["date_id", "store_id", "product_id"],
            as_index=False
        )["quantity"]
        .sum()
        .rename(columns={"quantity": "sold_qty"})
    )

    # Preparation quantities.
    daily_preparation = preparation[
        [
            "date_id",
            "store_id",
            "product_id",
            "actual_qty",
        ]
    ].rename(
        columns={"actual_qty": "prepared_qty"}
    )

    # Create the complete store/product/date combination.
    base = (
        dates[["date_id"]]
        .merge(stores[["store_id"]], how="cross")
        .merge(products[["product_id"]], how="cross")
    )

    base = base.merge(
        daily_sales,
        on=["date_id", "store_id", "product_id"],
        how="left",
    )

    base = base.merge(
        daily_preparation,
        on=["date_id", "store_id", "product_id"],
        how="left",
    )

    base["sold_qty"] = base["sold_qty"].fillna(0).astype(int)
    base["prepared_qty"] = (
        base["prepared_qty"]
        .fillna(0)
        .astype(int)
    )

    records = []

    previous_closing_stock = {}

    inventory_id = 1

    for _, row in base.sort_values(
        ["store_id", "product_id", "date_id"]
    ).iterrows():

        key = (
            row["store_id"],
            row["product_id"],
        )

        # Establish initial stock for each store/product.
        if key not in previous_closing_stock:
            opening_stock = random.randint(10, 30)
        else:
            opening_stock = previous_closing_stock[key]

        sold_qty = int(row["sold_qty"])
        prepared_qty = int(row["prepared_qty"])

        # Regular replenishment based on expected daily demand.
        expected_receipt = max(
            0,
            int(round(sold_qty * random.uniform(0.50, 1.20)))
        )

        received_qty = expected_receipt

        available_before_sales = (
            opening_stock
            + received_qty
            + prepared_qty
        )

        # Determine whether available inventory can satisfy sales.
        if sold_qty > available_before_sales:
            stockout_flag = True
            closing_stock_before_waste = 0
        else:
            stockout_flag = False
            closing_stock_before_waste = (
                available_before_sales - sold_qty
            )

        records.append(
            {
                "inventory_id": f"INV{inventory_id:08d}",
                "date_id": int(row["date_id"]),
                "store_id": row["store_id"],
                "product_id": row["product_id"],
                "opening_stock": opening_stock,
                "received_qty": received_qty,
                "prepared_qty": prepared_qty,
                "sold_qty": sold_qty,
                "closing_stock": closing_stock_before_waste,
                "damaged_qty": 0,
                "expired_qty": 0,
                "stockout_flag": stockout_flag,
            }
        )

        previous_closing_stock[key] = closing_stock_before_waste

        inventory_id += 1

    return pd.DataFrame(records)


def main() -> None:
    """Generate and save inventory data."""

    df = generate_inventory()

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "fact_inventory.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    logger.info(
        "Inventory fact table saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s inventory records",
        len(df),
    )

    print(df.head())
    print(f"\nShape: {df.shape}")

    print(
        "\nTotal Opening Stock:",
        df["opening_stock"].sum(),
    )

    print(
        "Total Received:",
        df["received_qty"].sum(),
    )

    print(
        "Total Prepared:",
        df["prepared_qty"].sum(),
    )

    print(
        "Total Sold:",
        df["sold_qty"].sum(),
    )

    print(
        "Stockout Records:",
        df["stockout_flag"].sum(),
    )


if __name__ == "__main__":
    main()
