import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# FILE CONFIGURATION
# ============================================================

project_root = Path(__file__).resolve().parent.parent

data_path = (
    project_root
    / "data"
    / "upi_transactions.csv"
)

print("UPI Transaction Data Validation")
print("-" * 40)
print(f"Reading dataset from:\n{data_path}")

# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    data_path,
    parse_dates=["txn_timestamp"]
)

print("\nDataset loaded successfully.")

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Information:")
df.info()

# ============================================================
# SCHEMA VALIDATION
# ============================================================

expected_columns = [
    "transaction_id",
    "user_id",
    "txn_timestamp",
    "amount",
    "status",
    "failure_reason",
    "bank_name",
    "app_version",
    "device_type",
    "city",
]

actual_columns = df.columns.tolist()

assert actual_columns == expected_columns, \
    "Dataset schema does not match expected schema."

print("\n✓ Schema validation passed.")

# ============================================================
# COMPLETENESS VALIDATION
# ============================================================

null_summary = pd.DataFrame({
    "null_count": df.isna().sum(),
    "null_percentage": (
        df.isna().mean() * 100
    )
})

print("\nMissing Value Summary:")
print(null_summary.round(2))

mandatory_columns = [
    "transaction_id",
    "user_id",
    "txn_timestamp",
    "amount",
    "status",
    "bank_name",
    "app_version",
    "device_type",
    "city",
]

assert df[mandatory_columns].notna().all().all(), \
    "Unexpected null values found in mandatory columns."

print("✓ Mandatory-field completeness validation passed.")

# ============================================================
# UNIQUENESS AND DUPLICATE VALIDATION
# ============================================================

duplicate_transaction_ids = (
    df["transaction_id"].duplicated().sum()
)

duplicate_rows = (
    df.duplicated().sum()
)

print("\nDuplicate Check:")
print(
    f"Duplicate transaction IDs: "
    f"{duplicate_transaction_ids:,}"
)

print(
    f"Fully duplicated rows: "
    f"{duplicate_rows:,}"
)

assert duplicate_transaction_ids == 0, \
    "Duplicate transaction IDs found."

assert duplicate_rows == 0, \
    "Fully duplicated rows found."

print("✓ Duplicate validation passed.")

# ============================================================
# BUSINESS RULE VALIDATION
# ============================================================

print("\nRunning business rule validations...")

allowed_statuses = {
    "SUCCESS",
    "FAILED"
}

unexpected_statuses = (
    set(df["status"].dropna().unique())
    - allowed_statuses
)

assert len(unexpected_statuses) == 0, \
    f"Unexpected transaction statuses found: {unexpected_statuses}"

print("✓ Transaction status validation passed.")

successful_transactions = (
    df["status"] == "SUCCESS"
)

failed_transactions = (
    df["status"] == "FAILED"
)


success_with_failure_reason = (
    df.loc[
        successful_transactions,
        "failure_reason"
    ]
    .notna()
    .sum()
)

failed_without_failure_reason = (
    df.loc[
        failed_transactions,
        "failure_reason"
    ]
    .isna()
    .sum()
)

print("\nStatus / Failure Reason Consistency:")
print(
    f"SUCCESS transactions with failure reason: "
    f"{success_with_failure_reason:,}"
)

print(
    f"FAILED transactions without failure reason: "
    f"{failed_without_failure_reason:,}"
)

assert success_with_failure_reason == 0, \
    "Successful transactions contain failure reasons."

assert failed_without_failure_reason == 0, \
    "Failed transactions contain missing failure reasons."

print("✓ Status/failure-reason consistency passed.")

allowed_failure_reasons = {
    "BANK_SERVER_ERROR",
    "NETWORK_ERROR",
    "INSUFFICIENT_FUNDS",
    "TECHNICAL_ERROR",
    "TIMEOUT",
}

observed_failure_reasons = set(
    df.loc[
        failed_transactions,
        "failure_reason"
    ]
    .dropna()
    .unique()
)

unexpected_failure_reasons = (
    observed_failure_reasons
    - allowed_failure_reasons
)

assert len(unexpected_failure_reasons) == 0, \
    f"Unexpected failure reasons found: {unexpected_failure_reasons}"

print("✓ Failure reason category validation passed.")

invalid_amounts = df[
    (df["amount"] < 10)
    | (df["amount"] > 50_000)
]

