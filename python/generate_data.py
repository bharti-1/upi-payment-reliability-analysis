import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42

NUM_TRANSACTIONS = 1_000_000
NUM_USERS = 100_000

START_DATE = "2025-01-01"
END_DATE = "2025-12-31 23:59:59"

MIN_AMOUNT = 10
MAX_AMOUNT = 50_000

BASE_FAILURE_RATE = 0.05


# Set random seed for reproducibility
np.random.seed(RANDOM_SEED)

# ============================================================
# CATEGORICAL CONFIGURATION
# ============================================================

BANKS = ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB"]
BANK_PROBS = [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]

CITIES = [
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
]

CITY_PROBS = [
    0.15,
    0.15,
    0.14,
    0.11,
    0.10,
    0.09,
    0.08,
    0.07,
    0.06,
    0.05,
]

DEVICE_TYPES = ["Android", "iOS"]
DEVICE_PROBS = [0.80, 0.20]

APP_VERSIONS = ["4.0.0", "4.1.0", "4.2.0", "4.3.0", "5.0.0"]

FAILURE_REASONS = [
    "BANK_SERVER_ERROR",
    "NETWORK_ERROR",
    "INSUFFICIENT_FUNDS",
    "TECHNICAL_ERROR",
    "TIMEOUT",
]
# ============================================================
# CONFIGURATION VALIDATION
# ============================================================

assert np.isclose(sum(BANK_PROBS), 1.0), \
    "Bank probabilities must sum to 1."

assert np.isclose(sum(CITY_PROBS), 1.0), \
    "City probabilities must sum to 1."

assert np.isclose(sum(DEVICE_PROBS), 1.0), \
    "Device probabilities must sum to 1."

print("UPI Synthetic Data Generation")
print("-" * 40)
print(f"Transactions to generate: {NUM_TRANSACTIONS:,}")
print(f"Synthetic users: {NUM_USERS:,}")
print(f"Analysis period: {START_DATE} to {END_DATE}")
print(f"Baseline failure rate: {BASE_FAILURE_RATE:.1%}")

# ============================================================
# GENERATE TRANSACTION IDS
# ============================================================

transaction_ids = np.array([
    f"TXN{i:07d}"
    for i in range(1, NUM_TRANSACTIONS + 1)
])

print("\nTransaction IDs generated.")
print(f"First transaction ID: {transaction_ids[0]}")
print(f"Last transaction ID: {transaction_ids[-1]}")
print(f"Total transaction IDs: {len(transaction_ids):,}")

# ============================================================
# GENERATE USER IDS
# ============================================================

user_population = np.array([
    f"USER{i:06d}"
    for i in range(1, NUM_USERS + 1)
])

print("\nUser population created.")
print(f"First user ID: {user_population[0]}")
print(f"Last user ID: {user_population[-1]}")
print(f"Total synthetic users: {len(user_population):,}")

# Create user activity weights using a lognormal distribution
user_activity_weights = np.random.lognormal(
    mean=0.0,
    sigma=1.0,
    size=NUM_USERS
)

# Convert weights into probabilities
user_activity_probs = (
    user_activity_weights / user_activity_weights.sum()
)

# Assign a user to every transaction
user_ids = np.random.choice(
    user_population,
    size=NUM_TRANSACTIONS,
    p=user_activity_probs
)

print("\nUsers assigned to transactions.")
print(f"Total user assignments: {len(user_ids):,}")
print(f"Unique users appearing in transactions: {len(np.unique(user_ids)):,}")

assert len(transaction_ids) == NUM_TRANSACTIONS
assert len(np.unique(transaction_ids)) == NUM_TRANSACTIONS
assert len(user_ids) == NUM_TRANSACTIONS

print("\nTransaction ID and user assignment validation passed.")

# ============================================================
# GENERATE TRANSACTION TIMESTAMPS
# ============================================================

start_date = pd.Timestamp(START_DATE).normalize()
end_date = pd.Timestamp(END_DATE).normalize()

# Number of calendar days in the analysis period
num_days = (end_date - start_date).days + 1

