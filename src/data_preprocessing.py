
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


DATE_COLUMNS = {
    "dim_date": ["full_date"],
    "dim_store": ["opening_date"],
    "dim_customer": ["signup_date"],
    "dim_promotion": ["start_date", "end_date"],
    "dim_holiday": ["holiday_date"],
}


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to lowercase snake_case.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


def convert_date_columns(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    """
    Convert known date columns to datetime format.
    """

    df = df.copy()

    date_columns = DATE_COLUMNS.get(dataset_name, [])

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


def remove_duplicate_rows(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    """
    Remove duplicate rows from a dataset.
    """

    df = df.copy()

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)

    logger.info(
        "%s: removed %s duplicate rows.",
        dataset_name,
        duplicate_count
    )

    return df


def analyze_missing_values(data: dict) -> pd.DataFrame:
    """
    Generate a missing-value report for all datasets.
    """

    records = []

    for dataset_name, df in data.items():

        for column in df.columns:

            missing_count = int(df[column].isna().sum())

            records.append({
                "dataset": dataset_name,
                "column": column,
                "missing_count": missing_count,
                "missing_percentage": round(
                    (missing_count / len(df)) * 100, 2
                ) if len(df) > 0 else 0
            })

    return pd.DataFrame(records)


def handle_missing_values(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    """
    Handle missing values without changing meaningful
    missing holiday names in the date dimension.

    Other missing values are reported, not automatically
    filled, to avoid introducing incorrect assumptions.
    """

    df = df.copy()

    missing_count = int(df.isna().sum().sum())

    logger.info(
        "%s: %s missing values detected.",
        dataset_name,
        missing_count
    )

    return df