print(
    f"\nTransactions with invalid amounts: "
    f"{len(invalid_amounts):,}"
)

assert len(invalid_amounts) == 0, \
    "Transaction amounts outside allowed range found."

print("✓ Transaction amount range validation passed.")

assert (df["amount"] > 0).all(), \
    "Zero or negative transaction amounts found."

print("✓ Positive transaction amount validation passed.")

analysis_start = pd.Timestamp(
    "2025-01-01 00:00:00"
)

analysis_end = pd.Timestamp(
    "2025-12-31 23:59:59"
)

invalid_timestamps = df[
    (df["txn_timestamp"] < analysis_start)
    | (df["txn_timestamp"] > analysis_end)
]

print(
    f"\nTransactions outside analysis period: "
    f"{len(invalid_timestamps):,}"
)

assert len(invalid_timestamps) == 0, \
    "Transactions outside analysis period found."

print("✓ Transaction timestamp validation passed.")

print(
    f"Earliest transaction: "
    f"{df['txn_timestamp'].min()}"
)

print(
    f"Latest transaction: "
    f"{df['txn_timestamp'].max()}"
)

allowed_banks = {
    "SBI",
    "HDFC",
    "ICICI",
    "Axis",
    "Kotak",
    "PNB",
}

unexpected_banks = (
    set(df["bank_name"].dropna().unique())
    - allowed_banks
)

assert len(unexpected_banks) == 0, \
    f"Unexpected banks found: {unexpected_banks}"

print("✓ Bank category validation passed.")

allowed_cities = {
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Ahmedabad",
    "Jaipur",
    "Lucknow",
}

unexpected_cities = (
    set(df["city"].dropna().unique())
    - allowed_cities
)

assert len(unexpected_cities) == 0, \
    f"Unexpected cities found: {unexpected_cities}"

print("✓ City category validation passed.")

allowed_devices = {
    "Android",
    "iOS",
}

unexpected_devices = (
    set(df["device_type"].dropna().unique())
    - allowed_devices
)

assert len(unexpected_devices) == 0, \
    f"Unexpected device types found: {unexpected_devices}"

print("✓ Device category validation passed.")

allowed_app_versions = {
    "4.0.0",
    "4.1.0",
    "4.2.0",
    "4.3.0",
    "5.0.0",
}

unexpected_app_versions = (
    set(df["app_version"].dropna().unique())
    - allowed_app_versions
)

assert len(unexpected_app_versions) == 0, \
    f"Unexpected app versions found: {unexpected_app_versions}"

print("✓ App-version category validation passed.")

valid_transaction_id_format = (
    df["transaction_id"]
    .str.match(r"^TXN\d{7}$")
)

invalid_transaction_id_count = (
    (~valid_transaction_id_format)
    .sum()
)

print(
    f"\nInvalid transaction ID formats: "
    f"{invalid_transaction_id_count:,}"
)

assert invalid_transaction_id_count == 0, \
    "Invalid transaction ID format found."

print("✓ Transaction ID format validation passed.")

valid_user_id_format = (
    df["user_id"]
    .str.match(r"^USER\d{6}$")
)

invalid_user_id_count = (
    (~valid_user_id_format)
    .sum()
)

print(
    f"Invalid user ID formats: "
    f"{invalid_user_id_count:,}"
)

assert invalid_user_id_count == 0, \
    "Invalid user ID format found."

print("✓ User ID format validation passed.")

print("\n" + "=" * 50)
print("BUSINESS RULE VALIDATION SUMMARY")
print("=" * 50)

print("✓ Status values valid")
print("✓ Status/failure reason relationship valid")
print("✓ Failure reason categories valid")
print("✓ Transaction amounts valid")
print("✓ Transaction timestamps valid")
print("✓ Bank categories valid")
print("✓ City categories valid")
print("✓ Device categories valid")
print("✓ App-version categories valid")
print("✓ Transaction ID format valid")
print("✓ User ID format valid")

print("=" * 50)
print("All business rule validations passed.")

# ============================================================
# DISTRIBUTION AND ANOMALY VALIDATION
# ============================================================

print("\nRunning distribution and anomaly checks...")

status_distribution = (
    df["status"]
    .value_counts()
)

status_percentage = (
    df["status"]
    .value_counts(normalize=True)
    .mul(100)
)