print("\nGenerating transaction timestamps...")
print(f"Number of days in analysis period: {num_days}")

# Create all calendar dates in the analysis period
date_range = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

# Generate moderate variation in daily transaction activity
daily_weights = np.random.lognormal(
    mean=0.0,
    sigma=0.15,
    size=len(date_range)
)

daily_probs = daily_weights / daily_weights.sum()

# Assign a date to every transaction
transaction_dates = np.random.choice(
    date_range,
    size=NUM_TRANSACTIONS,
    p=daily_probs
)

# Hourly transaction activity weights
hourly_weights = np.array([
    0.20,  # 00:00
    0.15,  # 01:00
    0.10,  # 02:00
    0.08,  # 03:00
    0.08,  # 04:00
    0.12,  # 05:00
    0.25,  # 06:00
    0.50,  # 07:00
    0.80,  # 08:00
    1.00,  # 09:00
    1.10,  # 10:00
    1.15,  # 11:00
    1.20,  # 12:00
    1.15,  # 13:00
    1.10,  # 14:00
    1.10,  # 15:00
    1.15,  # 16:00
    1.25,  # 17:00
    1.40,  # 18:00
    1.50,  # 19:00
    1.45,  # 20:00
    1.25,  # 21:00
    0.90,  # 22:00
    0.50,  # 23:00
])

hourly_probs = hourly_weights / hourly_weights.sum()

transaction_hours = np.random.choice(
    np.arange(24),
    size=NUM_TRANSACTIONS,
    p=hourly_probs
)

transaction_minutes = np.random.randint(
    0,
    60,
    size=NUM_TRANSACTIONS
)

transaction_seconds = np.random.randint(
    0,
    60,
    size=NUM_TRANSACTIONS
)

transaction_dates = pd.to_datetime(transaction_dates)

txn_timestamps = (
    transaction_dates
    + pd.to_timedelta(transaction_hours, unit="h")
    + pd.to_timedelta(transaction_minutes, unit="m")
    + pd.to_timedelta(transaction_seconds, unit="s")
)

print("\nTransaction timestamps generated.")
print(f"Total timestamps: {len(txn_timestamps):,}")
print(f"Earliest timestamp: {txn_timestamps.min()}")
print(f"Latest timestamp: {txn_timestamps.max()}")

assert len(txn_timestamps) == NUM_TRANSACTIONS

assert txn_timestamps.min() >= pd.Timestamp(START_DATE)

assert txn_timestamps.max() <= pd.Timestamp(END_DATE)

print("Timestamp validation passed.")

# ============================================================
# GENERATE TRANSACTION AMOUNTS
# ============================================================

print("\nGenerating transaction amounts...")

# Generate right-skewed transaction amounts using a lognormal distribution
transaction_amounts = np.random.lognormal(
    mean=5.0,
    sigma=1.0,
    size=NUM_TRANSACTIONS
)

# Keep amounts within the documented transaction range
transaction_amounts = np.clip(
    transaction_amounts,
    MIN_AMOUNT,
    MAX_AMOUNT
)

# Round amounts to two decimal places
transaction_amounts = np.round(
    transaction_amounts,
    2
)

print("Transaction amounts generated.")

amount_series = pd.Series(transaction_amounts)

print("\nTransaction Amount Statistics:")
print(f"Minimum: ₹{amount_series.min():,.2f}")
print(f"Maximum: ₹{amount_series.max():,.2f}")
print(f"Mean: ₹{amount_series.mean():,.2f}")
print(f"Median: ₹{amount_series.median():,.2f}")

print(f"P90: ₹{amount_series.quantile(0.90):,.2f}")
print(f"P95: ₹{amount_series.quantile(0.95):,.2f}")
print(f"P99: ₹{amount_series.quantile(0.99):,.2f}")

# ============================================================
# VALIDATE TRANSACTION AMOUNTS
# ============================================================

assert len(transaction_amounts) == NUM_TRANSACTIONS

assert np.all(transaction_amounts >= MIN_AMOUNT)

assert np.all(transaction_amounts <= MAX_AMOUNT)

assert not np.isnan(transaction_amounts).any()

