
import pandas as pd

from src.data_loader import load_all_data
from src.logger import get_logger
from src.config import DATA_PROCESSED
from src.utils import ensure_directory


logger = get_logger(__name__)


def generate_quality_report(
    datasets: dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Generate a dataset-level data quality report.
    """

    report = []

    for dataset_name, df in datasets.items():

        total_cells = df.shape[0] * df.shape[1]
        missing_cells = int(df.isna().sum().sum())

        report.append({
            "dataset": dataset_name,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_cells": missing_cells,
            "missing_percentage": (
                round(missing_cells / total_cells * 100, 2)
                if total_cells > 0 else 0
            ),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": round(
                df.memory_usage(deep=True).sum() / (1024 ** 2), 2
            ),
        })

    return pd.DataFrame(report)


def main():

    logger.info("Starting SmartServe data quality report")

    datasets = load_all_data()

    report = generate_quality_report(datasets)

    ensure_directory(DATA_PROCESSED)

    output_file = DATA_PROCESSED / "data_quality_report.csv"

    report.to_csv(output_file, index=False)

    print("\nSMARTSERVE DATA QUALITY REPORT")
    print("=" * 90)
    print(report.to_string(index=False))
    print("=" * 90)

    logger.info("Data quality report saved to %s", output_file)


if __name__ == "__main__":
    main()
