import pandas as pd

from src.config import CONFIG, DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory


logger = get_logger(__name__)


def generate_stores(number_of_stores: int) -> pd.DataFrame:
    """
    Generate the SmartServe store dimension.

    Args:
        number_of_stores: Number of stores to generate.

    Returns:
        DataFrame containing store information.
    """

    logger.info("Generating %s stores", number_of_stores)

    cities = [
        "Dhaka",
        "Chattogram",
        "Sylhet",
        "Rajshahi",
        "Khulna",
        "Barishal",
        "Rangpur",
    ]

    areas = [
        "Downtown",
        "Shopping Mall",
        "University Area",
        "Business District",
        "Residential Area",
    ]

    store_types = [
        "Flagship",
        "Standard",
        "Express",
    ]

    regions = [
        "Central",
        "East",
        "North",
        "South",
        "West",
    ]

    seating_capacity = [
        40,
        50,
        60,
        70,
        80,
    ]

    average_daily_customers = [
        180,
        220,
        260,
        300,
        350,
    ]

    stores = []

    for i in range(number_of_stores):
        city = cities[i % len(cities)]
        area = areas[i % len(areas)]
        store_type = store_types[i % len(store_types)]
        region = regions[i % len(regions)]

        stores.append(
            {
                "store_id": f"ST{i + 1:03d}",
                "store_name": f"SmartServe {city} {i + 1}",
                "city": city,
                "area": area,
                "store_type": store_type,
                "opening_date": "2022-01-01",
                "seating_capacity": seating_capacity[i % len(seating_capacity)],
                "average_daily_customers": average_daily_customers[
                    i % len(average_daily_customers)
                ],
                "manager_region": region,
            }
        )

    df = pd.DataFrame(stores)

    df["opening_date"] = pd.to_datetime(df["opening_date"])

    return df


def main() -> None:
    """
    Generate and save the store dimension.
    """

    prototype_config = CONFIG["data_generation"]["prototype"]

    df = generate_stores(
        number_of_stores=prototype_config["stores"]
    )

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "dim_store.csv"

    df.to_csv(output_file, index=False)

    logger.info(
        "Store dimension saved to %s",
        output_file
    )

    logger.info(
        "Generated %s store records",
        len(df)
    )

    print(df)


if __name__ == "__main__":
    main()