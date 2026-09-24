import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def generate_payments(number_of_records=12000):

    # Read existing customers
    customers_file = SOURCE_DIR / "customers.csv"
    customers_df = pd.read_csv(customers_file)

    # Get valid customer IDs
    customer_ids = customers_df["customer_id"].tolist()

    payment_methods = [
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ]

    payment_statuses = [
        "SUCCESS",
        "SUCCESS",
        "SUCCESS",
        "SUCCESS",
        "FAILED",
        "PENDING",
        "REFUNDED"
    ]

    start_date = date.today() - timedelta(days=365)

    data = []

    for i in range(1, number_of_records + 1):

        payment_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        data.append({
            "payment_id": f"PAY{i:06d}",
            "customer_id": random.choice(customer_ids),
            "payment_date": payment_date,
            "amount": random.choice([
                199,
                299,
                399,
                499,
                599,
                799,
                999,
                1499
            ]),
            "payment_method": random.choice(payment_methods),
            "status": random.choice(payment_statuses)
        })

    df = pd.DataFrame(data)

    output_file = SOURCE_DIR / "payments.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} payment records.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_payments()