import pandas as pd

from src.config import CONFIG, DATA_RAW
from src.logger import get_logger
from src.utils import ensure_directory


logger = get_logger(__name__)


def generate_holidays() -> pd.DataFrame:
    """
    Generate the SmartServe holiday dimension.

    Returns:
        DataFrame containing holiday information.
    """

    logger.info("Generating holiday calendar")

    holidays = [
        # 2025
        {
            "holiday_id": "HOL001",
            "holiday_date": "2025-01-01",
            "holiday_name": "New Year's Day",
            "holiday_type": "Public Holiday",
        },
        {
            "holiday_id": "HOL002",
            "holiday_date": "2025-02-21",
            "holiday_name": "International Mother Language Day",
            "holiday_type": "Public Holiday",
        },
        {
            "holiday_id": "HOL003",
            "holiday_date": "2025-03-26",
            "holiday_name": "Independence Day",
            "holiday_type": "Public Holiday",
        },
        {
            "holiday_id": "HOL004",
            "holiday_date": "2025-03-31",
            "holiday_name": "Eid-ul-Fitr",
            "holiday_type": "Religious Holiday",
        },

        # 2026
        {
            "holiday_id": "HOL005",
            "holiday_date": "2026-01-01",
            "holiday_name": "New Year's Day",
            "holiday_type": "Public Holiday",
        },
        {
            "holiday_id": "HOL006",
            "holiday_date": "2026-02-21",
            "holiday_name": "International Mother Language Day",
            "holiday_type": "Public Holiday",
        },
        {
            "holiday_id": "HOL007",
            "holiday_date": "2026-03-26",
            "holiday_name": "Independence Day",
            "holiday_type": "Public Holiday",
        },
        {
            "holiday_id": "HOL008",
            "holiday_date": "2026-03-20",
            "holiday_name": "Eid-ul-Fitr",
            "holiday_type": "Religious Holiday",
        },
    ]

    df = pd.DataFrame(holidays)

    df["holiday_date"] = pd.to_datetime(df["holiday_date"])

    return df


def main() -> None:
    """Generate and save the holiday dimension."""

    df = generate_holidays()

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "dim_holiday.csv"

    df.to_csv(output_file, index=False)

    logger.info(
        "Holiday dimension saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s holiday records",
        len(df),
    )

    print(df)
    print(f"\nShape: {df.shape}")


if __name__ == "__main__":
    main()
