import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def generate_recharges(number_of_records=10000):

    # Read existing customers
    customers_file = SOURCE_DIR / "customers.csv"
    customers_df = pd.read_csv(customers_file)

    # Get valid customer IDs
    customer_ids = customers_df["customer_id"].tolist()

    # Possible recharge values
    recharge_amounts = [199, 299, 399, 499, 599, 799, 999]

    # Payment methods
    payment_modes = [
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ]

    # Recharge statuses
    statuses = [
        "SUCCESS",
        "SUCCESS",
        "SUCCESS",
        "SUCCESS",
        "FAILED",
        "PENDING"
    ]

    # Generate dates for the last 365 days
    start_date = date.today() - timedelta(days=365)

    data = []

    for i in range(1, number_of_records + 1):

        recharge_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        data.append({
            "recharge_id": f"R{i:06d}",
            "customer_id": random.choice(customer_ids),
            "recharge_date": recharge_date,
            "amount": random.choice(recharge_amounts),
            "payment_mode": random.choice(payment_modes),
            "status": random.choice(statuses)
        })

    # Convert generated data into DataFrame
    df = pd.DataFrame(data)

    # Output file
    output_file = SOURCE_DIR / "recharges.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} recharge records.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_recharges()