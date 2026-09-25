from pathlib import Path

import pandas as pd

from process_dataset import process_dataset


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_customers(df, valid_plan_ids):

    valid_plan = df["plan_id"].isin(valid_plan_ids)

    valid_status = df["status"].isin([
        "ACTIVE",
        "INACTIVE"
    ])

    valid_records = (
        valid_plan
        & valid_status
    )

    return valid_records


def validate_plans(df):

    valid_price = df["price"] > 0

    valid_data = df["data_gb"] > 0

    valid_validity = df["validity_days"] > 0

    valid_plan_type = df["plan_type"].isin([
        "Prepaid",
        "Postpaid"
    ])

    valid_status = df["status"].isin([
        "ACTIVE",
        "INACTIVE"
    ])

    valid_records = (
        valid_price
        & valid_data
        & valid_validity
        & valid_plan_type
        & valid_status
    )

    return valid_records


def validate_recharges(df, valid_customer_ids):

    valid_customer = df["customer_id"].isin(
        valid_customer_ids
    )

    valid_amount = df["amount"] > 0

    valid_payment_mode = df["payment_mode"].isin([
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ])

    valid_status = df["status"].isin([
        "SUCCESS",
        "FAILED",
        "PENDING"
    ])

    valid_records = (
        valid_customer
        & valid_amount
        & valid_payment_mode
        & valid_status
    )

    return valid_records


def validate_usage(df, valid_customer_ids):

    valid_customer = df["customer_id"].isin(
        valid_customer_ids
    )

    valid_data = df["data_used_gb"] >= 0

    valid_voice = df["voice_minutes"] >= 0

    valid_sms = df["sms_count"] >= 0

    valid_records = (
        valid_customer
        & valid_data
        & valid_voice
        & valid_sms
    )

    return valid_records


def validate_complaints(df, valid_customer_ids):

    valid_customer = df["customer_id"].isin(
        valid_customer_ids
    )

    valid_category = df["category"].isin([
        "NETWORK",
        "BILLING",
        "RECHARGE",
        "PLAN",
        "SIM",
        "OTHER"
    ])

    valid_priority = df["priority"].isin([
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ])

    valid_status = df["status"].isin([
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ])

    valid_records = (
        valid_customer
        & valid_category
        & valid_priority
        & valid_status
    )

    return valid_records


def validate_network_events(df):

    valid_duration = df["duration_minutes"] > 0

    valid_affected_users = df["affected_users"] >= 0

    valid_event_type = df["event_type"].isin([
        "OUTAGE",
        "HIGH_LATENCY",
        "PACKET_LOSS",
        "LOW_SIGNAL",
        "CONGESTION"
    ])

    valid_severity = df["severity"].isin([
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ])

    valid_status = df["status"].isin([
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ])

    valid_records = (
        valid_duration
        & valid_affected_users
        & valid_event_type
        & valid_severity
        & valid_status
    )

    return valid_records


def validate_payments(df, valid_customer_ids):

    valid_customer = df["customer_id"].isin(
        valid_customer_ids
    )

    valid_amount = df["amount"] > 0

    valid_payment_method = df["payment_method"].isin([
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ])

    valid_status = df["status"].isin([
        "SUCCESS",
        "FAILED",
        "PENDING",
        "REFUNDED"
    ])

    valid_records = (
        valid_customer
        & valid_amount
        & valid_payment_method
        & valid_status
    )

    return valid_records


# ============================================================
# MAIN PIPELINE
# ============================================================

def process_all():

    print()
    print("=" * 60)
    print("TELECONNECT DATA PROCESSING PIPELINE")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Load reference data
    # --------------------------------------------------------

    customers_df = pd.read_csv(
        SOURCE_DIR / "customers.csv"
    )

    plans_df = pd.read_csv(
        SOURCE_DIR / "plans.csv"
    )

    valid_customer_ids = set(
        customers_df["customer_id"]
    )

    valid_plan_ids = set(
        plans_df["plan_id"]
    )

    # --------------------------------------------------------
    # 1. Customers
    # --------------------------------------------------------

    process_dataset(
        file_name="customers.csv",
        validation_function=validate_customers,
        validation_arguments={
            "valid_plan_ids": valid_plan_ids
        }
    )

    # --------------------------------------------------------
    # 2. Plans
    # --------------------------------------------------------

    process_dataset(
        file_name="plans.csv",
        validation_function=validate_plans
    )

    # --------------------------------------------------------
    # 3. Recharges
    # --------------------------------------------------------

    process_dataset(
        file_name="recharges.csv",
        validation_function=validate_recharges,
        validation_arguments={
            "valid_customer_ids": valid_customer_ids
        }
    )

    # --------------------------------------------------------
    # 4. Usage
    # --------------------------------------------------------

    process_dataset(
        file_name="usage.csv",
        validation_function=validate_usage,
        validation_arguments={
            "valid_customer_ids": valid_customer_ids
        }
    )

    # --------------------------------------------------------
    # 5. Complaints
    # --------------------------------------------------------

    process_dataset(
        file_name="complaints.csv",
        validation_function=validate_complaints,
        validation_arguments={
            "valid_customer_ids": valid_customer_ids
        }
    )

    # --------------------------------------------------------
    # 6. Network Events
    # --------------------------------------------------------

    process_dataset(
        file_name="network_events.csv",
        validation_function=validate_network_events
    )

    # --------------------------------------------------------
    # 7. Payments
    # --------------------------------------------------------

    process_dataset(
        file_name="payments.csv",
        validation_function=validate_payments,
        validation_arguments={
            "valid_customer_ids": valid_customer_ids
        }
    )

    print("=" * 60)
    print("ALL DATASETS PROCESSED")
    print("=" * 60)


if __name__ == "__main__":
    process_all()