print("Transaction amount validation passed.")

amount_bands = pd.cut(
    transaction_amounts,
    bins=[0, 100, 500, 1000, 5000, 10000, 50000],
    labels=[
        "₹0-100",
        "₹101-500",
        "₹501-1,000",
        "₹1,001-5,000",
        "₹5,001-10,000",
        "₹10,001-50,000"
    ],
    include_lowest=True
)

amount_band_distribution = (
    pd.Series(amount_bands)
    .value_counts(sort=False)
)

print("\nTransaction Amount Band Distribution:")

for band, count in amount_band_distribution.items():
    percentage = count / NUM_TRANSACTIONS * 100

    print(
        f"{band}: "
        f"{count:,} transactions "
        f"({percentage:.2f}%)"
    )

# ============================================================
# GENERATE CATEGORICAL TRANSACTION DIMENSIONS
# ============================================================

print("\nGenerating categorical transaction dimensions...")


# ------------------------------------------------------------
# BANK
# ------------------------------------------------------------

bank_names = np.random.choice(
    BANKS,
    size=NUM_TRANSACTIONS,
    p=BANK_PROBS
)


# ------------------------------------------------------------
# CITY
# ------------------------------------------------------------

cities = np.random.choice(
    CITIES,
    size=NUM_TRANSACTIONS,
    p=CITY_PROBS
)


# ------------------------------------------------------------
# DEVICE TYPE
# ------------------------------------------------------------

device_types = np.random.choice(
    DEVICE_TYPES,
    size=NUM_TRANSACTIONS,
    p=DEVICE_PROBS
)

print("Categorical transaction dimensions generated.")

# ============================================================
# VALIDATE CATEGORICAL DIMENSIONS
# ============================================================

assert len(bank_names) == NUM_TRANSACTIONS
assert len(cities) == NUM_TRANSACTIONS
assert len(device_types) == NUM_TRANSACTIONS

print("Categorical dimension length validation passed.")

assert set(np.unique(bank_names)).issubset(set(BANKS))

assert set(np.unique(cities)).issubset(set(CITIES))

assert set(np.unique(device_types)).issubset(set(DEVICE_TYPES))

print("Categorical value validation passed.")

def print_distribution(values, title):
    counts = pd.Series(values).value_counts()

    percentages = (
        pd.Series(values)
        .value_counts(normalize=True)
        .mul(100)
    )

    distribution = pd.DataFrame({
        "Count": counts,
        "Percentage": percentages
    })

    print(f"\n{title}")
    print(distribution.round(2))

print_distribution(
    bank_names,
    "Bank Distribution"
)

print_distribution(
    cities,
    "City Distribution"
)

print_distribution(
    device_types,
    "Device Type Distribution"
)

def validate_distribution(
    values,
    categories,
    expected_probs,
    tolerance=0.01
):
    observed_probs = (
        pd.Series(values)
        .value_counts(normalize=True)
        .reindex(categories)
        .fillna(0)
        .values
    )

    differences = np.abs(
        observed_probs - np.array(expected_probs)
    )

    assert np.all(differences <= tolerance), \
        "Observed distribution differs too much from expected distribution."

validate_distribution(
    bank_names,
    BANKS,
    BANK_PROBS
)

validate_distribution(
    cities,
    CITIES,
    CITY_PROBS
)

validate_distribution(
    device_types,
    DEVICE_TYPES,
    DEVICE_PROBS
)

print("Categorical distribution validation passed.")

# ============================================================
# GENERATE TIME-DEPENDENT APP VERSIONS
# ============================================================

print("\nGenerating app versions based on transaction date...")

app_versions = np.empty(
    NUM_TRANSACTIONS,
    dtype=object
)

transaction_months = pd.DatetimeIndex(txn_timestamps).month

# App-version probability distributions by period

APP_PROBS_Q1 = [0.25, 0.30, 0.30, 0.15, 0.00]

APP_PROBS_Q2 = [0.15, 0.25, 0.30, 0.25, 0.05]

APP_PROBS_Q3 = [0.08, 0.15, 0.25, 0.27, 0.25]

