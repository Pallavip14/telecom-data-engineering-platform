from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "data" / "source"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REJECTED_DIR = BASE_DIR / "data" / "rejected"


PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)


def process_dataset(
    file_name,
    validation_function,
    validation_arguments=None
):

    input_file = SOURCE_DIR / file_name

    df = pd.read_csv(input_file)

    print("=" * 60)
    print(f"PROCESSING: {file_name}")
    print("=" * 60)

    print(f"Input records: {len(df)}")

    if validation_arguments is None:

        valid_records = validation_function(df)

    else:

        valid_records = validation_function(
            df,
            **validation_arguments
        )

    valid_df = df[valid_records].copy()

    rejected_df = df[~valid_records].copy()

    dataset_name = Path(file_name).stem

    processed_file = (
        PROCESSED_DIR /
        f"{dataset_name}_valid.csv"
    )

    rejected_file = (
        REJECTED_DIR /
        f"{dataset_name}_rejected.csv"
    )

    valid_df.to_csv(
        processed_file,
        index=False
    )

    rejected_df.to_csv(
        rejected_file,
        index=False
    )

    print(f"Valid records: {len(valid_df)}")
    print(f"Rejected records: {len(rejected_df)}")

    print(f"Processed file: {processed_file}")
    print(f"Rejected file: {rejected_file}")

    print()

    return valid_df, rejected_df