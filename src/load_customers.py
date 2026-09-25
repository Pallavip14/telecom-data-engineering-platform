from pathlib import Path

import pandas as pd

from database import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = BASE_DIR / "data" / "source" / "customers.csv"


def load_customers():

    print("Reading customers.csv...")

    df = pd.read_csv(SOURCE_FILE)

    print(f"Records found in CSV: {len(df)}")

    connection = get_connection()

    cursor = connection.cursor()

    try:

        for _, row in df.iterrows():

            cursor.execute(
                """
                INSERT INTO raw.customers (
                    customer_id,
                    first_name,
                    last_name,
                    gender,
                    date_of_birth,
                    city,
                    state,
                    registration_date,
                    plan_id,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                ON CONFLICT (customer_id)
                DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    gender = EXCLUDED.gender,
                    date_of_birth = EXCLUDED.date_of_birth,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state,
                    registration_date = EXCLUDED.registration_date,
                    plan_id = EXCLUDED.plan_id,
                    status = EXCLUDED.status
                """,
                (
                    row["customer_id"],
                    row["first_name"],
                    row["last_name"],
                    row["gender"],
                    row["date_of_birth"],
                    row["city"],
                    row["state"],
                    row["registration_date"],
                    row["plan_id"],
                    row["status"]
                )
            )

        connection.commit()

        print(f"Successfully loaded {len(df)} records into raw.customers.")

    except Exception as error:

        connection.rollback()

        print("Error while loading customers:")
        print(error)

    finally:

        cursor.close()
        connection.close()

        print("Database connection closed.")


if __name__ == "__main__":
    load_customers()