APP_PROBS_Q4 = [0.03, 0.07, 0.15, 0.25, 0.50]

assert np.isclose(sum(APP_PROBS_Q1), 1.0)
assert np.isclose(sum(APP_PROBS_Q2), 1.0)
assert np.isclose(sum(APP_PROBS_Q3), 1.0)
assert np.isclose(sum(APP_PROBS_Q4), 1.0)

print("App-version probability configuration validated.")

q1_mask = transaction_months <= 3

q2_mask = (
    (transaction_months >= 4)
    & (transaction_months <= 6)
)

q3_mask = (
    (transaction_months >= 7)
    & (transaction_months <= 9)
)

q4_mask = transaction_months >= 10

app_versions[q1_mask] = np.random.choice(
    APP_VERSIONS,
    size=q1_mask.sum(),
    p=APP_PROBS_Q1
)

app_versions[q2_mask] = np.random.choice(
    APP_VERSIONS,
    size=q2_mask.sum(),
    p=APP_PROBS_Q2
)

app_versions[q3_mask] = np.random.choice(
    APP_VERSIONS,
    size=q3_mask.sum(),
    p=APP_PROBS_Q3
)

app_versions[q4_mask] = np.random.choice(
    APP_VERSIONS,
    size=q4_mask.sum(),
    p=APP_PROBS_Q4
)

print("Time-dependent app versions generated.")

assert len(app_versions) == NUM_TRANSACTIONS

assert not pd.Series(app_versions).isna().any()

assert set(np.unique(app_versions)).issubset(
    set(APP_VERSIONS)
)

print("App-version validation passed.")

app_validation_df = pd.DataFrame({
    "month": transaction_months,
    "app_version": app_versions
})

app_month_distribution = pd.crosstab(
    app_validation_df["month"],
    app_validation_df["app_version"],
    normalize="index"
) * 100

print("\nApp Version Distribution by Month (%):")
print(app_month_distribution.round(2))

# ============================================================
# FAILURE PROBABILITY ENGINE
# ============================================================

print("\nBuilding failure probability engine...")

# Every transaction starts with the baseline failure probability
failure_probs = np.full(
    NUM_TRANSACTIONS,
    BASE_FAILURE_RATE,
    dtype=float
)

print(
    f"Initial baseline failure probability: "
    f"{failure_probs.mean():.2%}"
)

# ------------------------------------------------------------
# BANK EFFECT
# ------------------------------------------------------------

failure_probs += np.where(
    bank_names == "PNB",
    0.010,
    0.0
)

failure_probs += np.where(
    bank_names == "SBI",
    0.006,
    0.0
)

failure_probs += np.where(
    bank_names == "HDFC",
    -0.003,
    0.0
)

# ------------------------------------------------------------
# APP VERSION EFFECT
# ------------------------------------------------------------

failure_probs += np.where(
    app_versions == "4.0.0",
    0.012,
    0.0
)

failure_probs += np.where(
    app_versions == "4.1.0",
    0.005,
    0.0
)

failure_probs += np.where(
    app_versions == "5.0.0",
    -0.004,
    0.0
)

# ------------------------------------------------------------
# APP VERSION + DEVICE INTERACTION
# ------------------------------------------------------------

app_device_risk = (
    (app_versions == "4.1.0")
    & (device_types == "Android")
)

failure_probs += np.where(
    app_device_risk,
    0.008,
    0.0
)

# ------------------------------------------------------------
# TIME-OF-DAY EFFECT
# ------------------------------------------------------------

late_night_risk = (
    (transaction_hours >= 0)
    & (transaction_hours <= 4)
)

failure_probs += np.where(
    late_night_risk,
    0.010,
    0.0
)

# ------------------------------------------------------------
# HIGH-VALUE TRANSACTION EFFECT
# ------------------------------------------------------------

high_value_risk = transaction_amounts >= 5000

failure_probs += np.where(
    high_value_risk,
    0.006,
    0.0
)

# ------------------------------------------------------------
# TEMPORARY FAILURE INCIDENT
# ------------------------------------------------------------

