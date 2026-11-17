
"""
SmartServe Food Intelligence
Module: model_deployment.py

Purpose:
Load, validate, and inspect trained machine learning models.

This module provides reusable functions for loading saved models
and retrieving basic model information.

Usage:
    from src.model_deployment import (
        load_trained_model,
        get_model_information
    )

    model = load_trained_model(model_path)
    model_info = get_model_information(model)

Run:
    .venv\Scripts\python.exe -m src.model_deployment
"""

from pathlib import Path
from typing import Any

import joblib

from src.logger import get_logger

logger = get_logger(__name__)


def validate_model_file(model_path: str | Path) -> Path:
    """
    Validate the existence of a saved machine learning model.

    Args:
        model_path: Path to the saved model file.

    Returns:
        Path: Validated model file path.

    Raises:
        FileNotFoundError: If the model file does not exist.
        ValueError: If the path does not point to a file.
    """

    model_path = Path(model_path)

    if not model_path.exists():
        logger.error("Model file not found: %s", model_path)
        raise FileNotFoundError(
            f"Model file not found: {model_path}"
        )

    if not model_path.is_file():
        logger.error("Invalid model file path: %s", model_path)
        raise ValueError(
            f"Model path is not a file: {model_path}"
        )

    logger.info("Model file validation completed: %s", model_path)

    return model_path


def load_trained_model(model_path: str | Path) -> Any:
    """
    Load a previously trained machine learning model.

    Args:
        model_path: Path to the saved model file.

    Returns:
        Any: Loaded machine learning model.
    """

    model_path = validate_model_file(model_path)

    logger.info("Loading trained model: %s", model_path)

    model = joblib.load(model_path)

    logger.info(
        "Successfully loaded model: %s",
        type(model).__name__
    )

    return model


def get_model_information(model: Any) -> dict[str, Any]:
    """
    Retrieve basic information about a loaded model.

    Args:
        model: Loaded machine learning model.

    Returns:
        dict: Basic model information.
    """

    model_information = {
        "model_name": type(model).__name__,
        "model_module": type(model).__module__,
        "prediction_supported": callable(
            getattr(model, "predict", None)
        )
    }

    logger.info(
        "Retrieved model information: %s",
        model_information["model_name"]
    )

    return model_information


def main() -> None:
    """
    Execute a basic model deployment validation.
    """

    project_root = Path(__file__).resolve().parent.parent

    model_path = (
        project_root
        / "models"
        / "gradient_boosting_model.pkl"
    )

    logger.info("Starting model deployment validation")

    model = load_trained_model(model_path)

    model_information = get_model_information(model)

    print("\nSMARTSERVE MODEL DEPLOYMENT")
    print("=" * 55)

    for key, value in model_information.items():
        print(f"{key}: {value}")

    print("\nMODEL DEPLOYMENT VALIDATION COMPLETED")

    logger.info("Model deployment validation completed")


if __name__ == "__main__":
    main()
