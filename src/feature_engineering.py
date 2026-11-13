
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


def add_calendar_features(
    sales: pd.DataFrame,
    dates: pd.DataFrame
) -> pd.DataFrame:
    """
    Add calendar features to the sales dataset.

    The original input DataFrames remain unchanged.
    """

    sales = sales.copy()
    dates = dates.copy()

    # Validate required columns
    required_sales = ["date_id"]
    required_dates = ["date_id", "full_date"]

    for column in required_sales:
        if column not in sales.columns:
            raise ValueError(
                f"Missing required sales column: {column}"
            )

    for column in required_dates:
        if column not in dates.columns:
            raise ValueError(
                f"Missing required date column: {column}"
            )

    # Standardize date keys
    sales["date_id"] = pd.to_numeric(
        sales["date_id"], errors="raise"
    ).astype("int64")

    dates["date_id"] = pd.to_numeric(
        dates["date_id"], errors="raise"
    ).astype("int64")

    dates["full_date"] = pd.to_datetime(
        dates["full_date"], errors="coerce"
    )

    if dates["date_id"].duplicated().any():
        raise ValueError("Duplicate date_id values found in dim_date.")

    # Select useful calendar columns
    calendar_columns = [
        "year",
        "quarter",
        "month",
        "month_name",
        "day_name",
        "is_weekend",
        "is_holiday",
        "season"
    ]

    available_columns = [
        column
        for column in calendar_columns
        if column in dates.columns
        and column not in sales.columns
    ]

    date_features = dates[
        ["date_id", "full_date"] + available_columns
    ]

    # Merge calendar information into sales
    result = sales.merge(
        date_features,
        on="date_id",
        how="left",
        validate="many_to_one"
    )

    # Create additional calendar features
    result["day_of_month"] = result["full_date"].dt.day

    result["day_of_week"] = (
        result["full_date"].dt.dayofweek
    )

    result["week_of_year"] = (
        result["full_date"].dt.isocalendar().week.astype("Int64")
    )

    result["is_month_start"] = (
        result["full_date"].dt.is_month_start
    )

    result["is_month_end"] = (
        result["full_date"].dt.is_month_end
    )

    logger.info(
        "Calendar features added to sales dataset. "
        "Rows: %s | Columns: %s",
        len(result),
        len(result.columns)
    )

    return result


def add_product_store_features(
    sales: pd.DataFrame,
    stores: pd.DataFrame,
    products: pd.DataFrame
) -> pd.DataFrame:
    """
    Enrich sales data with product and store attributes.

    Dimension attributes are prefixed with product_ or store_.
    """

    result = sales.copy()

    dimensions = [
        ("store", stores, "store_id"),
        ("product", products, "product_id")
    ]

    for prefix, dimension, key in dimensions:

        if key not in result.columns:
            raise ValueError(
                f"Sales dataset is missing {key}."
            )

        if key not in dimension.columns:
            raise ValueError(
                f"{prefix} dimension is missing {key}."
            )

        if dimension[key].duplicated().any():
            raise ValueError(
                f"Duplicate {key} values found in {prefix} dimension."
            )

        # Select dimension attributes not already present in sales
        attributes = [
            column for column in dimension.columns
            if column != key
        ]

        # Prefix attribute names to avoid column-name collisions
        dimension_features = dimension[
            [key] + attributes
        ].rename(
            columns={
                column: f"{prefix}_{column}"
                for column in attributes
            }
        )

        result = result.merge(
            dimension_features,
            on=key,
            how="left",
            validate="many_to_one"
        )

    if len(result) != len(sales):
        raise ValueError(
            "Sales row count changed after dimension merging."
        )

    logger.info(
        "Product and store features added. Rows: %s | Columns: %s",
        len(result),
        len(result.columns)
    )

    return result