incident_start = pd.Timestamp("2025-08-15 18:00:00")
incident_end = pd.Timestamp("2025-08-16 06:00:00")

incident_mask = (
    (txn_timestamps >= incident_start)
    & (txn_timestamps <= incident_end)
)

failure_probs += np.where(
    incident_mask,
    0.040,
    0.0
)

# ------------------------------------------------------------
# CONSTRAIN FINAL FAILURE PROBABILITY
# ------------------------------------------------------------

failure_probs = np.clip(
    failure_probs,
    0.01,
    0.25
)

failure_prob_series = pd.Series(failure_probs)

print("\nFailure Probability Statistics:")
print(f"Minimum: {failure_prob_series.min():.2%}")
print(f"Maximum: {failure_prob_series.max():.2%}")
print(f"Mean: {failure_prob_series.mean():.2%}")
print(f"Median: {failure_prob_series.median():.2%}")
print(f"P95: {failure_prob_series.quantile(0.95):.2%}")
print(f"P99: {failure_prob_series.quantile(0.99):.2%}")

assert len(failure_probs) == NUM_TRANSACTIONS
assert np.all(failure_probs >= 0)
assert np.all(failure_probs <= 1)
assert not np.isnan(failure_probs).any()

print("Failure probability validation passed.")

# ============================================================
# GENERATE TRANSACTION STATUS
# ============================================================

print("\nGenerating transaction status...")

random_values = np.random.random(
    NUM_TRANSACTIONS
)

failed_mask = random_values < failure_probs

statuses = np.where(
    failed_mask,
    "FAILED",
    "SUCCESS"
)

total_failed = failed_mask.sum()
total_success = NUM_TRANSACTIONS - total_failed

observed_failure_rate = (
    total_failed / NUM_TRANSACTIONS
)

print("\nTransaction Status Summary:")
print(f"Successful Transactions: {total_success:,}")
print(f"Failed Transactions: {total_failed:,}")
print(f"Observed Failure Rate: {observed_failure_rate:.2%}")

expected_failure_rate = failure_probs.mean()

print(
    f"Mean Expected Failure Probability: "
    f"{expected_failure_rate:.2%}"
)

print(
    f"Observed Failure Rate: "
    f"{observed_failure_rate:.2%}"
)

# ============================================================
# GENERATE FAILURE REASONS
# ============================================================

print("\nGenerating failure reasons...")

failure_reasons = np.full(
    NUM_TRANSACTIONS,
    None,
    dtype=object
)

BASE_REASON_PROBS = [
    0.20,  # BANK_SERVER_ERROR
    0.20,  # NETWORK_ERROR
    0.25,  # INSUFFICIENT_FUNDS
    0.20,  # TECHNICAL_ERROR
    0.15,  # TIMEOUT
]

assert np.isclose(
    sum(BASE_REASON_PROBS),
    1.0
)

failure_reasons[failed_mask] = np.random.choice(
    FAILURE_REASONS,
    size=total_failed,
    p=BASE_REASON_PROBS
)

incident_failed_mask = (
    incident_mask
    & failed_mask
)

incident_failed_count = (
    incident_failed_mask.sum()
)

INCIDENT_REASON_PROBS = [
    0.10,  # BANK_SERVER_ERROR
    0.15,  # NETWORK_ERROR
    0.10,  # INSUFFICIENT_FUNDS
    0.15,  # TECHNICAL_ERROR
    0.50,  # TIMEOUT
]

assert np.isclose(
    sum(INCIDENT_REASON_PROBS),
    1.0
)

failure_reasons[incident_failed_mask] = np.random.choice(
    FAILURE_REASONS,
    size=incident_failed_count,
    p=INCIDENT_REASON_PROBS
)

old_app_failed_mask = (
    (app_versions == "4.0.0")
    & failed_mask
    & (~incident_mask)
)

old_app_failed_count = (
    old_app_failed_mask.sum()
)

OLD_APP_REASON_PROBS = [
    0.15,  # BANK_SERVER_ERROR
    0.15,  # NETWORK_ERROR
    0.20,  # INSUFFICIENT_FUNDS
    0.40,  # TECHNICAL_ERROR
    0.10,  # TIMEOUT
]

