import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def generate_network_events(number_of_records=3000):

    cities = [
        "Mumbai",
        "Pune",
        "Nagpur",
        "Nashik",
        "Thane",
        "Indore",
        "Bhopal"
    ]

    event_types = [
        "OUTAGE",
        "HIGH_LATENCY",
        "PACKET_LOSS",
        "LOW_SIGNAL",
        "CONGESTION"
    ]

    severities = [
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

    start_date = date.today() - timedelta(days=365)

    data = []

    for i in range(1, number_of_records + 1):

        event_date = start_date + timedelta(
            days=random.randint(0, 364)
        )

        data.append({
            "event_id": f"NE{i:06d}",
            "event_date": event_date,
            "city": random.choice(cities),
            "event_type": random.choice(event_types),
            "severity": random.choice(severities),
            "duration_minutes": random.randint(5, 300),
            "affected_users": random.randint(10, 5000),
            "status": random.choice(statuses)
        })

    df = pd.DataFrame(data)

    output_file = SOURCE_DIR / "network_events.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} network event records.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_network_events()