def add_customer_features(
    sales: pd.DataFrame,
    customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Add customer attributes to the sales dataset.
    """

    result = sales.copy()
    customers = customers.copy()

    key = "customer_id"

    if key not in result.columns or key not in customers.columns:
        raise ValueError("customer_id must exist in both datasets.")

    if customers[key].duplicated().any():
        raise ValueError("Customer dimension contains duplicate customer_id values.")

    attributes = [
        column for column in customers.columns
        if column != key
    ]

    customer_features = customers[[key] + attributes].rename(
        columns={
            column: f"customer_{column}"
            for column in attributes
        }
    )

    result = result.merge(
        customer_features,
        on=key,
        how="left",
        validate="many_to_one"
    )

    if len(result) != len(sales):
        raise ValueError("Customer feature engineering changed the sales row count.")

    logger.info("Customer features added to sales dataset.")

    return result

    
    
def add_promotion_features(
    sales: pd.DataFrame,
    promotions: pd.DataFrame
) -> pd.DataFrame:
    """
    Add promotion attributes to the sales dataset.

    Sales without a promotion are retained with missing promotion
    attributes. The original sales row count must remain unchanged.
    """

    result = sales.copy()
    promotions = promotions.copy()

    key = "promotion_id"

    # 1. Validate required columns
    if key not in result.columns:
        raise ValueError("Sales dataset must contain promotion_id.")

    if key not in promotions.columns:
        raise ValueError("Promotion dataset must contain promotion_id.")

    # 2. Validate promotion dimension keys
    if promotions[key].isna().any():
        raise ValueError("Promotion dimension contains missing promotion_id values.")

    if promotions[key].duplicated().any():
        raise ValueError("Promotion dimension contains duplicate promotion_id values.")

    # 3. Prepare promotion attributes
    attributes = [
        column for column in promotions.columns
        if column != key
    ]

    promotion_features = promotions[[key] + attributes].rename(
        columns={
            column: f"promotion_{column}"
            for column in attributes
        }
    )

    # 4. Prevent accidental overwriting of existing columns
    new_columns = [
        column for column in promotion_features.columns
        if column != key
    ]

    existing_columns = set(result.columns).intersection(new_columns)

    if existing_columns:
        raise ValueError(
            f"Promotion feature columns already exist: "
            f"{sorted(existing_columns)}"
        )

    # 5. Merge promotion attributes into sales
    result = result.merge(
        promotion_features,
        on=key,
        how="left",
        validate="many_to_one",
        indicator="_promotion_merge_status"
    )

    # 6. Count unmatched non-null promotion IDs
    unmatched_count = int(
        (
            (result["_promotion_merge_status"] == "left_only")
            & result[key].notna()
        ).sum()
    )

    # 7. Remove temporary merge indicator
    result.drop(columns="_promotion_merge_status", inplace=True)

    # 8. Confirm that the sales row count is unchanged
    if len(result) != len(sales):
        raise ValueError(
            "Promotion feature engineering changed the sales row count."
        )

    logger.info(
        "Promotion features added | Rows: %s | Unmatched promotion IDs: %s",
        len(result),
        unmatched_count
    )

    return result


    
def add_weather_features(
    sales: pd.DataFrame,
    weather: pd.DataFrame
) -> pd.DataFrame:
    """
    Add store-level daily weather attributes to sales transactions.
    """

    result = sales.copy()
    weather = weather.copy()

    keys = ["date_id", "store_id"]

    # Validate required columns
    for key in keys:
        if key not in result.columns:
            raise ValueError(f"Sales dataset is missing {key}.")

        if key not in weather.columns:
            raise ValueError(f"Weather dataset is missing {key}.")

    # Check weather key uniqueness
    if weather.duplicated(subset=keys).any():
        raise ValueError(
            "Weather dataset contains duplicate date-store combinations."
        )

    # Select and rename weather attributes
    attributes = [
        column for column in weather.columns
        if column not in keys
    ]

    weather_features = weather[keys + attributes].rename(
        columns={
            column: f"weather_{column}"
            for column in attributes
        }
    )

    # Prevent overwriting existing columns
    new_columns = [
        column for column in weather_features.columns
        if column not in keys
    ]

    existing_columns = set(result.columns).intersection(new_columns)

    if existing_columns:
        raise ValueError(
            f"Weather columns already exist: {sorted(existing_columns)}"
        )

    # Merge weather features
    result = result.merge(
        weather_features,
        on=keys,
        how="left",
        validate="many_to_one",
        indicator="_weather_merge_status"
    )

    unmatched_count = int(
        (result["_weather_merge_status"] == "left_only").sum()
    )

    result.drop(
        columns=["_weather_merge_status"],
        inplace=True
    )

    # Confirm original row count is preserved
    if len(result) != len(sales):
        raise ValueError(
            "Weather feature engineering changed the sales row count."
        )

    logger.info(
        "Weather features added. Rows: %s, unmatched records: %s",
        len(result),
        unmatched_count
    )

    return result

def validate_featured_sales(
    original_sales: pd.DataFrame,
    featured_sales: pd.DataFrame
) -> pd.DataFrame:
    """
    Validate the enriched sales dataset.
    """

    checks = []

    def add_check(check_name, passed, details):
        checks.append({
            "check": check_name,
            "passed": bool(passed),
            "details": details
        })

    # Check 1: Row count preservation
    row_count_ok = len(original_sales) == len(featured_sales)

    add_check(
        "Sales row count preserved",
        row_count_ok,
        f"Original: {len(original_sales)}, "
        f"Featured: {len(featured_sales)}"
    )

    # Check 2: Sales ID order preservation
    ids_preserved = (
        original_sales["sales_id"].reset_index(drop=True).equals(
            featured_sales["sales_id"].reset_index(drop=True)
        )
    )

    add_check(
        "Sales IDs preserved in original order",
        ids_preserved,
        "Original sales IDs compared with featured sales IDs."
    )

    # Check 3: Duplicate sales IDs
    duplicate_ids = int(featured_sales["sales_id"].duplicated().sum())

    add_check(
        "No duplicate sales IDs",
        duplicate_ids == 0,
        f"Duplicate IDs: {duplicate_ids}"
    )

    # Check 4–8: Feature availability
    feature_groups = {
        "customer_": "customer_ features available",
        "product_": "product_ features available",
        "store_": "store_ features available",
        "promotion_": "promotion_ features available",
        "weather_": "weather_ features available"
    }

    for prefix, check_name in feature_groups.items():

        matching_columns = [
            column for column in featured_sales.columns
            if column.startswith(prefix)
        ]

        add_check(
            check_name,
            len(matching_columns) > 0,
            f"Found {len(matching_columns)} columns."
        )

    report = pd.DataFrame(checks)

    logger.info(
        "Featured sales validation completed. Passed: %s/%s",
        int(report["passed"].sum()),
        len(report)
    )

    return report