assert np.isclose(
    sum(OLD_APP_REASON_PROBS),
    1.0
)

failure_reasons[old_app_failed_mask] = np.random.choice(
    FAILURE_REASONS,
    size=old_app_failed_count,
    p=OLD_APP_REASON_PROBS
)

# ============================================================
# VALIDATE STATUS AND FAILURE REASONS
# ============================================================

assert len(statuses) == NUM_TRANSACTIONS
assert len(failure_reasons) == NUM_TRANSACTIONS

assert set(np.unique(statuses)).issubset(
    {"SUCCESS", "FAILED"}
)

success_mask = statuses == "SUCCESS"

assert pd.isna(
    failure_reasons[success_mask]
).all()

assert pd.notna(
    failure_reasons[failed_mask]
).all()

print(
    "Transaction status and failure reason "
    "validation passed."
)

failure_reason_distribution = (
    pd.Series(failure_reasons[failed_mask])
    .value_counts()
)

failure_reason_percentage = (
    pd.Series(failure_reasons[failed_mask])
    .value_counts(normalize=True)
    .mul(100)
)

failure_reason_summary = pd.DataFrame({
    "Count": failure_reason_distribution,
    "Percentage": failure_reason_percentage
})

print("\nFailure Reason Distribution:")
print(
    failure_reason_summary.round(2)
)

# ============================================================
# BUILD FINAL DATAFRAME
# ============================================================

print("\nBuilding final transaction dataset...")

df = pd.DataFrame({
    "transaction_id": transaction_ids,
    "user_id": user_ids,
    "txn_timestamp": txn_timestamps,
    "amount": transaction_amounts,
    "status": statuses,
    "failure_reason": failure_reasons,
    "bank_name": bank_names,
    "app_version": app_versions,
    "device_type": device_types,
    "city": cities
})

print("Final transaction dataset created.")

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Info:")
df.info()

# ============================================================
# FINAL DATA QUALITY VALIDATION
# ============================================================

print("\nRunning final data quality checks...")

assert len(df) == NUM_TRANSACTIONS, \
    "Incorrect number of rows."

assert df.shape[1] == 10, \
    "Incorrect number of columns."

print("✓ Dataset shape validation passed.")

assert df["transaction_id"].notna().all(), \
    "Null transaction IDs found."

assert df["transaction_id"].is_unique, \
    "Duplicate transaction IDs found."

print("✓ Transaction ID validation passed.")

assert df["user_id"].notna().all(), \
    "Null user IDs found."

assert df["user_id"].nunique() <= NUM_USERS, \
    "Unexpected number of users."

print("✓ User ID validation passed.")

assert df["txn_timestamp"].notna().all(), \
    "Null timestamps found."

assert df["txn_timestamp"].min() >= pd.Timestamp(START_DATE), \
    "Timestamp before analysis period found."

assert df["txn_timestamp"].max() <= pd.Timestamp(END_DATE), \
    "Timestamp after analysis period found."

print("✓ Timestamp validation passed.")

assert df["amount"].notna().all(), \
    "Null transaction amounts found."

assert (df["amount"] >= MIN_AMOUNT).all(), \
    "Transaction amount below minimum found."

assert (df["amount"] <= MAX_AMOUNT).all(), \
    "Transaction amount above maximum found."

print("✓ Transaction amount validation passed.")

assert df["status"].notna().all(), \
    "Null transaction statuses found."

assert set(df["status"].unique()).issubset(
    {"SUCCESS", "FAILED"}
), "Unexpected transaction status found."

print("✓ Transaction status validation passed.")

successful_transactions = (
    df["status"] == "SUCCESS"
)

failed_transactions = (
    df["status"] == "FAILED"
)

assert df.loc[
    successful_transactions,
    "failure_reason"
].isna().all(), \
    "Successful transactions contain failure reasons."

assert df.loc[
    failed_transactions,
    "failure_reason"
].notna().all(), \
    "Failed transactions contain null failure reasons."

