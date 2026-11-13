
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


def inspect_dataset(
    df: pd.DataFrame,
    dataset_name: str
) -> dict:
    """
    Inspect a dataset and return its basic quality summary.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    summary = {
        "dataset": dataset_name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2
        )
    }

    logger.info(
        "Inspected %s | Rows: %s | Columns: %s",
        dataset_name,
        summary["rows"],
        summary["columns"]
    )

    return summary


def inspect_all_datasets(data: dict) -> pd.DataFrame:
    """
    Inspect all datasets and return a consolidated report.
    """

    inspection_results = []

    for dataset_name, df in data.items():

        result = inspect_dataset(
            df=df,
            dataset_name=dataset_name
        )

        inspection_results.append(result)

    report = pd.DataFrame(inspection_results)

    logger.info(
        "Completed inspection of %s datasets.",
        len(report)
    )

    return report
