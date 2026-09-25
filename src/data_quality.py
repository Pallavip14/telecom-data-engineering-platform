from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "data" / "source"


def check_record_count(df, dataset_name):

    record_count = len(df)

    print(f"Total records: {record_count}")

    if record_count > 0:
        print(f"PASS: {dataset_name} contains records.")
        return True

    print(f"FAIL: {dataset_name} is empty.")
    return False


def check_missing_values(df, dataset_name):

    missing_values = df.isnull().sum()

    total_missing = missing_values.sum()

    print(f"Total missing values: {total_missing}")

    if total_missing == 0:
        print(f"PASS: No missing values in {dataset_name}.")
        return True

    print(f"FAIL: Missing values found in {dataset_name}.")
    print(missing_values[missing_values > 0])

    return False


def check_duplicate_ids(df, id_column, dataset_name):

    duplicate_count = df[id_column].duplicated().sum()

    print(f"Duplicate {id_column}: {duplicate_count}")

    if duplicate_count == 0:
        print(f"PASS: No duplicate {id_column}.")
        return True

    print(f"FAIL: Duplicate {id_column} found.")
    return False


def check_dataset(file_name, id_column):

    print("=" * 60)
    print(f"DATA QUALITY CHECK: {file_name}")
    print("=" * 60)

    file_path = SOURCE_DIR / file_name

    df = pd.read_csv(file_path)

    all_checks_passed = True

    # Check 1
    if not check_record_count(df, file_name):
        all_checks_passed = False

    print()

    # Check 2
    if not check_missing_values(df, file_name):
        all_checks_passed = False

    print()

    # Check 3
    if not check_duplicate_ids(df, id_column, file_name):
        all_checks_passed = False

    print()

    if all_checks_passed:
        print(f"RESULT: {file_name} → PASS")
    else:
        print(f"RESULT: {file_name} → FAIL")

    print()

    return all_checks_passed
def check_plan_rules():

    file_path = SOURCE_DIR / "plans.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("BUSINESS RULE CHECK: plans.csv")
    print("=" * 60)

    all_checks_passed = True

    # Rule 1: Price must be greater than zero
    invalid_price = (df["price"] <= 0).sum()

    print(f"Invalid prices: {invalid_price}")

    if invalid_price == 0:
        print("PASS: All plan prices are valid.")
    else:
        print("FAIL: Invalid plan prices found.")
        all_checks_passed = False

    print()

    # Rule 2: Data allowance must be greater than zero
    invalid_data = (df["data_gb"] <= 0).sum()

    print(f"Invalid data allowances: {invalid_data}")

    if invalid_data == 0:
        print("PASS: All data allowances are valid.")
    else:
        print("FAIL: Invalid data allowances found.")
        all_checks_passed = False

    print()

    # Rule 3: Validity must be greater than zero
    invalid_validity = (df["validity_days"] <= 0).sum()

    print(f"Invalid validity values: {invalid_validity}")

    if invalid_validity == 0:
        print("PASS: All validity values are valid.")
    else:
        print("FAIL: Invalid validity values found.")
        all_checks_passed = False

    print()

    # Rule 4: Plan type must be valid
    valid_plan_types = ["Prepaid", "Postpaid"]

    invalid_plan_type = (
        ~df["plan_type"].isin(valid_plan_types)
    ).sum()

    print(f"Invalid plan types: {invalid_plan_type}")

    if invalid_plan_type == 0:
        print("PASS: All plan types are valid.")
    else:
        print("FAIL: Invalid plan types found.")
        all_checks_passed = False

    print()

    # Rule 5: Status must be valid
    valid_statuses = ["ACTIVE", "INACTIVE"]

    invalid_status = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    print(f"Invalid statuses: {invalid_status}")

    if invalid_status == 0:
        print("PASS: All plan statuses are valid.")
    else:
        print("FAIL: Invalid plan statuses found.")
        all_checks_passed = False

    print()

    # Final result
    if all_checks_passed:
        print("BUSINESS RULE RESULT: PASS")
    else:
        print("BUSINESS RULE RESULT: FAIL")

    print()
    
def check_recharge_rules():

    file_path = SOURCE_DIR / "recharges.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("BUSINESS RULE CHECK: recharges.csv")
    print("=" * 60)

    all_checks_passed = True

    # Rule 1: Amount must be greater than zero
    invalid_amount = (df["amount"] <= 0).sum()

    print(f"Invalid amounts: {invalid_amount}")

    if invalid_amount == 0:
        print("PASS: All recharge amounts are valid.")
    else:
        print("FAIL: Invalid recharge amounts found.")
        all_checks_passed = False

    print()

    # Rule 2: Payment mode must be valid
    valid_payment_modes = [
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ]

    invalid_payment_mode = (
        ~df["payment_mode"].isin(valid_payment_modes)
    ).sum()

    print(f"Invalid payment modes: {invalid_payment_mode}")

    if invalid_payment_mode == 0:
        print("PASS: All payment modes are valid.")
    else:
        print("FAIL: Invalid payment modes found.")
        all_checks_passed = False

    print()

    # Rule 3: Status must be valid
    valid_statuses = [
        "SUCCESS",
        "FAILED",
        "PENDING"
    ]

    invalid_status = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    print(f"Invalid statuses: {invalid_status}")

    if invalid_status == 0:
        print("PASS: All recharge statuses are valid.")
    else:
        print("FAIL: Invalid recharge statuses found.")
        all_checks_passed = False

    print()

    if all_checks_passed:
        print("RECHARGE BUSINESS RULE RESULT: PASS")
    else:
        print("RECHARGE BUSINESS RULE RESULT: FAIL")

    print()
    