print("✓ Failure reason validation passed.")

observed_failure_reasons = set(
    df.loc[
        failed_transactions,
        "failure_reason"
    ].unique()
)

assert observed_failure_reasons.issubset(
    set(FAILURE_REASONS)
), "Unexpected failure reason found."

print("✓ Failure reason category validation passed.")

assert set(df["bank_name"].unique()).issubset(
    set(BANKS)
)

assert set(df["city"].unique()).issubset(
    set(CITIES)
)

assert set(df["device_type"].unique()).issubset(
    set(DEVICE_TYPES)
)

assert set(df["app_version"].unique()).issubset(
    set(APP_VERSIONS)
)

print("✓ Categorical value validation passed.")

# ============================================================
# HEADLINE KPI SUMMARY
# ============================================================

total_transactions = len(df)

successful_count = (
    df["status"] == "SUCCESS"
).sum()

failed_count = (
    df["status"] == "FAILED"
).sum()

success_rate = (
    successful_count
    / total_transactions
)

failure_rate = (
    failed_count
    / total_transactions
)

total_gmv = df["amount"].sum()

successful_gmv = df.loc[
    df["status"] == "SUCCESS",
    "amount"
].sum()

failed_gmv = df.loc[
    df["status"] == "FAILED",
    "amount"
].sum()

failed_gmv_rate = (
    failed_gmv
    / total_gmv
)

average_transaction_value = (
    df["amount"].mean()
)

print("\n" + "=" * 50)
print("DATASET KPI SUMMARY")
print("=" * 50)

print(
    f"Total Transactions: "
    f"{total_transactions:,}"
)

print(
    f"Successful Transactions: "
    f"{successful_count:,}"
)

print(
    f"Failed Transactions: "
    f"{failed_count:,}"
)

print(
    f"Success Rate: "
    f"{success_rate:.2%}"
)

print(
    f"Failure Rate: "
    f"{failure_rate:.2%}"
)

print(
    f"Total GMV: "
    f"₹{total_gmv:,.2f}"
)

print(
    f"Successful GMV: "
    f"₹{successful_gmv:,.2f}"
)

print(
    f"Failed GMV / GMV at Risk: "
    f"₹{failed_gmv:,.2f}"
)

print(
    f"Failed GMV Rate: "
    f"{failed_gmv_rate:.2%}"
)

print(
    f"Average Transaction Value: "
    f"₹{average_transaction_value:,.2f}"
)

print("=" * 50)

bank_failure_check = (
    df.groupby("bank_name")["status"]
    .apply(
        lambda x: (x == "FAILED").mean()
    )
    .sort_values(ascending=False)
)

print("\nFailure Rate by Bank:")
print(
    (bank_failure_check * 100)
    .round(2)
    .astype(str)
    + "%"
)

app_failure_check = (
    df.groupby("app_version")["status"]
    .apply(
        lambda x: (x == "FAILED").mean()
    )
    .sort_values(ascending=False)
)

print("\nFailure Rate by App Version:")
print(
    (app_failure_check * 100)
    .round(2)
    .astype(str)
    + "%"
)

hour_failure_check = (
    df.assign(
        hour=df["txn_timestamp"].dt.hour
    )
    .groupby("hour")["status"]
    .apply(
        lambda x: (x == "FAILED").mean()
    )
)

print("\nFailure Rate by Hour:")
print(
    (hour_failure_check * 100)
    .round(2)
    .astype(str)
    + "%"
)

print("\nAll final data quality checks passed.")

# ============================================================
# EXPORT DATASET
# ============================================================

print("\nExporting dataset...")

project_root = Path(__file__).resolve().parent.parent

data_directory = (
    project_root / "data"
)

data_directory.mkdir(
    parents=True,
    exist_ok=True
)

output_path = (
    data_directory
    / "upi_transactions.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"Dataset exported successfully to:"
    f"\n{output_path}"
)

assert output_path.exists(), \
    "CSV export failed."

print(
    f"Exported file size: "
    f"{output_path.stat().st_size / (1024 ** 2):.2f} MB"
)

print("\nData generation completed successfully.")