status_summary = pd.DataFrame({
    "Count": status_distribution,
    "Percentage": status_percentage
})

print("\nTransaction Status Distribution:")
print(status_summary.round(2))

overall_failure_rate = (
    df["status"]
    .eq("FAILED")
    .mean()
)

print(
    f"\nOverall Failure Rate: "
    f"{overall_failure_rate:.2%}"
)

assert 0.03 <= overall_failure_rate <= 0.10, \
    "Overall failure rate appears unreasonable."

print("✓ Overall failure rate sanity check passed.")
bank_distribution = (
    df["bank_name"]
    .value_counts(normalize=True)
    .mul(100)
)

print("\nBank Transaction Distribution (%):")
print(bank_distribution.round(2))
expected_bank_distribution = {
    "SBI": 25,
    "HDFC": 20,
    "ICICI": 18,
    "Axis": 15,
    "Kotak": 12,
    "PNB": 10,
}

bank_comparison = pd.DataFrame({
    "Expected_Percentage":
        pd.Series(expected_bank_distribution),

    "Observed_Percentage":
        bank_distribution
})

bank_comparison["Difference_pp"] = (
    bank_comparison["Observed_Percentage"]
    - bank_comparison["Expected_Percentage"]
)

print("\nExpected vs Observed Bank Distribution:")
print(bank_comparison.round(2))

assert (
    bank_comparison["Difference_pp"]
    .abs()
    <= 1.0
).all(), \
    "Bank distribution differs significantly from design."

print("✓ Bank distribution validation passed.")
device_distribution = (
    df["device_type"]
    .value_counts(normalize=True)
    .mul(100)
)

print("\nDevice Distribution (%):")
print(device_distribution.round(2))
expected_device_distribution = {
    "Android": 80,
    "iOS": 20,
}

device_comparison = pd.DataFrame({
    "Expected_Percentage":
        pd.Series(expected_device_distribution),

    "Observed_Percentage":
        device_distribution
})

device_comparison["Difference_pp"] = (
    device_comparison["Observed_Percentage"]
    - device_comparison["Expected_Percentage"]
)

print("\nExpected vs Observed Device Distribution:")
print(device_comparison.round(2))
assert (
    device_comparison["Difference_pp"]
    .abs()
    <= 1.0
).all(), \
    "Device distribution differs significantly from design."

print("✓ Device distribution validation passed.")
expected_city_distribution = {
    "Delhi": 15,
    "Mumbai": 15,
    "Bengaluru": 14,
    "Hyderabad": 11,
    "Chennai": 10,
    "Kolkata": 9,
    "Pune": 8,
    "Ahmedabad": 7,
    "Jaipur": 6,
    "Lucknow": 5,
}

city_distribution = (
    df["city"]
    .value_counts(normalize=True)
    .mul(100)
)

city_comparison = pd.DataFrame({
    "Expected_Percentage":
        pd.Series(expected_city_distribution),

    "Observed_Percentage":
        city_distribution
})

city_comparison["Difference_pp"] = (
    city_comparison["Observed_Percentage"]
    - city_comparison["Expected_Percentage"]
)

print("\nExpected vs Observed City Distribution:")
print(city_comparison.round(2))
assert (
    city_comparison["Difference_pp"]
    .abs()
    <= 1.0
).all(), \
    "City distribution differs significantly from design."

print("✓ City distribution validation passed.")
amount_stats = df["amount"].describe(
    percentiles=[
        0.50,
        0.90,
        0.95,
        0.99
    ]
)

print("\nTransaction Amount Statistics:")
print(amount_stats.round(2))
amount_mean = df["amount"].mean()
amount_median = df["amount"].median()

print(
    f"\nMean Transaction Amount: "
    f"₹{amount_mean:,.2f}"
)

print(
    f"Median Transaction Amount: "
    f"₹{amount_median:,.2f}"
)
assert amount_mean > amount_median, \
    "Transaction amounts do not appear right-skewed."

print("✓ Transaction amount skewness sanity check passed.")
minimum_boundary_count = (
    df["amount"] == 10
).sum()

maximum_boundary_count = (
    df["amount"] == 50_000
).sum()

minimum_boundary_percentage = (
    minimum_boundary_count
    / len(df)
    * 100
)

maximum_boundary_percentage = (
    maximum_boundary_count
    / len(df)
    * 100
)

