
"""
SmartServe - MySQL CSV Data Loader

Run from the project root:
    .venv\Scripts\python.exe sql\load_data.py

Loads the 11 raw CSV files into smartserve_db.
"""

import csv
import os
from pathlib import Path
from getpass import getpass

import mysql.connector


# ------------------------------------------------------------
# PROJECT PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD") or getpass(
        "Enter your MySQL password: "
    ),
    "database": os.getenv("MYSQL_DATABASE", "smartserve_db"),
}


# ------------------------------------------------------------
# LOAD ORDER
# Parent tables must be loaded before dependent tables.
# ------------------------------------------------------------

TABLE_FILES = [
    ("dim_date", "dim_date.csv"),
    ("dim_store", "dim_store.csv"),
    ("dim_product", "dim_product.csv"),
    ("dim_customer", "dim_customer.csv"),
    ("dim_promotion", "dim_promotion.csv"),
    ("dim_holiday", "dim_holiday.csv"),
    ("dim_weather", "dim_weather.csv"),
    ("fact_sales", "fact_sales.csv"),
    ("fact_inventory", "fact_inventory.csv"),
    ("fact_preparation", "fact_preparation.csv"),
    ("fact_waste", "fact_waste.csv"),
]


# ------------------------------------------------------------
# BOOLEAN COLUMNS
# ------------------------------------------------------------

BOOLEAN_COLUMNS = {
    "is_weekend",
    "is_holiday",
    "loyalty_member",
    "active_flag",
    "stockout_flag",
}


def normalize_value(column, value):
    """Convert CSV values into MySQL-compatible values."""

    if value is None:
        return None

    value = value.strip()

    if value.lower() in {"", "nan", "null"}:
        return None

    if column in BOOLEAN_COLUMNS:
        if value.lower() in {"true", "1", "yes"}:
            return 1
        if value.lower() in {"false", "0", "no"}:
            return 0
        raise ValueError(
            f"Unexpected boolean value for {column}: {value}"
        )

    return value


def load_table(cursor, table_name, csv_filename):
    """Load one CSV file into its corresponding MySQL table."""

    file_path = RAW_DATA_DIR / csv_filename

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    print(f"\nLoading {table_name}...")

    with file_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)
        columns = reader.fieldnames

        if not columns:
            raise ValueError(f"No column headers found in {csv_filename}")

        column_sql = ", ".join(
            f"`{column}`" for column in columns
        )

        placeholders = ", ".join(
            ["%s"] * len(columns)
        )

        insert_sql = (
            f"INSERT INTO `{table_name}` "
            f"({column_sql}) VALUES ({placeholders})"
        )

        batch = []
        total_rows = 0
        batch_size = 1000

        for row in reader:
            values = tuple(
                normalize_value(column, row[column])
                for column in columns
            )

            batch.append(values)

            if len(batch) >= batch_size:
                cursor.executemany(insert_sql, batch)
                total_rows += len(batch)
                batch.clear()

        if batch:
            cursor.executemany(insert_sql, batch)
            total_rows += len(batch)

    print(f"Inserted {total_rows:,} rows into {table_name}")

    return total_rows


def main():
    """Connect to MySQL and load all project datasets."""

    connection = None

    print("=" * 65)
    print("SMARTSERVE - MYSQL DATA LOADING")
    print("=" * 65)

    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Database: {DB_CONFIG['database']}")

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        cursor = connection.cursor()
        connection.start_transaction()

        total_loaded = 0

        for table_name, csv_filename in TABLE_FILES:
            rows_loaded = load_table(
                cursor,
                table_name,
                csv_filename
            )
            total_loaded += rows_loaded

        connection.commit()

        print("\n" + "=" * 65)
        print("DATA LOADING COMPLETED SUCCESSFULLY")
        print("=" * 65)
        print(f"Total rows loaded: {total_loaded:,}")
        print(f"Tables loaded: {len(TABLE_FILES)}")

    except Exception as error:
        if connection and connection.is_connected():
            connection.rollback()

        print("\nDATA LOADING FAILED")
        print(f"Error: {error}")
        print("The current loading transaction has been rolled back.")

        raise

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    main()