def check_usage_rules():

    file_path = SOURCE_DIR / "usage.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("BUSINESS RULE CHECK: usage.csv")
    print("=" * 60)

    all_checks_passed = True

    # Data usage cannot be negative
    invalid_data = (df["data_used_gb"] < 0).sum()

    print(f"Invalid data usage values: {invalid_data}")

    if invalid_data == 0:
        print("PASS: Data usage values are valid.")
    else:
        print("FAIL: Negative data usage found.")
        all_checks_passed = False

    print()

    # Voice minutes cannot be negative
    invalid_voice = (df["voice_minutes"] < 0).sum()

    print(f"Invalid voice minutes: {invalid_voice}")

    if invalid_voice == 0:
        print("PASS: Voice minutes are valid.")
    else:
        print("FAIL: Negative voice minutes found.")
        all_checks_passed = False

    print()

    # SMS count cannot be negative
    invalid_sms = (df["sms_count"] < 0).sum()

    print(f"Invalid SMS counts: {invalid_sms}")

    if invalid_sms == 0:
        print("PASS: SMS counts are valid.")
    else:
        print("FAIL: Negative SMS counts found.")
        all_checks_passed = False

    print()

    if all_checks_passed:
        print("USAGE BUSINESS RULE RESULT: PASS")
    else:
        print("USAGE BUSINESS RULE RESULT: FAIL")

    print()
    
def check_complaint_rules():

    file_path = SOURCE_DIR / "complaints.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("BUSINESS RULE CHECK: complaints.csv")
    print("=" * 60)

    all_checks_passed = True

    valid_categories = [
        "NETWORK",
        "BILLING",
        "RECHARGE",
        "PLAN",
        "SIM",
        "OTHER"
    ]

    invalid_category = (
        ~df["category"].isin(valid_categories)
    ).sum()

    print(f"Invalid categories: {invalid_category}")

    if invalid_category == 0:
        print("PASS: Complaint categories are valid.")
    else:
        print("FAIL: Invalid complaint categories found.")
        all_checks_passed = False

    print()

    valid_priorities = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]

    invalid_priority = (
        ~df["priority"].isin(valid_priorities)
    ).sum()

    print(f"Invalid priorities: {invalid_priority}")

    if invalid_priority == 0:
        print("PASS: Complaint priorities are valid.")
    else:
        print("FAIL: Invalid complaint priorities found.")
        all_checks_passed = False

    print()

    valid_statuses = [
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ]

    invalid_status = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    print(f"Invalid statuses: {invalid_status}")

    if invalid_status == 0:
        print("PASS: Complaint statuses are valid.")
    else:
        print("FAIL: Invalid complaint statuses found.")
        all_checks_passed = False

    print()

    if all_checks_passed:
        print("COMPLAINT BUSINESS RULE RESULT: PASS")
    else:
        print("COMPLAINT BUSINESS RULE RESULT: FAIL")

    print()
    
def check_network_event_rules():

    file_path = SOURCE_DIR / "network_events.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("BUSINESS RULE CHECK: network_events.csv")
    print("=" * 60)

    all_checks_passed = True

    # Duration must be greater than zero
    invalid_duration = (df["duration_minutes"] <= 0).sum()

    print(f"Invalid durations: {invalid_duration}")

    if invalid_duration == 0:
        print("PASS: Event durations are valid.")
    else:
        print("FAIL: Invalid event durations found.")
        all_checks_passed = False

    print()

    # Affected users cannot be negative
    invalid_users = (df["affected_users"] < 0).sum()

    print(f"Invalid affected users: {invalid_users}")

    if invalid_users == 0:
        print("PASS: Affected user counts are valid.")
    else:
        print("FAIL: Invalid affected user counts found.")
        all_checks_passed = False

    print()

    valid_event_types = [
        "OUTAGE",
        "HIGH_LATENCY",
        "PACKET_LOSS",
        "LOW_SIGNAL",
        "CONGESTION"
    ]

    invalid_event_type = (
        ~df["event_type"].isin(valid_event_types)
    ).sum()

    print(f"Invalid event types: {invalid_event_type}")

    if invalid_event_type == 0:
        print("PASS: Event types are valid.")
    else:
        print("FAIL: Invalid event types found.")
        all_checks_passed = False

    print()

    valid_severities = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]

    invalid_severity = (
        ~df["severity"].isin(valid_severities)
    ).sum()

    print(f"Invalid severities: {invalid_severity}")

    if invalid_severity == 0:
        print("PASS: Severities are valid.")
    else:
        print("FAIL: Invalid severities found.")
        all_checks_passed = False

    print()

    valid_statuses = [
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ]

    invalid_status = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    print(f"Invalid statuses: {invalid_status}")

    if invalid_status == 0:
        print("PASS: Network event statuses are valid.")
    else:
        print("FAIL: Invalid network event statuses found.")
        all_checks_passed = False

    print()

    if all_checks_passed:
        print("NETWORK EVENT BUSINESS RULE RESULT: PASS")
    else:
        print("NETWORK EVENT BUSINESS RULE RESULT: FAIL")

    print()
    
