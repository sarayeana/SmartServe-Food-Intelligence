import random

import pandas as pd

from src.config import CONFIG, DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory, set_random_seed


logger = get_logger(__name__)


def generate_preparation() -> pd.DataFrame:
    """
    Generate the SmartServe preparation fact table.

    Preparation is generated at store/product/date level by
    aggregating actual sales and applying realistic planning
    variation.

    Returns:
        DataFrame containing preparation information.
    """

    logger.info("Starting preparation data generation")

    set_random_seed(RANDOM_SEED)

    sales = pd.read_csv(DATA_RAW / "fact_sales.csv")
    products = pd.read_csv(DATA_RAW / "dim_product.csv")

    # Aggregate sales to store/product/date level.
    daily_sales = (
        sales.groupby(
            ["date_id", "store_id", "product_id"],
            as_index=False
        )["quantity"]
        .sum()
        .rename(columns={"quantity": "sold_qty"})
    )

    # Add product cost and preparation time.
    daily_sales = daily_sales.merge(
        products[
            [
                "product_id",
                "unit_cost",
                "preparation_time",
            ]
        ],
        on="product_id",
        how="left",
    )

    records = []

    preparation_id = 1

    for _, row in daily_sales.iterrows():

        sold_qty = int(row["sold_qty"])

        # Managers do not perfectly predict demand.
        planning_factor = random.uniform(
            0.85,
            1.25,
        )

        planned_qty = max(
            1,
            int(round(sold_qty * planning_factor))
        )

        # Actual preparation can differ slightly
        # from the planned quantity.
        execution_factor = random.uniform(
            0.95,
            1.10,
        )

        actual_qty = max(
            1,
            int(round(planned_qty * execution_factor))
        )

        preparation_cost = (
            actual_qty * float(row["unit_cost"])
        )

        preparation_time = (
            actual_qty * float(row["preparation_time"])
        )

        records.append(
            {
                "preparation_id": f"PREP{preparation_id:08d}",
                "date_id": int(row["date_id"]),
                "store_id": row["store_id"],
                "product_id": row["product_id"],
                "planned_qty": planned_qty,
                "actual_qty": actual_qty,
                "preparation_cost": round(
                    preparation_cost,
                    2,
                ),
                "preparation_time_minutes": round(
                    preparation_time,
                    2,
                ),
            }
        )

        preparation_id += 1

    return pd.DataFrame(records)


def main() -> None:
    """Generate and save preparation data."""

    df = generate_preparation()

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "fact_preparation.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    logger.info(
        "Preparation fact table saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s preparation records",
        len(df),
    )

    print(df.head())
    print(f"\nShape: {df.shape}")

    print(
        "\nTotal Planned:",
        df["planned_qty"].sum(),
    )

    print(
        "Total Prepared:",
        df["actual_qty"].sum(),
    )


if __name__ == "__main__":
    main()
