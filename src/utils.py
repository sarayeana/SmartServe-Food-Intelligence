from pathlib import Path
import random

import numpy as np


def set_random_seed(seed: int) -> None:
    """
    Set random seeds for reproducible results.
    """
    random.seed(seed)
    np.random.seed(seed)


def ensure_directory(path: Path) -> Path:
    """
    Create a directory if it does not already exist.

    Returns:
        Path: The directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_project_root() -> Path:
    """
    Return the root directory of the SmartServe project.
    """
    return Path(__file__).resolve().parent.parent
