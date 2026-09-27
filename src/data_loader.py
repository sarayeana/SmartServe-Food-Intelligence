from pathlib import Path

import pandas as pd

from src.config import DATA_RAW
from src.logger import get_logger


logger = get_logger(__name__)


def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from the raw data directory.

    Args:
        filename: Name of the CSV file.

    Returns:
        Loaded pandas DataFrame.
    """

    file_path = DATA_RAW / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {file_path}"
        )

    logger.info(
        "Loading data file: %s",
        file_path,
    )

    return pd.read_csv(file_path)


def load_all_data() -> dict[str, pd.DataFrame]:
    """
    Load all SmartServe raw datasets.

    Returns:
        Dictionary containing all datasets.
    """

    datasets = {
        "dim_date": load_csv("dim_date.csv"),
        "dim_store": load_csv("dim_store.csv"),
        "dim_product": load_csv("dim_product.csv"),
        "dim_customer": load_csv("dim_customer.csv"),
        "dim_promotion": load_csv("dim_promotion.csv"),
        "dim_holiday": load_csv("dim_holiday.csv"),
        "dim_weather": load_csv("dim_weather.csv"),
        "fact_sales": load_csv("fact_sales.csv"),
        "fact_preparation": load_csv(
            "fact_preparation.csv"
        ),
        "fact_inventory": load_csv(
            "fact_inventory.csv"
        ),
        "fact_waste": load_csv(
            "fact_waste.csv"
        ),
    }

    logger.info(
        "Successfully loaded %s datasets",
        len(datasets),
    )

    return datasets


def print_dataset_summary(
    datasets: dict[str, pd.DataFrame],
) -> None:
    """
    Print row and column information for each dataset.
    """

    print("\nSMARTSERVE DATASET SUMMARY")
    print("=" * 70)

    for name, df in datasets.items():

        print(
            f"{name:<25}"
            f"Rows: {len(df):>8,}   "
            f"Columns: {len(df.columns):>3}"
        )

    print("=" * 70)


if __name__ == "__main__":

    data = load_all_data()

    print_dataset_summary(data)
