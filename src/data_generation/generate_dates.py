
import pandas as pd

from src.config import CONFIG, DATA_RAW
from src.logger import get_logger
from src.utils import ensure_directory


logger = get_logger(__name__)


def generate_dates(
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Generate the SmartServe date dimension and enrich it
    with holiday information from dim_holiday.csv.
    """

    logger.info(
        "Generating dates from %s to %s",
        start_date,
        end_date
    )

    dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D"
    )

    df = pd.DataFrame({
        "full_date": dates
    })

    # Calendar attributes
    df["date_id"] = df["full_date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["full_date"].dt.year
    df["quarter"] = df["full_date"].dt.quarter
    df["month"] = df["full_date"].dt.month
    df["month_name"] = df["full_date"].dt.month_name()
    df["week"] = df["full_date"].dt.isocalendar().week.astype(int)
    df["day"] = df["full_date"].dt.day
    df["day_name"] = df["full_date"].dt.day_name()
    df["day_of_week"] = df["full_date"].dt.dayofweek + 1
    df["is_weekend"] = df["day_of_week"].isin([6, 7])

    # Season classification
    def get_season(month: int) -> str:
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        return "Autumn"

    df["season"] = df["month"].apply(get_season)

    # Initialize holiday columns
    df["is_holiday"] = False
    df["holiday_name"] = None

    # Enrich date dimension using the holiday dimension
    holiday_file = DATA_RAW / "dim_holiday.csv"

    if holiday_file.exists():

        holidays = pd.read_csv(holiday_file)

        required_columns = {"holiday_date", "holiday_name"}

        if not required_columns.issubset(holidays.columns):
            raise ValueError(
                "dim_holiday.csv must contain holiday_date "
                "and holiday_name columns."
            )

        holidays["holiday_date"] = pd.to_datetime(
            holidays["holiday_date"],
            errors="raise"
        ).dt.normalize()

        if holidays["holiday_date"].duplicated().any():
            raise ValueError(
                "Duplicate holiday dates found in dim_holiday.csv."
            )

        holiday_map = (
            holidays
            .dropna(subset=["holiday_name"])
            .set_index("holiday_date")["holiday_name"]
            .to_dict()
        )

        df["holiday_name"] = (
            df["full_date"]
            .dt.normalize()
            .map(holiday_map)
        )

        df["is_holiday"] = df["holiday_name"].notna()

        logger.info(
            "Matched %s holidays within the generated date range.",
            int(df["is_holiday"].sum())
        )

    else:
        logger.warning(
            "dim_holiday.csv not found. Holiday fields remain empty."
        )

    # Reorder columns
    df = df[
        [
            "date_id",
            "full_date",
            "year",
            "quarter",
            "month",
            "month_name",
            "week",
            "day",
            "day_name",
            "day_of_week",
            "is_weekend",
            "is_holiday",
            "holiday_name",
            "season",
        ]
    ]

    return df


def main() -> None:
    """
    Generate and save the date dimension.
    """

    prototype_config = CONFIG["data_generation"]["prototype"]

    ensure_directory(DATA_RAW)

    df = generate_dates(
        start_date=prototype_config["start_date"],
        end_date=prototype_config["end_date"]
    )

    output_file = DATA_RAW / "dim_date.csv"
    df.to_csv(output_file, index=False)

    logger.info(
        "Date dimension saved to %s",
        output_file
    )

    logger.info(
        "Generated %s date records",
        len(df)
    )


if __name__ == "__main__":
    main()