def check_payment_rules():

    file_path = SOURCE_DIR / "payments.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("BUSINESS RULE CHECK: payments.csv")
    print("=" * 60)

    all_checks_passed = True

    # Amount must be greater than zero
    invalid_amount = (df["amount"] <= 0).sum()

    print(f"Invalid amounts: {invalid_amount}")

    if invalid_amount == 0:
        print("PASS: All payment amounts are valid.")
    else:
        print("FAIL: Invalid payment amounts found.")
        all_checks_passed = False

    print()

    valid_payment_methods = [
        "UPI",
        "CARD",
        "NET_BANKING",
        "WALLET"
    ]

    invalid_payment_method = (
        ~df["payment_method"].isin(valid_payment_methods)
    ).sum()

    print(f"Invalid payment methods: {invalid_payment_method}")

    if invalid_payment_method == 0:
        print("PASS: Payment methods are valid.")
    else:
        print("FAIL: Invalid payment methods found.")
        all_checks_passed = False

    print()

    valid_statuses = [
        "SUCCESS",
        "FAILED",
        "PENDING",
        "REFUNDED"
    ]

    invalid_status = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    print(f"Invalid statuses: {invalid_status}")

    if invalid_status == 0:
        print("PASS: Payment statuses are valid.")
    else:
        print("FAIL: Invalid payment statuses found.")
        all_checks_passed = False

    print()

    if all_checks_passed:
        print("PAYMENT BUSINESS RULE RESULT: PASS")
    else:
        print("PAYMENT BUSINESS RULE RESULT: FAIL")

    print()
def check_reference_integrity(
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship_name
):

    invalid_count = (
        ~child_df[child_column].isin(parent_df[parent_column])
    ).sum()

    print(f"{relationship_name}: {invalid_count} invalid records")

    if invalid_count == 0:
        print(f"PASS: {relationship_name}")
        return True

    print(f"FAIL: {relationship_name}")
    return False
def check_relationships():

    print("=" * 60)
    print("REFERENTIAL INTEGRITY CHECKS")
    print("=" * 60)

    customers = pd.read_csv(SOURCE_DIR / "customers.csv")
    plans = pd.read_csv(SOURCE_DIR / "plans.csv")
    recharges = pd.read_csv(SOURCE_DIR / "recharges.csv")
    usage = pd.read_csv(SOURCE_DIR / "usage.csv")
    complaints = pd.read_csv(SOURCE_DIR / "complaints.csv")
    payments = pd.read_csv(SOURCE_DIR / "payments.csv")

    check_reference_integrity(
        customers,
        "plan_id",
        plans,
        "plan_id",
        "customers.plan_id → plans.plan_id"
    )

    check_reference_integrity(
        recharges,
        "customer_id",
        customers,
        "customer_id",
        "recharges.customer_id → customers.customer_id"
    )

    check_reference_integrity(
        usage,
        "customer_id",
        customers,
        "customer_id",
        "usage.customer_id → customers.customer_id"
    )

    check_reference_integrity(
        complaints,
        "customer_id",
        customers,
        "customer_id",
        "complaints.customer_id → customers.customer_id"
    )

    check_reference_integrity(
        payments,
        "customer_id",
        customers,
        "customer_id",
        "payments.customer_id → customers.customer_id"
    )

    print()
    
if __name__ == "__main__":

    check_dataset(
        "customers.csv",
        "customer_id"
    )

    check_dataset(
        "plans.csv",
        "plan_id"
    )

    check_dataset(
        "recharges.csv",
        "recharge_id"
    )

    check_dataset(
        "usage.csv",
        "usage_id"
    )

    check_dataset(
        "complaints.csv",
        "complaint_id"
    )

    check_dataset(
        "network_events.csv",
        "event_id"
    )

    check_dataset(
        "payments.csv",
        "payment_id"
    )
    check_plan_rules()
    check_recharge_rules()
    check_usage_rules()
    check_complaint_rules()
    check_network_event_rules()
    check_payment_rules()
    check_relationships()