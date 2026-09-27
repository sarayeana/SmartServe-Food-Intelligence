import random

import pandas as pd

from src.config import CONFIG, DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory, set_random_seed


logger = get_logger(__name__)


def generate_customers(number_of_customers: int) -> pd.DataFrame:
    """
    Generate the SmartServe customer dimension.

    Args:
        number_of_customers: Number of customers to generate.

    Returns:
        DataFrame containing customer information.
    """

    logger.info("Generating %s customers", number_of_customers)

    set_random_seed(RANDOM_SEED)

    customer_segments = [
        "Regular",
        "Occasional",
        "Premium",
        "New",
    ]

    age_groups = [
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55+",
    ]

    acquisition_channels = [
        "Walk-in",
        "Social Media",
        "Referral",
        "Website",
        "Mobile App",
    ]

    data = []

    for i in range(1, number_of_customers + 1):

        # Generate signup date between 2022 and 2025
        signup_date = pd.Timestamp("2022-01-01") + pd.Timedelta(
            days=random.randint(0, 1460)
        )

        data.append(
            {
                "customer_id": f"CUS{i:05d}",
                "signup_date": signup_date,
                "customer_segment": random.choices(
                    customer_segments,
                    weights=[45, 30, 15, 10],
                    k=1,
                )[0],
                "age_group": random.choice(age_groups),
                "loyalty_member": random.choices(
                    [True, False],
                    weights=[40, 60],
                    k=1,
                )[0],
                "acquisition_channel": random.choice(
                    acquisition_channels
                ),
            }
        )

    return pd.DataFrame(data)


def main() -> None:
    """Generate and save the customer dimension."""

    prototype_config = CONFIG["data_generation"]["prototype"]

    df = generate_customers(
        number_of_customers=prototype_config["customers"]
    )

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "dim_customer.csv"

    df.to_csv(output_file, index=False)

    logger.info(
        "Customer dimension saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s customer records",
        len(df),
    )

    print(df.head())
    print(f"\nShape: {df.shape}")


if __name__ == "__main__":
    main()
