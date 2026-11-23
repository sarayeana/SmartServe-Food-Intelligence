
"""
SmartServe - MySQL Database Validation

Run from the project root:
    .venv\Scripts\python.exe sql\validate_database.py
"""

import os
from getpass import getpass

import mysql.connector


DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD") or getpass(
        "Enter your MySQL password: "
    ),
    "database": os.getenv("MYSQL_DATABASE", "smartserve_db"),
}


# Expected row counts based on the original CSV files.
EXPECTED_COUNTS = {
    "dim_date": 90,
    "dim_store": 5,
    "dim_product": 20,
    "dim_customer": 1000,
    "dim_promotion": 8,
    "dim_holiday": 8,
    "dim_weather": 450,
    "fact_sales": 122318,
    "fact_inventory": 9000,
    "fact_preparation": 9000,
    "fact_waste": 3648,
}


# Primary keys for uniqueness and NULL checks.
PRIMARY_KEYS = {
    "dim_date": "date_id",
    "dim_store": "store_id",
    "dim_product": "product_id",
    "dim_customer": "customer_id",
    "dim_promotion": "promotion_id",
    "dim_holiday": "holiday_id",
    "dim_weather": "weather_id",
    "fact_sales": "sales_id",
    "fact_inventory": "inventory_id",
    "fact_preparation": "preparation_id",
    "fact_waste": "waste_id",
}


def main():
    connection = None

    print("=" * 70)
    print("SMARTSERVE - MYSQL DATABASE VALIDATION")
    print("=" * 70)

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        total_rows = 0
        all_checks_passed = True

        print("\n1. TABLE ROW COUNT VALIDATION")
        print("-" * 70)

        for table, expected in EXPECTED_COUNTS.items():
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            actual = cursor.fetchone()[0]

            total_rows += actual
            passed = actual == expected

            status = "PASS" if passed else "FAIL"

            print(
                f"{table:<22} "
                f"Expected: {expected:>8,} | "
                f"Actual: {actual:>8,} | {status}"
            )

            if not passed:
                all_checks_passed = False

        print(f"\nTotal database rows: {total_rows:,}")

        print("\n2. PRIMARY KEY VALIDATION")
        print("-" * 70)

        for table, primary_key in PRIMARY_KEYS.items():

            cursor.execute(
                f"SELECT COUNT(*) FROM `{table}` "
                f"WHERE `{primary_key}` IS NULL"
            )
            null_count = cursor.fetchone()[0]

            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM (
                    SELECT `{primary_key}`
                    FROM `{table}`
                    GROUP BY `{primary_key}`
                    HAVING COUNT(*) > 1
                ) AS duplicates
                """
            )
            duplicate_count = cursor.fetchone()[0]

            passed = null_count == 0 and duplicate_count == 0

            status = "PASS" if passed else "FAIL"

            print(
                f"{table:<22} "
                f"NULL keys: {null_count:>3} | "
                f"Duplicate keys: {duplicate_count:>3} | "
                f"{status}"
            )

            if not passed:
                all_checks_passed = False

        print("\n3. DATABASE STRUCTURE VALIDATION")
        print("-" * 70)

        cursor.execute("SHOW TABLES")
        actual_tables = {row[0] for row in cursor.fetchall()}
        expected_tables = set(EXPECTED_COUNTS)

        missing_tables = expected_tables - actual_tables
        unexpected_tables = actual_tables - expected_tables

        if not missing_tables and not unexpected_tables:
            print("PASS - All 11 expected tables exist.")
        else:
            print("FAIL - Database table structure does not match.")
            print("Missing tables:", missing_tables)
            print("Unexpected tables:", unexpected_tables)
            all_checks_passed = False

        print("\n" + "=" * 70)

        if all_checks_passed:
            print("FINAL RESULT: ALL VALIDATION CHECKS PASSED")
        else:
            print("FINAL RESULT: SOME VALIDATION CHECKS FAILED")

        print("=" * 70)

    except Exception as error:
        print(f"\nVALIDATION ERROR: {error}")
        raise

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    main()
