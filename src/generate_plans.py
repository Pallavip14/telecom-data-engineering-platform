import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"

SOURCE_DIR.mkdir(parents=True, exist_ok=True)


def generate_plans():

    plans = [
        {
            "plan_id": "P001",
            "plan_name": "Smart 299",
            "plan_type": "Prepaid",
            "price": 299,
            "data_gb": 1.5,
            "validity_days": 28,
            "voice_minutes": 1000,
            "sms_limit": 100,
            "status": "ACTIVE"
        },
        {
            "plan_id": "P002",
            "plan_name": "Smart 499",
            "plan_type": "Prepaid",
            "price": 499,
            "data_gb": 2.0,
            "validity_days": 28,
            "voice_minutes": 1500,
            "sms_limit": 100,
            "status": "ACTIVE"
        },
        {
            "plan_id": "P003",
            "plan_name": "Premium 799",
            "plan_type": "Postpaid",
            "price": 799,
            "data_gb": 2.5,
            "validity_days": 30,
            "voice_minutes": 2000,
            "sms_limit": 200,
            "status": "ACTIVE"
        },
        {
            "plan_id": "P004",
            "plan_name": "Basic 199",
            "plan_type": "Prepaid",
            "price": 199,
            "data_gb": 1.0,
            "validity_days": 28,
            "voice_minutes": 500,
            "sms_limit": 50,
            "status": "ACTIVE"
        }
    ]

    df = pd.DataFrame(plans)

    output_file = SOURCE_DIR / "plans.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} plans.")
    print(f"File created: {output_file}")


if __name__ == "__main__":
    generate_plans()