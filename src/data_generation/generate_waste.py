import random

import pandas as pd

from src.config import DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory, set_random_seed


logger = get_logger(__name__)


def generate_waste() -> pd.DataFrame:
    """
    Generate the SmartServe waste fact table.

    Waste is generated from the relationship between
    preparation, sales, inventory, and product characteristics.

    Returns:
        DataFrame containing waste information.
    """

    logger.info("Starting waste data generation")

    set_random_seed(RANDOM_SEED)

    preparation = pd.read_csv(
        DATA_RAW / "fact_preparation.csv"
    )

    sales = pd.read_csv(
        DATA_RAW / "fact_sales.csv"
    )

    products = pd.read_csv(
        DATA_RAW / "dim_product.csv"
    )

    inventory = pd.read_csv(
        DATA_RAW / "fact_inventory.csv"
    )

    # Aggregate actual sales to store/product/date level.
    daily_sales = (
        sales.groupby(
            ["date_id", "store_id", "product_id"],
            as_index=False
        )["quantity"]
        .sum()
        .rename(columns={"quantity": "sold_qty"})
    )

    # Keep the relevant preparation information.
    prep = preparation[
        [
            "date_id",
            "store_id",
            "product_id",
            "planned_qty",
            "actual_qty",
        ]
    ].rename(
        columns={
            "actual_qty": "prepared_qty"
        }
    )

    # Merge sales with preparation.
    df = prep.merge(
        daily_sales,
        on=[
            "date_id",
            "store_id",
            "product_id",
        ],
        how="left",
    )

    df["sold_qty"] = (
        df["sold_qty"]
        .fillna(0)
        .astype(int)
    )

    # Add product information.
    df = df.merge(
        products[
            [
                "product_id",
                "unit_cost",
                "shelf_life_hours",
            ]
        ],
        on="product_id",
        how="left",
    )

    # Add inventory information.
    df = df.merge(
        inventory[
            [
                "date_id",
                "store_id",
                "product_id",
                "opening_stock",
                "received_qty",
            ]
        ],
        on=[
            "date_id",
            "store_id",
            "product_id",
        ],
        how="left",
    )

    waste_records = []

    waste_id = 1

    for _, row in df.iterrows():

        prepared_qty = int(row["prepared_qty"])
        sold_qty = int(row["sold_qty"])

        # Quantity left after sales.
        surplus_qty = max(
            0,
            prepared_qty - sold_qty
        )

        if surplus_qty <= 0:
            continue

        shelf_life = float(row["shelf_life_hours"])

        waste_qty = 0
        waste_reason = None

        # --------------------------------------------------
        # 1. Overproduction
        # --------------------------------------------------
        # Strong preparation surplus creates avoidable waste.
        if surplus_qty >= max(
            2,
            int(prepared_qty * 0.15)
        ):
            overproduction_rate = random.uniform(
                0.30,
                0.70,
            )

            waste_qty = max(
                1,
                int(round(
                    surplus_qty * overproduction_rate
                ))
            )

            waste_reason = "Overproduction"

        # --------------------------------------------------
        # 2. Expired
        # --------------------------------------------------
        # Short-shelf-life products are more vulnerable
        # to expiration when surplus exists.
        elif surplus_qty > 0 and shelf_life <= 8:
            if random.random() < 0.25:

                expiration_rate = random.uniform(
                    0.20,
                    0.60,
                )

                waste_qty = max(
                    1,
                    int(round(
                        surplus_qty * expiration_rate
                    ))
                )

                waste_reason = "Expired"

        # --------------------------------------------------
        # 3. Damaged
        # --------------------------------------------------
        elif random.random() < 0.05:

            waste_qty = 1
            waste_reason = "Damaged"

        # --------------------------------------------------
        # 4. Preparation Error
        # --------------------------------------------------
        elif random.random() < 0.04:

            waste_qty = 1
            waste_reason = "Preparation Error"

        # --------------------------------------------------
        # 5. Quality Issue
        # --------------------------------------------------
        elif random.random() < 0.03:

            waste_qty = 1
            waste_reason = "Quality Issue"

        if waste_qty <= 0:
            continue

        # Never allow waste to exceed available surplus.
        waste_qty = min(
            waste_qty,
            surplus_qty,
        )

        waste_cost = (
            waste_qty * float(row["unit_cost"])
        )

        waste_records.append(
            {
                "waste_id": f"WST{waste_id:08d}",
                "date_id": int(row["date_id"]),
                "store_id": row["store_id"],
                "product_id": row["product_id"],
                "waste_reason_id": waste_reason,
                "quantity_wasted": waste_qty,
                "unit_cost": float(row["unit_cost"]),
                "waste_cost": round(
                    waste_cost,
                    2,
                ),
            }
        )

        waste_id += 1

    return pd.DataFrame(waste_records)


def main() -> None:
    """Generate and save waste data."""

    df = generate_waste()

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "fact_waste.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    logger.info(
        "Waste fact table saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s waste records",
        len(df),
    )

    print(df.head())

    print(f"\nShape: {df.shape}")

    print(
        "\nTotal Waste Quantity:",
        df["quantity_wasted"].sum(),
    )

    print(
        "Total Waste Cost:",
        round(df["waste_cost"].sum(), 2),
    )

    print("\nWaste by Reason:")

    print(
        df.groupby(
            "waste_reason_id"
        )["quantity_wasted"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


if __name__ == "__main__":
    main()