print("\nAmount Boundary Check:")

print(
    f"Transactions exactly ₹10: "
    f"{minimum_boundary_count:,} "
    f"({minimum_boundary_percentage:.4f}%)"
)

print(
    f"Transactions exactly ₹50,000: "
    f"{maximum_boundary_count:,} "
    f"({maximum_boundary_percentage:.4f}%)"
)
assert minimum_boundary_percentage < 5, \
    "Too many transactions concentrated at minimum amount."

assert maximum_boundary_percentage < 1, \
    "Too many transactions concentrated at maximum amount."

print("✓ Amount boundary concentration check passed.")
monthly_counts = (
    df["txn_timestamp"]
    .dt.to_period("M")
    .value_counts()
    .sort_index()
)

print("\nMonthly Transaction Volume:")
print(monthly_counts)
assert len(monthly_counts) == 12, \
    "Not all 12 months contain transactions."

assert (monthly_counts > 0).all(), \
    "One or more months contain no transactions."

print("✓ Monthly coverage validation passed.")
daily_counts = (
    df["txn_timestamp"]
    .dt.date
    .value_counts()
)

print(
    f"\nUnique transaction dates: "
    f"{len(daily_counts):,}"
)

assert len(daily_counts) == 365, \
    "Not all calendar dates contain transactions."

print("✓ Daily coverage validation passed.")
app_month_distribution = pd.crosstab(
    df["txn_timestamp"].dt.month,
    df["app_version"],
    normalize="index"
) * 100

print("\nApp Version Distribution by Month (%):")
print(app_month_distribution.round(2))
q1_5_share = (
    df.loc[
        df["txn_timestamp"].dt.quarter == 1,
        "app_version"
    ]
    .eq("5.0.0")
    .mean()
)

q4_5_share = (
    df.loc[
        df["txn_timestamp"].dt.quarter == 4,
        "app_version"
    ]
    .eq("5.0.0")
    .mean()
)

print(
    f"\n5.0.0 share in Q1: "
    f"{q1_5_share:.2%}"
)

print(
    f"5.0.0 share in Q4: "
    f"{q4_5_share:.2%}"
)

assert q4_5_share > q1_5_share, \
    "Expected app-version rollout pattern not found."

print("✓ App-version rollout sanity check passed.")
user_transaction_counts = (
    df["user_id"]
    .value_counts()
)

print("\nUser Activity Statistics:")
print(
    user_transaction_counts
    .describe(
        percentiles=[
            0.50,
            0.90,
            0.95,
            0.99
        ]
    )
    .round(2)
)
print(
    f"\nUnique active users: "
    f"{df['user_id'].nunique():,}"
)

print(
    f"Maximum transactions by one user: "
    f"{user_transaction_counts.max():,}"
)
bank_failure_rates = (
    df.assign(
        failure_flag=(
            df["status"] == "FAILED"
        ).astype(int)
    )
    .groupby("bank_name")["failure_flag"]
    .agg(
        transaction_count="count",
        failed_transactions="sum",
        failure_rate="mean"
    )
)

bank_failure_rates["failure_rate"] *= 100

bank_failure_rates = (
    bank_failure_rates
    .sort_values(
        "failure_rate",
        ascending=False
    )
)

print("\nFailure Rate by Bank:")
print(bank_failure_rates.round(2))
app_failure_rates = (
    df.assign(
        failure_flag=(
            df["status"] == "FAILED"
        ).astype(int)
    )
    .groupby("app_version")["failure_flag"]
    .agg(
        transaction_count="count",
        failed_transactions="sum",
        failure_rate="mean"
    )
)

app_failure_rates["failure_rate"] *= 100

app_failure_rates = (
    app_failure_rates
    .sort_values(
        "failure_rate",
        ascending=False
    )
)

print("\nFailure Rate by App Version:")
print(app_failure_rates.round(2))
failure_reason_distribution = (
    df.loc[
        df["status"] == "FAILED",
        "failure_reason"
    ]
    .value_counts()
)

failure_reason_percentage = (
    df.loc[
        df["status"] == "FAILED",
        "failure_reason"
    ]
    .value_counts(normalize=True)
    .mul(100)
)

failure_reason_summary = pd.DataFrame({
    "Count": failure_reason_distribution,
    "Percentage": failure_reason_percentage
})

