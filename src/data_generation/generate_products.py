import pandas as pd

from src.config import CONFIG, DATA_RAW
from src.logger import get_logger
from src.utils import ensure_directory


logger = get_logger(__name__)


def generate_products(number_of_products: int) -> pd.DataFrame:
    """
    Generate the SmartServe product dimension.

    Args:
        number_of_products: Number of products to generate.

    Returns:
        DataFrame containing product information.
    """

    logger.info("Generating %s products", number_of_products)

    products = [
        ("Americano", "Beverage", "Coffee", "Regular", 120, 45, 4, 3),
        ("Cappuccino", "Beverage", "Coffee", "Regular", 160, 65, 4, 5),
        ("Latte", "Beverage", "Coffee", "Regular", 170, 70, 4, 5),
        ("Mocha", "Beverage", "Coffee", "Regular", 190, 80, 4, 6),
        ("Espresso", "Beverage", "Coffee", "Small", 100, 35, 4, 2),

        ("Iced Coffee", "Beverage", "Cold Drinks", "Regular", 180, 70, 6, 4),
        ("Iced Latte", "Beverage", "Cold Drinks", "Regular", 200, 80, 6, 5),
        ("Lemonade", "Beverage", "Cold Drinks", "Regular", 150, 55, 8, 3),
        ("Mango Smoothie", "Beverage", "Smoothie", "Regular", 220, 95, 6, 6),
        ("Chocolate Shake", "Beverage", "Shake", "Regular", 230, 100, 6, 6),

        ("Chicken Sandwich", "Food", "Sandwich", "Regular", 280, 140, 12, 8),
        ("Beef Burger", "Food", "Burger", "Regular", 350, 180, 12, 10),
        ("Chicken Burger", "Food", "Burger", "Regular", 320, 160, 12, 9),
        ("Veggie Sandwich", "Food", "Sandwich", "Regular", 240, 110, 12, 7),
        ("French Fries", "Food", "Sides", "Regular", 160, 65, 10, 5),

        ("Chocolate Cake", "Dessert", "Cake", "Slice", 220, 95, 24, 3),
        ("Cheesecake", "Dessert", "Cake", "Slice", 250, 110, 24, 3),
        ("Blueberry Muffin", "Dessert", "Bakery", "Regular", 150, 60, 24, 2),
        ("Chocolate Cookie", "Dessert", "Bakery", "Regular", 100, 35, 48, 2),
        ("Croissant", "Dessert", "Bakery", "Regular", 140, 55, 24, 3),
    ]

    products = products[:number_of_products]

    data = []

    for i, product in enumerate(products, start=1):
        (
            product_name,
            category,
            subcategory,
            size,
            selling_price,
            unit_cost,
            shelf_life_hours,
            preparation_time,
        ) = product

        data.append(
            {
                "product_id": f"PRD{i:03d}",
                "product_name": product_name,
                "category": category,
                "subcategory": subcategory,
                "size": size,
                "unit_cost": unit_cost,
                "selling_price": selling_price,
                "shelf_life_hours": shelf_life_hours,
                "preparation_time": preparation_time,
                "active_flag": True,
            }
        )

    return pd.DataFrame(data)


def main() -> None:
    """Generate and save the product dimension."""

    prototype_config = CONFIG["data_generation"]["prototype"]

    df = generate_products(
        number_of_products=prototype_config["products"]
    )

    ensure_directory(DATA_RAW)

    output_file = DATA_RAW / "dim_product.csv"

    df.to_csv(output_file, index=False)

    logger.info("Product dimension saved to %s", output_file)
    logger.info("Generated %s product records", len(df))

    print(df)


if __name__ == "__main__":
    main()
