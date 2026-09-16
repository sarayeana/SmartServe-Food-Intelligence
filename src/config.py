from pathlib import Path
import yaml


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Load config.yaml
CONFIG_FILE = PROJECT_ROOT / "config.yaml"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    CONFIG = yaml.safe_load(file)


# Project information
PROJECT_NAME = CONFIG["project"]["name"]
PROJECT_VERSION = CONFIG["project"]["version"]


# Data paths
DATA_RAW = PROJECT_ROOT / CONFIG["paths"]["data_raw"]
DATA_PROCESSED = PROJECT_ROOT / CONFIG["paths"]["data_processed"]
DATA_ML = PROJECT_ROOT / CONFIG["paths"]["data_ml"]


# Model paths
MODELS = PROJECT_ROOT / CONFIG["paths"]["models"]
DEMAND_MODELS = PROJECT_ROOT / CONFIG["paths"]["demand_models"]
WASTE_MODELS = PROJECT_ROOT / CONFIG["paths"]["waste_models"]


# Other project paths
NOTEBOOKS = PROJECT_ROOT / CONFIG["paths"]["notebooks"]
SQL = PROJECT_ROOT / CONFIG["paths"]["sql"]
EXCEL = PROJECT_ROOT / CONFIG["paths"]["excel"]
POWERBI = PROJECT_ROOT / CONFIG["paths"]["powerbi"]
DOCUMENTATION = PROJECT_ROOT / CONFIG["paths"]["documentation"]
REPORTS = PROJECT_ROOT / CONFIG["paths"]["reports"]


# Random seed
RANDOM_SEED = CONFIG["random_seed"]