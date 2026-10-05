from pathlib import Path

import pandas as pd

from database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def load_processed_file(file_name, table_name):

    file_path = PROCESSED_DIR / file_name

    print("=" * 60)
    print(f"LOADING: {file_name}")
    print("=" * 60)

    # Read processed CSV
    df = pd.read_csv(file_path)

    print(f"Records found: {len(df)}")

    connection = get_connection()
    cursor = connection.cursor()

    try:

        columns = list(df.columns)

        column_names = ", ".join(columns)

        placeholders = ", ".join(
            ["%s"] * len(columns)
        )

        query = f"""
            INSERT INTO staging.{table_name} (
                {column_names}
            )
            VALUES (
                {placeholders}
            )
            ON CONFLICT DO NOTHING
        """

        for _, row in df.iterrows():

            values = tuple(
                row[column]
                for column in columns
            )

            cursor.execute(
                query,
                values
            )

        connection.commit()

        print(
            f"Successfully loaded {len(df)} "
            f"records into staging.{table_name}."
        )

    except Exception as error:

        connection.rollback()

        print("Error while loading data:")
        print(error)

    finally:

        cursor.close()
        connection.close()

        print("Database connection closed.")

        print()


def load_all_processed_data():

    datasets = [
        ("customers_valid.csv", "customers"),
        ("plans_valid.csv", "plans"),
        ("recharges_valid.csv", "recharges"),
        ("usage_valid.csv", "usage"),
        ("complaints_valid.csv", "complaints"),
        ("network_events_valid.csv", "network_events"),
        ("payments_valid.csv", "payments")
    ]

    for file_name, table_name in datasets:

        load_processed_file(
            file_name,
            table_name
        )


if __name__ == "__main__":

    load_all_processed_data()