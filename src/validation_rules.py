import pandas as pd


def validate_recharges(
    df,
    valid_customer_ids
):

    valid_payment_modes = [
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ]

    valid_statuses = [
        "SUCCESS",
        "FAILED",
        "PENDING"
    ]

    valid_customer = df["customer_id"].isin(
        valid_customer_ids
    )

    valid_amount = df["amount"] > 0

    valid_payment_mode = df["payment_mode"].isin(
        valid_payment_modes
    )

    valid_status = df["status"].isin(
        valid_statuses
    )

    valid_records = (
        valid_customer
        & valid_amount
        & valid_payment_mode
        & valid_status
    )

    return valid_records