print("\nFailure Reason Distribution:")
print(failure_reason_summary.round(2))
assert len(failure_reason_summary) == 5, \
    "One or more expected failure reasons are absent."

print("✓ Failure reason distribution sanity check passed.")
total_gmv = df["amount"].sum()

failed_gmv = (
    df.loc[
        df["status"] == "FAILED",
        "amount"
    ]
    .sum()
)

failed_gmv_rate = (
    failed_gmv
    / total_gmv
)

print("\nGMV Sanity Check:")

print(
    f"Total GMV: "
    f"₹{total_gmv:,.2f}"
)

print(
    f"Failed GMV / GMV at Risk: "
    f"₹{failed_gmv:,.2f}"
)

print(
    f"Failed GMV Rate: "
    f"{failed_gmv_rate:.2%}"
)
assert failed_gmv > 0, \
    "Failed GMV cannot be zero."

assert failed_gmv < total_gmv, \
    "Failed GMV cannot exceed total GMV."

print("✓ Failed GMV sanity check passed.")
print("\n" + "=" * 50)
print("DISTRIBUTION & ANOMALY VALIDATION SUMMARY")
print("=" * 50)

print("✓ Overall failure rate reasonable")
print("✓ Bank distribution aligned with design")
print("✓ Device distribution aligned with design")
print("✓ City distribution aligned with design")
print("✓ Transaction amount distribution reasonable")
print("✓ Amount boundary concentration reasonable")
print("✓ All 12 months represented")
print("✓ All 365 calendar days represented")
print("✓ App-version rollout pattern detected")
print("✓ User activity distribution inspected")
print("✓ Bank failure patterns inspected")
print("✓ App-version failure patterns inspected")
print("✓ Failure reason distribution reasonable")
print("✓ Failed GMV relationship valid")

print("=" * 50)
print("Distribution and anomaly validation completed.")
# ============================================================
# FINAL VALIDATION REPORT
# ============================================================

print("\nPreparing final validation report...")

validation_summary = {
    "Total Transactions": f"{len(df):,}",
    "Total Columns": df.shape[1],
    "Unique Transaction IDs": f"{df['transaction_id'].nunique():,}",
    "Unique Active Users": f"{df['user_id'].nunique():,}",
    "Duplicate Transaction IDs": duplicate_transaction_ids,
    "Fully Duplicate Rows": duplicate_rows,
    "Overall Failure Rate": f"{overall_failure_rate:.2%}",
    "Total GMV": f"₹{total_gmv:,.2f}",
    "Failed GMV / GMV at Risk": f"₹{failed_gmv:,.2f}",
    "Failed GMV Rate": f"{failed_gmv_rate:.2%}",
    "Earliest Transaction": str(df["txn_timestamp"].min()),
    "Latest Transaction": str(df["txn_timestamp"].max()),
    "Validation Status": "PASSED"
}
print("\n" + "=" * 60)
print("FINAL DATA VALIDATION REPORT")
print("=" * 60)

for metric, value in validation_summary.items():
    print(f"{metric:<35} {value}")

print("=" * 60)
# ============================================================
# SAVE VALIDATION REPORT
# ============================================================

report_directory = (
    project_root
    / "documentation"
)

report_path = (
    report_directory
    / "data_validation_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as report_file:

    report_file.write(
        "UPI PAYMENT RELIABILITY ANALYSIS\n"
    )

    report_file.write(
        "DATA VALIDATION REPORT\n"
    )

    report_file.write(
        "=" * 60 + "\n\n"
    )

    for metric, value in validation_summary.items():
        report_file.write(
            f"{metric}: {value}\n"
        )

    report_file.write(
        "\nValidation Checks Completed:\n"
    )

    report_file.write(
        "- Schema validation\n"
        "- Mandatory field completeness\n"
        "- Transaction ID uniqueness\n"
        "- Duplicate row validation\n"
        "- Status and failure reason consistency\n"
        "- Amount range validation\n"
        "- Timestamp range validation\n"
        "- Categorical value validation\n"
        "- ID format validation\n"
        "- Distribution sanity checks\n"
        "- Monthly and daily coverage\n"
        "- App-version rollout validation\n"
        "- Failed GMV sanity validation\n"
    )

    report_file.write(
        "\nFinal Result: PASSED\n"
    )

print(
    f"\nValidation report saved to:"
    f"\n{report_path}"
)
