import random
from datetime import datetime

import pandas as pd

from src.config import CONFIG, DATA_RAW, RANDOM_SEED
from src.logger import get_logger
from src.utils import ensure_directory, set_random_seed


logger = get_logger(__name__)


def load_dimensions():
    """Load the dimension tables required for sales generation."""

    dates = pd.read_csv(DATA_RAW / "dim_date.csv")
    stores = pd.read_csv(DATA_RAW / "dim_store.csv")
    products = pd.read_csv(DATA_RAW / "dim_product.csv")
    customers = pd.read_csv(DATA_RAW / "dim_customer.csv")
    promotions = pd.read_csv(DATA_RAW / "dim_promotion.csv")
    weather = pd.read_csv(DATA_RAW / "dim_weather.csv")

    dates["full_date"] = pd.to_datetime(dates["full_date"])
    promotions["start_date"] = pd.to_datetime(promotions["start_date"])
    promotions["end_date"] = pd.to_datetime(promotions["end_date"])

    return (
        dates,
        stores,
        products,
        customers,
        promotions,
        weather,
    )


def get_base_demand(product):
    """
    Return approximate daily demand for a product.

    Different products have different demand levels.
    """

    category = product["category"]
    subcategory = product["subcategory"]

    if subcategory == "Coffee":
        return random.randint(25, 55)

    if subcategory == "Cold Drinks":
        return random.randint(20, 45)

    if subcategory == "Smoothie":
        return random.randint(12, 30)

    if subcategory == "Shake":
        return random.randint(10, 25)

    if subcategory == "Burger":
        return random.randint(15, 35)

    if subcategory == "Sandwich":
        return random.randint(12, 30)

    if subcategory == "Sides":
        return random.randint(15, 35)

    if subcategory == "Cake":
        return random.randint(8, 20)

    if subcategory == "Bakery":
        return random.randint(10, 25)

    return random.randint(10, 25)


def get_store_multiplier(store):
    """Return demand multiplier based on store type."""

    store_type = store["store_type"]

    multipliers = {
        "Flagship": 1.30,
        "Standard": 1.00,
        "Express": 0.75,
    }

    return multipliers.get(store_type, 1.00)


def get_day_multiplier(date_row):
    """Return demand multiplier based on day of week."""

    if date_row["is_weekend"]:
        return 1.20

    return 1.00


def get_weather_multiplier(product, weather_row):
    """Return a simple weather-based demand multiplier."""

    condition = weather_row["weather_condition"]
    category = product["category"]
    subcategory = product["subcategory"]

    multiplier = 1.00

    # Cold drinks perform better in hot weather.
    if subcategory in ["Cold Drinks", "Smoothie", "Shake"]:
        if weather_row["temperature"] >= 32:
            multiplier *= 1.25

    # Coffee demand increases slightly during rainy weather.
    if subcategory == "Coffee" and condition == "Rainy":
        multiplier *= 1.15

    # Heavy rain slightly reduces store traffic.
    if condition == "Rainy":
        multiplier *= 0.90

    return multiplier


def find_promotion(product, date, promotions):
    """
    Find an applicable promotion for a product on a given date.
    """

    matching = promotions[
        (promotions["start_date"] <= date)
        & (promotions["end_date"] >= date)
        & (
            (promotions["target_category"] == product["category"])
            | (promotions["target_category"] == "All")
        )
    ]

    if matching.empty:
        return None

    # Select one applicable promotion.
    return matching.sample(
        n=1,
        random_state=random.randint(1, 1_000_000)
    ).iloc[0]


def generate_sales() -> pd.DataFrame:
    """Generate the SmartServe sales fact table."""

    logger.info("Starting sales data generation")

    set_random_seed(RANDOM_SEED)

    (
        dates,
        stores,
        products,
        customers,
        promotions,
        weather,
    ) = load_dimensions()

    sales_records = []

    sales_id = 1
    order_number = 1

    for _, date_row in dates.iterrows():

        date = date_row["full_date"]

        for _, store in stores.iterrows():

            store_weather = weather[
                (weather["date_id"] == date_row["date_id"])
                & (weather["store_id"] == store["store_id"])
            ]

            if store_weather.empty:
                continue

            weather_row = store_weather.iloc[0]

            store_multiplier = get_store_multiplier(store)
            day_multiplier = get_day_multiplier(date_row)

            for _, product in products.iterrows():

                base_demand = get_base_demand(product)

                weather_multiplier = get_weather_multiplier(
                    product,
                    weather_row,
                )

                promotion = find_promotion(
                    product,
                    date,
                    promotions,
                )

                promotion_multiplier = 1.00
                promotion_id = None
                discount_percent = 0.0

                if promotion is not None:
                    promotion_id = promotion["promotion_id"]
                    discount_percent = float(
                        promotion["discount_percent"]
                    )

                    # Promotion increases demand.
                    promotion_multiplier = (
                        1 + discount_percent / 100 * 0.8
                    )

                demand = (
                    base_demand
                    * store_multiplier
                    * day_multiplier
                    * weather_multiplier
                    * promotion_multiplier
                )

                # Add realistic demand variation.
                demand *= random.uniform(0.75, 1.25)

                quantity = max(
                    1,
                    int(round(demand))
                )

                # Generate several orders from the product quantity.
                remaining_quantity = quantity

                while remaining_quantity > 0:

                    order_quantity = min(
                        remaining_quantity,
                        random.randint(1, 4)
                    )

                    customer = customers.sample(
                        n=1
                    ).iloc[0]

                    unit_price = float(product["selling_price"])

                    gross_sales = (
                        order_quantity * unit_price
                    )

                    discount_amount = (
                        gross_sales
                        * discount_percent
                        / 100
                    )

                    net_sales = (
                        gross_sales - discount_amount
                    )

                    unit_cost = float(product["unit_cost"])

                    cost_amount = (
                        order_quantity * unit_cost
                    )

                    profit_amount = (
                        net_sales - cost_amount
                    )

                    payment_method = random.choice(
                        [
                            "Cash",
                            "Card",
                            "Mobile Banking",
                        ]
                    )

                    sales_records.append(
                        {
                            "sales_id": f"SAL{sales_id:08d}",
                            "order_id": f"ORD{order_number:08d}",
                            "date_id": int(date_row["date_id"]),
                            "store_id": store["store_id"],
                            "customer_id": customer["customer_id"],
                            "product_id": product["product_id"],
                            "promotion_id": promotion_id,
                            "quantity": order_quantity,
                            "unit_price": unit_price,
                            "discount_amount": round(
                                discount_amount,
                                2,
                            ),
                            "gross_sales": round(
                                gross_sales,
                                2,
                            ),
                            "net_sales": round(
                                net_sales,
                                2,
                            ),
                            "cost_amount": round(
                                cost_amount,
                                2,
                            ),
                            "profit_amount": round(
                                profit_amount,
                                2,
                            ),
                            "payment_method": payment_method,
                        }
                    )

                    sales_id += 1
                    order_number += 1

                    remaining_quantity -= order_quantity

    return pd.DataFrame(sales_records)


def main() -> None:
    """Generate and save sales data."""

    df = generate_sales()

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "fact_sales.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    logger.info(
        "Sales fact table saved to %s",
        output_file,
    )

    logger.info(
        "Generated %s sales records",
        len(df),
    )

    print(df.head())
    print(f"\nShape: {df.shape}")
    print(
        f"Total Net Sales: "
        f"{df['net_sales'].sum():,.2f}"
    )


if __name__ == "__main__":
    main()
