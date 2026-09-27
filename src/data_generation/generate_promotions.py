import pandas as pd

from src.config import CONFIG, DATA_RAW
from src.logger import get_logger
from src.utils import ensure_directory


logger = get_logger(__name__)


def generate_promotions(number_of_promotions: int) -> pd.DataFrame:
    """
    Generate the SmartServe promotion dimension.

    Args:
        number_of_promotions: Number of promotions to generate.

    Returns:
        DataFrame containing promotion information.
    """

    logger.info("Generating %s promotions", number_of_promotions)

    promotions = [
        {
            "promotion_id": "PROMO001",
            "promotion_name": "Morning Coffee Deal",
            "promotion_type": "Time-Based",
            "discount_percent": 10,
            "start_date": "2025-01-01",
            "end_date": "2025-01-31",
            "target_category": "Beverage",
        },
        {
            "promotion_id": "PROMO002",
            "promotion_name": "Weekend Special",
            "promotion_type": "Weekend",
            "discount_percent": 15,
            "start_date": "2025-01-10",
            "end_date": "2025-02-28",
            "target_category": "Food",
        },
        {
            "promotion_id": "PROMO003",
            "promotion_name": "Sweet Treats",
            "promotion_type": "Category",
            "discount_percent": 20,
            "start_date": "2025-01-15",
            "end_date": "2025-02-15",
            "target_category": "Dessert",
        },
        {
            "promotion_id": "PROMO004",
            "promotion_name": "Valentine Special",
            "promotion_type": "Seasonal",
            "discount_percent": 25,
            "start_date": "2025-02-10",
            "end_date": "2025-02-16",
            "target_category": "Dessert",
        },
        {
            "promotion_id": "PROMO005",
            "promotion_name": "Ramadan Beverage Offer",
            "promotion_type": "Seasonal",
            "discount_percent": 15,
            "start_date": "2025-03-01",
            "end_date": "2025-03-31",
            "target_category": "Beverage",
        },
        {
            "promotion_id": "PROMO006",
            "promotion_name": "Lunch Combo",
            "promotion_type": "Combo",
            "discount_percent": 12,
            "start_date": "2025-02-01",
            "end_date": "2025-03-15",
            "target_category": "Food",
        },
        {
            "promotion_id": "PROMO007",
            "promotion_name": "New Customer Offer",
            "promotion_type": "Customer",
            "discount_percent": 10,
            "start_date": "2025-01-01",
            "end_date": "2025-03-31",
            "target_category": "All",
        },
        {
            "promotion_id": "PROMO008",
            "promotion_name": "Evening Snack Deal",
            "promotion_type": "Time-Based",
            "discount_percent": 15,
            "start_date": "2025-02-15",
            "end_date": "2025-03-31",
            "target_category": "Food",
        },
    ]

    df = pd.DataFrame(promotions[:number_of_promotions])

    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    return df


def main() -> None:
    """Generate and save the promotion dimension."""

    # We want 8 prototype promotions.
    number_of_promotions = 8

    df = generate_promotions(number_of_promotions)

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "dim_promotion.csv"

    df.to_csv(output_file, index=False)

    logger.info(
        "Promotion dimension saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s promotion records",
        len(df),
    )

    print(df)
    print(f"\nShape: {df.shape}")


if __name__ == "__main__":
    main()
