# Model Evaluation Utilities
# Reusable regression evaluation functions for SmartServe.

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def evaluate_regression_model(
    model_name,
    actual_values,
    predicted_values
):
    """
    Evaluate a regression model using standard metrics.
    """

    mae = mean_absolute_error(
        actual_values,
        predicted_values
    )

    mse = mean_squared_error(
        actual_values,
        predicted_values
    )

    rmse = np.sqrt(mse)

    r2 = r2_score(
        actual_values,
        predicted_values
    )

    return {
        "Model": model_name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }


def create_model_comparison(results):
    """
    Create a comparison table sorted by RMSE.
    """

    comparison = pd.DataFrame(results)

    return comparison.sort_values(
        by="RMSE",
        ascending=True
    ).reset_index(drop=True)