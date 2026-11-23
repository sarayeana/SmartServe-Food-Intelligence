
import csv
import getpass
import os
from pathlib import Path

import getpass
import mysql.connector


# ------------------------------------------------------------
# PROJECT PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "business_intelligence"
    / "forecast_performance.csv"
)


# ------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": getpass.getpass("Enter MySQL password: "),
    "database": "smartserve_db"
}

# ------------------------------------------------------------
# EXPECTED CSV COLUMNS
# ------------------------------------------------------------

EXPECTED_COLUMNS = [
    "date_id",
    "full_date",
    "store_id",
    "product_id",
    "actual_sales_qty",
    "predicted_sales_qty",
    "prediction_error",
    "absolute_error",
    "error_type",
    "demand_level",
]


# ------------------------------------------------------------
# LOAD CSV DATA
# ------------------------------------------------------------

def load_forecast_data():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Forecast CSV not found: {CSV_PATH}"
        )

    records = []

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                "CSV columns do not match the expected structure.\n"
                f"Found: {reader.fieldnames}\n"
                f"Expected: {EXPECTED_COLUMNS}"
            )

        for row in reader:

            records.append((
                row["date_id"],
                row["full_date"],
                row["store_id"],
                row["product_id"],
                int(float(row["actual_sales_qty"])),
                float(row["predicted_sales_qty"]),
                float(row["prediction_error"]),
                float(row["absolute_error"]),
                row["error_type"] or None,
                row["demand_level"] or None,
            ))

    print(f"CSV records loaded into memory: {len(records):,}")

    if not records:
        raise ValueError("The forecast CSV contains no records.")

    # --------------------------------------------------------
    # DATABASE INSERTION
    # --------------------------------------------------------

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:

        insert_query = """
            INSERT INTO forecast_performance (
                date_id,
                full_date,
                store_id,
                product_id,
                actual_sales_qty,
                predicted_sales_qty,
                prediction_error,
                absolute_error,
                error_type,
                demand_level
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Replace existing analytics records on each full reload.
        cursor.execute("DELETE FROM forecast_performance")

        cursor.executemany(insert_query, records)

        connection.commit()

        print("\nFORECAST DATA LOAD SUCCESSFUL")
        print("=" * 55)
        print(f"Records inserted: {cursor.rowcount:,}")

        cursor.execute(
            "SELECT COUNT(*) FROM forecast_performance"
        )

        total_records = cursor.fetchone()[0]

        print(f"Records in database: {total_records:,}")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":
    load_forecast_data()
