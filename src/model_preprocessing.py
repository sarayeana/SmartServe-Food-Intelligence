
import pandas as pd

from src.logger import get_logger


logger = get_logger(__name__)


def impute_missing_features(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    feature_columns: list
) -> tuple:
    """
    Impute missing numerical and categorical features.

    Numerical features use the training median.
    Categorical features use the training mode.

    Imputation values are calculated from training data only
    to prevent data leakage.
    """

    train = train_data.copy()
    test = test_data.copy()

    if not feature_columns:
        raise ValueError("Feature columns cannot be empty.")

    missing_train = [
        col for col in feature_columns
        if col not in train.columns
    ]

    missing_test = [
        col for col in feature_columns
        if col not in test.columns
    ]

    if missing_train or missing_test:
        raise ValueError(
            f"Missing training columns: {missing_train}; "
            f"Missing testing columns: {missing_test}"
        )

    imputation_values = {}

    for column in feature_columns:

        if pd.api.types.is_numeric_dtype(train[column]):

            value = train[column].median()

        else:

            modes = train[column].mode(dropna=True)

            if modes.empty:
                raise ValueError(
                    f"No valid training values found in {column}."
                )

            value = modes.iloc[0]

        if pd.isna(value):
            raise ValueError(
                f"Cannot calculate an imputation value for {column}."
            )

        imputation_values[column] = value

        train[column] = train[column].fillna(value)
        test[column] = test[column].fillna(value)

    logger.info("Feature imputation completed.")

    return train, test, imputation_values


def validate_imputed_features(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    feature_columns: list
) -> pd.DataFrame:
    """
    Validate missing values after feature imputation.
    """

    records = []

    for dataset_name, df in [
        ("Training", train_data),
        ("Testing", test_data)
    ]:

        for column in feature_columns:

            records.append({
                "dataset": dataset_name,
                "feature": column,
                "missing_count": int(df[column].isna().sum()),
                "data_type": str(df[column].dtype)
            })

    report = pd.DataFrame(records)

    if report["missing_count"].sum() > 0:
        logger.warning("Missing values remain after imputation.")
    else:
        logger.info("All features passed missing-value validation.")

    return report

def prepare_model_features(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame
) -> tuple:
    """
    Prepare model predictors for training and testing.

    Derive store operating days, remove identifier columns,
    and identify numerical and categorical features.
    """

    train = train_data.copy()
    test = test_data.copy()

    for df in [train, test]:
        df["calendar_full_date"] = pd.to_datetime(
            df["calendar_full_date"]
        )
        df["store_opening_date"] = pd.to_datetime(
            df["store_opening_date"]
        )

        df["store_operating_days"] = (
            df["calendar_full_date"] -
            df["store_opening_date"]
        ).dt.days

    excluded_columns = [
        "date_id",
        "calendar_full_date",
        "store_id",
        "product_id",
        "sales_qty",
        "store_opening_date",
        "weather_weather_id"
    ]

    X_train = train.drop(
        columns=excluded_columns,
        errors="ignore"
    )

    X_test = test.drop(
        columns=excluded_columns,
        errors="ignore"
    )

    numerical_features = X_train.select_dtypes(
        include=["number", "bool"]
    ).columns.tolist()

    categorical_features = X_train.select_dtypes(
        include=["object", "category", "str"]
    ).columns.tolist()

    if X_train.columns.tolist() != X_test.columns.tolist():
        raise ValueError(
            "Training and testing feature columns do not match."
        )

    logger.info(
        "Model features prepared | Numerical: %s | Categorical: %s",
        len(numerical_features),
        len(categorical_features)
    )

    return (
        X_train,
        X_test,
        numerical_features,
        categorical_features
    )

def prepare_missing_value_indicators(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame
) -> tuple:
    """
    Handle expected holiday nulls and create missing-value
    indicators for numerical features.
    """

    train = train_data.copy()
    test = test_data.copy()

    holiday_column = "calendar_holiday_name"

    if holiday_column in train.columns:
        train[holiday_column] = (
            train[holiday_column].fillna("No Holiday")
        )
        test[holiday_column] = (
            test[holiday_column].fillna("No Holiday")
        )

    numerical_columns = train.select_dtypes(
        include=["number"]
    ).columns.tolist()

    indicator_columns = []

    for column in numerical_columns:

        if train[column].isna().any() or test[column].isna().any():

            indicator = f"{column}_missing"

            train[indicator] = train[column].isna().astype(int)
            test[indicator] = test[column].isna().astype(int)

            indicator_columns.append(indicator)

    logger.info(
        "Missing-value indicators created: %s",
        len(indicator_columns)
    )

    return train, test, indicator_columns

def encode_categorical_features(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    categorical_columns: list
) -> tuple:
    """
    One-hot encode categorical features.

    Fit the encoder on training data only and transform
    both training and testing data.
    """

    from sklearn.preprocessing import OneHotEncoder

    train = train_data.copy()
    test = test_data.copy()

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )

    train_encoded = encoder.fit_transform(
        train[categorical_columns]
    )

    test_encoded = encoder.transform(
        test[categorical_columns]
    )

    encoded_columns = encoder.get_feature_names_out(
        categorical_columns
    )

    train_encoded_df = pd.DataFrame(
        train_encoded,
        columns=encoded_columns,
        index=train.index
    )

    test_encoded_df = pd.DataFrame(
        test_encoded,
        columns=encoded_columns,
        index=test.index
    )

    train = train.drop(columns=categorical_columns)
    test = test.drop(columns=categorical_columns)

    train = pd.concat([train, train_encoded_df], axis=1)
    test = pd.concat([test, test_encoded_df], axis=1)

    logger.info(
        "Categorical encoding completed | Encoded columns: %s",
        len(encoded_columns)
    )

    return train, test, encoder

def convert_boolean_features(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame
) -> tuple:
    """
    Convert Boolean predictor columns into integer values.
    """

    train = train_data.copy()
    test = test_data.copy()

    boolean_columns = train.select_dtypes(
        include=["bool"]
    ).columns.tolist()

    train[boolean_columns] = train[boolean_columns].astype(int)
    test[boolean_columns] = test[boolean_columns].astype(int)

    logger.info(
        "Boolean features converted: %s",
        len(boolean_columns)
    )

    return train, test, boolean_columns