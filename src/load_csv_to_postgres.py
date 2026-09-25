from pathlib import Path

import pandas as pd

from database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def load_csv_to_postgres(csv_file, table_name):

    csv_path = SOURCE_DIR / csv_file

    print(f"Reading {csv_file}...")

    # Read CSV
    df = pd.read_csv(csv_path)

    print(f"Records found: {len(df)}")

    # Connect to PostgreSQL
    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Get column names from CSV
        columns = list(df.columns)

        # Create column list for SQL
        column_names = ", ".join(columns)

        # Create placeholders
        placeholders = ", ".join(["%s"] * len(columns))

        query = f"""
            INSERT INTO raw.{table_name} (
                {column_names}
            )
            VALUES (
                {placeholders}
            )
        """

        # Insert records
        for _, row in df.iterrows():

            values = tuple(row[column] for column in columns)

            cursor.execute(query, values)

        # Save changes
        connection.commit()

        print(
            f"Successfully loaded {len(df)} records "
            f"into raw.{table_name}."
        )

    except Exception as error:

        connection.rollback()

        print("Error while loading data:")
        print(error)

    finally:

        cursor.close()
        connection.close()

        print("Database connection closed.")


if __name__ == "__main__":

    load_csv_to_postgres("recharges.csv", "recharges")
    load_csv_to_postgres("usage.csv", "usage")
    load_csv_to_postgres("complaints.csv", "complaints")
    load_csv_to_postgres("network_events.csv", "network_events")
    load_csv_to_postgres("payments.csv", "payments")