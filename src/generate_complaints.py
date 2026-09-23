import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def generate_complaints(number_of_records=5000):

    # Read existing customers
    customers_file = SOURCE_DIR / "customers.csv"
    customers_df = pd.read_csv(customers_file)

    # Get valid customer IDs
    customer_ids = customers_df["customer_id"].tolist()

    categories = [
        "NETWORK",
        "BILLING",
        "RECHARGE",
        "PLAN",
        "SIM",
        "OTHER"
    ]

    priorities = [
        "LOW",
        "MEDIUM",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]

    statuses = [
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ]

    complaint_titles = {
        "NETWORK": [
            "Internet not working",
            "Slow internet",
            "Network issue",
            "Poor network coverage"
        ],
        "BILLING": [
            "Incorrect bill amount",
            "Billing issue",
            "Unexpected charge"
        ],
        "RECHARGE": [
            "Recharge failed",
            "Recharge amount not reflected",
            "Recharge issue"
        ],
        "PLAN": [
            "Plan benefits not received",
            "Plan activation issue",
            "Plan related query"
        ],
        "SIM": [
            "SIM not working",
            "SIM activation issue",
            "SIM replacement request"
        ],
        "OTHER": [
            "General complaint",
            "Service related issue",
            "Other issue"
        ]
    }

    start_date = date.today() - timedelta(days=365)

    data = []

    for i in range(1, number_of_records + 1):

        category = random.choice(categories)

        complaint_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        data.append({
            "complaint_id": f"CP{i:06d}",
            "customer_id": random.choice(customer_ids),
            "complaint_date": complaint_date,
            "category": category,
            "title": random.choice(complaint_titles[category]),
            "priority": random.choice(priorities),
            "status": random.choice(statuses)
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save CSV
    output_file = SOURCE_DIR / "complaints.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} complaint records.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_complaints()