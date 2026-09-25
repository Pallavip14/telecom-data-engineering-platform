from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def simulate_bad_recharges():

    input_file = SOURCE_DIR / "recharges.csv"

    df = pd.read_csv(input_file)

    print(f"Original records: {len(df)}")

    # Introduce an invalid customer ID
    df.loc[0, "customer_id"] = "C999999"

    # Introduce an invalid amount
    df.loc[1, "amount"] = -100

    # Introduce an invalid payment mode
    df.loc[2, "payment_mode"] = "CASH"

    # Introduce an invalid status
    df.loc[3, "status"] = "INVALID"

    df.to_csv(input_file, index=False)

    print("Bad data successfully introduced.")
    print("Modified file:", input_file)


if __name__ == "__main__":
    simulate_bad_recharges()