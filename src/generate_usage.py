import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def generate_usage(number_of_records=20000):

    # Read existing customers
    customers_file = SOURCE_DIR / "customers.csv"
    customers_df = pd.read_csv(customers_file)

    # Get valid customer IDs
    customer_ids = customers_df["customer_id"].tolist()

    # Generate usage dates for the last 365 days
    start_date = date.today() - timedelta(days=365)

    data = []

    for i in range(1, number_of_records + 1):

        usage_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        data.append({
            "usage_id": f"U{i:06d}",
            "customer_id": random.choice(customer_ids),
            "usage_date": usage_date,
            "data_used_gb": round(random.uniform(0.1, 5.0), 2),
            "voice_minutes": random.randint(0, 300),
            "sms_count": random.randint(0, 100)
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save CSV
    output_file = SOURCE_DIR / "usage.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} usage records.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_usage()