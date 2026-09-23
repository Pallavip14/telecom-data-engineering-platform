import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"

SOURCE_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(number_of_records=1000):

    plans = ["P001", "P002", "P003", "P004"]

    data = []

    for i in range(1, number_of_records + 1):

        data.append({
            "customer_id": f"C{i:06d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "gender": random.choice(["Male", "Female"]),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18,
                maximum_age=70
            ),
            "city": random.choice([
                "Mumbai",
                "Pune",
                "Nagpur",
                "Nashik",
                "Thane",
                "Indore",
                "Bhopal"
            ]),
            "state": random.choice([
                "Maharashtra",
                "Madhya Pradesh"
            ]),
            "registration_date": fake.date_between(
                start_date="-3y",
                end_date="today"
            ),
            "plan_id": random.choice(plans),
            "status": random.choice([
                "ACTIVE",
                "ACTIVE",
                "ACTIVE",
                "INACTIVE"
            ])
        })

    df = pd.DataFrame(data)

    output_file = SOURCE_DIR / "customers.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} customer records.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_customers()