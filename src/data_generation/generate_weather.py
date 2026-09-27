import random

import pandas as pd

from src.config import DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory, set_random_seed


logger = get_logger(__name__)


def generate_weather(
    date_file: str = "data/raw/dim_date.csv",
    store_file: str = "data/raw/dim_store.csv",
) -> pd.DataFrame:
    """
    Generate store-level daily weather data.

    Args:
        date_file: Path to the date dimension.
        store_file: Path to the store dimension.

    Returns:
        DataFrame containing daily weather by store.
    """

    logger.info("Generating weather data")

    set_random_seed(RANDOM_SEED)

    dates = pd.read_csv(date_file)
    stores = pd.read_csv(store_file)

    dates["full_date"] = pd.to_datetime(dates["full_date"])

    # Seasonal temperature ranges in Celsius.
    seasonal_ranges = {
        "Winter": (16, 27),
        "Spring": (22, 34),
        "Summer": (27, 36),
        "Autumn": (22, 33),
    }

    weather_conditions = [
        "Sunny",
        "Partly Cloudy",
        "Cloudy",
        "Rainy",
    ]

    records = []

    for _, date_row in dates.iterrows():

        season = date_row["season"]
        min_temp, max_temp = seasonal_ranges[season]

        for _, store_row in stores.iterrows():

            temperature = round(
                random.uniform(min_temp, max_temp),
                1,
            )

            # Rain becomes more likely during the summer/monsoon period.
            if season == "Summer":
                condition = random.choices(
                    weather_conditions,
                    weights=[30, 20, 15, 35],
                    k=1,
                )[0]
            else:
                condition = random.choices(
                    weather_conditions,
                    weights=[45, 25, 20, 10],
                    k=1,
                )[0]

            if condition == "Rainy":
                rainfall = round(
                    random.uniform(5, 60),
                    1,
                )
                humidity = random.randint(70, 95)

            elif condition == "Cloudy":
                rainfall = round(
                    random.uniform(0, 8),
                    1,
                )
                humidity = random.randint(60, 85)

            elif condition == "Partly Cloudy":
                rainfall = round(
                    random.uniform(0, 3),
                    1,
                )
                humidity = random.randint(50, 80)

            else:
                rainfall = 0.0
                humidity = random.randint(40, 70)

            records.append(
                {
                    "weather_id": (
                        f"WTH{date_row['date_id']}"
                        f"{store_row['store_id']}"
                    ),
                    "date_id": int(date_row["date_id"]),
                    "store_id": store_row["store_id"],
                    "temperature": temperature,
                    "rainfall": rainfall,
                    "humidity": humidity,
                    "weather_condition": condition,
                }
            )

    return pd.DataFrame(records)


def main() -> None:
    """Generate and save weather data."""

    df = generate_weather()

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "dim_weather.csv"

    df.to_csv(output_file, index=False)

    logger.info(
        "Weather data saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s weather records",
        len(df),
    )

    print(df.head())
    print(f"\nShape: {df.shape}")


if __name__ == "__main__":
    main()
