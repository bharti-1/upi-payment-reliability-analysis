# Data Generation Plan

## 1. Purpose

This document defines the design and generation strategy for the synthetic UPI
transaction dataset used in the UPI Payment Reliability, Failure Root-Cause &
GMV Impact Analysis project.

The dataset will be generated using Python and will simulate transaction-level
UPI payment activity across multiple banks, cities, application versions,
device types, transaction amounts, and time periods.

The purpose of generating synthetic data is to create a reproducible dataset
that supports realistic analytical scenarios while avoiding the use of
confidential or personally identifiable financial data.

The generated dataset will contain intentionally simulated transaction and
failure patterns so that SQL, Python, and Power BI can be used to investigate
payment reliability, identify high-impact segments, and quantify Failed GMV.

All patterns and relationships introduced during data generation are simulated
for portfolio and analytical purposes and should not be interpreted as
representing the performance of any real bank, payment platform, application,
or customer population.

## 2. Dataset Scope

The synthetic dataset will contain approximately 1,000,000 transaction-level
records.

### Analysis Period

January 1, 2025 to December 31, 2025.

### Granularity

One row represents one UPI payment attempt.

### Currency

Indian Rupees (INR).

### Primary Transaction Status

Each transaction will have one of two statuses:

- SUCCESS
- FAILED

### Planned Dataset Size

Approximately 1,000,000 transactions.

The dataset size is intentionally large enough to support:

- SQL aggregation and window-function analysis.
- Time-based transaction analysis.
- Multi-dimensional segmentation.
- Python exploratory and statistical analysis.
- Power BI dashboard development.
- Performance considerations when working with a relatively large analytical
  dataset.

### Data Source

The dataset will be generated entirely using Python.

No real customer, bank, merchant, or transaction-level financial data will be
used.

## 3. Dataset Schema

The dataset will use transaction-level granularity, where each row represents
one UPI payment attempt.

The initial dataset will contain the following columns:

| Column | Data Type | Description |
|---|---|---|
| transaction_id | String | Unique identifier for each payment attempt |
| user_id | String | Synthetic identifier representing the user initiating the transaction |
| txn_timestamp | Datetime | Date and time when the payment attempt occurred |
| amount | Decimal | Transaction amount in INR |
| status | String | Final status of the payment attempt: SUCCESS or FAILED |
| failure_reason | String / Null | Simulated reason for failure; populated only for failed transactions |
| bank_name | String | Simulated bank associated with the transaction |
| app_version | String | Application version used during the transaction |
| device_type | String | Device operating system/category used for the transaction |
| city | String | Simulated city associated with the transaction |

### 3.1 Primary Key

`transaction_id` will act as the unique identifier for each transaction record.

Each transaction ID must occur exactly once in the dataset.

### 3.2 Transaction Granularity

Each row represents one payment attempt rather than one unique customer or
payment journey.

A user may therefore appear in multiple transaction records.

The dataset does not currently link an initial failed transaction to a later
retry attempt.

### 3.3 Failure Reason Logic

`failure_reason` will depend on transaction status.

For successful transactions:

status = SUCCESS  
failure_reason = NULL

For failed transactions:

status = FAILED  
failure_reason = one of the defined simulated failure categories

This relationship will later be included in data-quality validation.

### 3.4 Derived Analytical Fields

The following fields do not need to be stored as part of the original generated
transaction data because they can be derived from existing columns during
analysis:

- transaction_date
- year
- month
- month_name
- day_of_week
- hour
- time_of_day
- transaction_amount_band
- success_flag
- failure_flag

These fields may be created in SQL, Python, or Power BI depending on the
analytical requirement.

## 4. Column Definitions and Allowed Values

### 4.1 transaction_id

**Purpose:**  
Unique identifier for each payment attempt.

**Format:**  
TXN followed by a zero-padded sequential number.

**Example:**  
TXN0000001

**Rules:**

- Must be unique.
- Must not contain null values.
- One transaction ID represents one payment attempt.

---

### 4.2 user_id

**Purpose:**  
Synthetic identifier representing the user initiating the payment.

**Format:**  
USER followed by a zero-padded number.

**Example:**  
USER000123

**Planned User Population:**  
Approximately 100,000 unique synthetic users.

**Rules:**

- A user may perform multiple transactions.
- User IDs are completely synthetic.
- Multiple transactions from the same user should not automatically be
  interpreted as retries of the same payment.

---

### 4.3 txn_timestamp

**Purpose:**  
Records when the transaction attempt occurred.

**Data Type:**  
Datetime

**Allowed Range:**  
2025-01-01 00:00:00 to 2025-12-31 23:59:59

**Rules:**

- Every transaction must contain a valid timestamp.
- Timestamps will support monthly, daily, weekday, and hourly analysis.
- Transaction activity will not necessarily be distributed uniformly across
  all hours and days.

---

### 4.4 amount

**Purpose:**  
Represents the monetary value of the payment attempt in INR.

**Data Type:**  
Decimal

**Planned Range:**  
₹10 to ₹50,000

**Rules:**

- Amount must be greater than zero.
- Values will be rounded to two decimal places.
- Transaction amounts will follow a right-skewed distribution rather than a
  uniform distribution.
- Most transactions will be relatively low or medium value, while high-value
  transactions will occur less frequently.

---

### 4.5 status

**Purpose:**  
Represents whether the payment attempt was successfully completed.

**Allowed Values:**

- SUCCESS
- FAILED

**Rules:**

- Every transaction must have exactly one status.
- Failure probability will be influenced by selected simulated transaction
  characteristics rather than being completely random.

---

### 4.6 failure_reason

**Purpose:**  
Provides a simulated reason for an unsuccessful payment attempt.

**Allowed Failure Categories:**

- BANK_SERVER_ERROR
- NETWORK_ERROR
- INSUFFICIENT_FUNDS
- TECHNICAL_ERROR
- TIMEOUT

**Rules:**

- SUCCESS transactions must have a NULL failure reason.
- FAILED transactions must have a populated failure reason.
- Failure reasons are simplified simulated categories created for analytical
  purposes.

---

### 4.7 bank_name

**Purpose:**  
Represents the bank associated with the simulated transaction.

**Allowed Values:**

- SBI
- HDFC
- ICICI
- Axis
- Kotak
- PNB

**Rules:**

- Every transaction must be associated with one bank.
- Transaction volume will vary across banks.
- Any simulated differences in failure performance do not represent the actual
  performance of these banks.

---

### 4.8 app_version

**Purpose:**  
Represents the application version used for the payment attempt.

**Allowed Values:**

- 4.0.0
- 4.1.0
- 4.2.0
- 4.3.0
- 5.0.0

**Rules:**

- Application-version adoption will vary across the dataset.
- Older versions may remain in use while newer versions are introduced.
- Selected versions may contain intentionally simulated reliability patterns.

---

### 4.9 device_type

**Purpose:**  
Represents the device platform used to initiate the transaction.

**Allowed Values:**

- Android
- iOS

**Rules:**

- Every transaction must have one device type.
- Device distribution will not necessarily be equal.
- Device type may be used together with app version during reliability
  investigation.

---

### 4.10 city

**Purpose:**  
Represents the simulated city associated with the transaction.

**Allowed Values:**

- Delhi
- Mumbai
- Bengaluru
- Hyderabad
- Chennai
- Kolkata
- Pune
- Ahmedabad
- Jaipur
- Lucknow

**Rules:**

- Every transaction must have one city.
- Transaction volume will vary across cities.
- Geographic failure patterns, if introduced, will be simulated and must not be
  interpreted as real-world city-level UPI performance.

## 5. Data Distributions

The synthetic dataset will use controlled probability distributions rather than
uniform random generation.

The purpose is to create transaction behavior that is suitable for realistic
analytical investigation while remaining fully synthetic.

### 5.1 User Activity Distribution

The dataset will contain approximately 100,000 unique synthetic users across
approximately 1,000,000 transactions.

Transaction activity will not be distributed equally across all users.

Some users will perform relatively few transactions, while a smaller group of
users will perform transactions more frequently.

This creates a more realistic repeated-user pattern compared with assigning the
same number of transactions to every user.

---

### 5.2 Transaction Amount Distribution

Transaction amounts will range approximately from ₹10 to ₹50,000.

The amount distribution will be right-skewed.

Expected characteristics:

- Low-value transactions will occur most frequently.
- Medium-value transactions will occur regularly.
- High-value transactions will be less common.
- Extremely high-value transactions will represent a relatively small portion
  of transaction volume.

The exact distribution will be finalized during Python implementation and
validated before the dataset is used for analysis.

---

### 5.3 Bank Transaction Distribution

Transaction volume will vary across banks.

Planned approximate distribution:

| Bank | Transaction Share |
|---|---:|
| SBI | 25% |
| HDFC | 20% |
| ICICI | 18% |
| Axis | 15% |
| Kotak | 12% |
| PNB | 10% |

These percentages represent simulated transaction volume only and do not
represent real UPI market share.

---

### 5.4 Device Distribution

Planned approximate device distribution:

| Device Type | Transaction Share |
|---|---:|
| Android | 80% |
| iOS | 20% |

The distribution is intentionally unequal to support volume-aware comparison
between device segments.

These proportions are synthetic assumptions for the project and are not
intended to represent actual device market share.

---

### 5.5 City Distribution

Transaction volume will vary across cities rather than being equally
distributed.

Planned approximate distribution:

| City | Transaction Share |
|---|---:|
| Delhi | 15% |
| Mumbai | 15% |
| Bengaluru | 14% |
| Hyderabad | 11% |
| Chennai | 10% |
| Kolkata | 9% |
| Pune | 8% |
| Ahmedabad | 7% |
| Jaipur | 6% |
| Lucknow | 5% |

These values are synthetic and are used only to create variation in transaction
volume for analytical purposes.

---

### 5.6 Application Version Distribution

Application-version adoption will vary across transactions.

Planned overall distribution:

| App Version | Transaction Share |
|---|---:|
| 4.0.0 | 8% |
| 4.1.0 | 12% |
| 4.2.0 | 20% |
| 4.3.0 | 25% |
| 5.0.0 | 35% |

Newer versions will generally represent a larger portion of transaction volume.

During implementation, app-version availability may also be linked to time so
that newer versions become more common later in the year rather than appearing
with exactly the same probability throughout the entire analysis period.

---

### 5.7 Time Distribution

Transactions will occur throughout the full analysis period from January 1,
2025 through December 31, 2025.

Transaction volume will not be distributed uniformly across every hour.

Expected daily activity pattern:

- Very low transaction activity during late-night and early-morning hours.
- Increasing activity during morning hours.
- High transaction activity during daytime and evening periods.
- Reduced activity again during late-night hours.

Weekday and monthly transaction volumes may also contain moderate variation to
support time-based analysis.

---

### 5.8 Baseline Failure Rate

The dataset will be designed around an approximate overall baseline failure
rate of 5%.

The final observed failure rate may differ slightly because transaction-level
failure probability will later be adjusted using simulated risk factors.

The baseline failure probability acts as the starting point before applying
additional simulated effects associated with selected transaction dimensions.

The final overall failure rate will be validated after dataset generation.

## 6. Simulated Failure Patterns

Transaction failures will not be generated using a single fixed random failure
rate.

Each transaction will begin with a baseline failure probability of approximately
5%. This probability will then be adjusted using selected simulated risk factors.

The purpose of these adjustments is to create meaningful analytical patterns
that can later be investigated using SQL and Python.

All patterns described below are synthetic and do not represent actual UPI,
bank, device, application, or geographic performance.

### 6.1 Baseline Failure Probability

Each transaction will begin with an approximate baseline failure probability:

Baseline Failure Probability = 5%

Individual transaction probabilities may then increase or decrease depending on
the characteristics of the transaction.

The final probability will be constrained to a reasonable range before the
transaction status is generated.

---

### 6.2 Bank-Level Reliability Pattern

Selected banks will have modest differences in simulated failure probability.

The purpose is to create variation in bank-level reliability without making one
bank unrealistically responsible for all failures.

The bank effect will be relatively small so that bank-level performance must be
evaluated together with transaction volume, failure contribution, and other
dimensions.

---

### 6.3 Application-Version Pattern

Selected application versions will have different simulated reliability
characteristics.

An older application version may receive a moderately elevated failure
probability.

A newer version may have a slightly lower failure probability.

Application-version adoption will also change over time, creating an opportunity
to analyze the relationship between version, transaction period, and failure
performance.

---

### 6.4 Device and Application Interaction

Device type alone will not necessarily create a large reliability difference.

However, a selected application-version and device-type combination may receive
an additional failure probability adjustment.

This creates an interaction effect where the combination of two dimensions may
be more informative than analyzing either dimension independently.

Example analytical question:

Does an application version show elevated failure rates across all devices, or
is the pattern concentrated within one device type?

---

### 6.5 Time-of-Day Pattern

Transactions occurring during selected late-night or early-morning periods may
have a moderately elevated failure probability.

This pattern is intended to simulate time-dependent operational or technical
variation.

The effect will remain moderate so that time of day does not dominate all other
failure patterns.

---

### 6.6 High-Value Transaction Pattern

Higher-value transactions may receive a small increase in failure probability.

This will allow the analysis to compare:

- Failure Rate
- Failed GMV
- Failed GMV Rate
- Transaction amount bands

The effect will be intentionally limited so that high transaction value is not
treated as a direct cause of failure.

---

### 6.7 Temporary Failure Spike

A short period during the year will contain an intentionally elevated failure
probability.

This simulated event will create a temporary reliability anomaly that should be
detectable through daily or hourly trend analysis.

The spike will affect only a limited period rather than the full dataset.

This supports investigation of questions such as:

- When did the failure spike occur?
- Which transaction segments were most affected?
- Which failure reasons increased during the period?
- Did the spike materially affect Failed GMV?

---

### 6.8 Failure Reason Assignment

Failure reasons will be assigned only after a transaction has been classified
as FAILED.

The base failure categories are:

- BANK_SERVER_ERROR
- NETWORK_ERROR
- INSUFFICIENT_FUNDS
- TECHNICAL_ERROR
- TIMEOUT

Failure reasons will not necessarily be distributed equally.

Their probabilities may also depend on transaction characteristics.

For example:

- BANK_SERVER_ERROR may be more common within selected bank-related failure
  patterns.
- NETWORK_ERROR may be more common during selected time periods or device
  combinations.
- TECHNICAL_ERROR may be more common for selected application versions.
- TIMEOUT may increase during the temporary failure spike.
- INSUFFICIENT_FUNDS may occur across multiple transaction segments.

These relationships are simulated analytical patterns and do not represent
actual payment-system behavior.

---

### 6.9 Multi-Dimensional Effects

Some failure patterns will result from combinations of dimensions rather than
from one variable alone.

Potential interactions include:

- Bank + time of day
- App version + device type
- Bank + app version
- Transaction amount + failure reason
- Temporary failure period + failure reason

The number and strength of these interactions will be limited to prevent the
dataset from becoming artificially complex.

---

### 6.10 Noise and Random Variation

Not every failed transaction will be explained by one of the intentionally
simulated patterns.

Random variation will remain in the dataset.

This prevents the analysis from becoming completely deterministic and ensures
that analytical findings are based on patterns and probabilities rather than
perfect rules.

The generated dataset should therefore contain both:

- Detectable simulated signals
- Natural random variation

## 7. Data Generation Logic and Execution Flow

The synthetic dataset will be generated using Python with a structured,
reproducible pipeline.

The generation process will separate normal transaction characteristics from
failure-risk logic so that the simulated patterns remain understandable and
maintainable.

### 7.1 Initialize Generation Parameters

The Python generation script will first define the main configuration values,
including:

- Number of transactions
- Number of synthetic users
- Analysis start date
- Analysis end date
- Random seed
- Allowed categorical values
- Category probability distributions
- Baseline failure probability
- Simulated failure-risk adjustments

These parameters will be defined clearly rather than scattered throughout the
generation code.

---

### 7.2 Generate Transaction IDs

A unique transaction ID will be created for every payment attempt.

Example format:

TXN0000001  
TXN0000002  
TXN0000003

The number of unique transaction IDs must equal the total number of generated
records.

---

### 7.3 Assign Synthetic Users

Each transaction will be assigned a synthetic user ID from the planned user
population.

User activity will not be perfectly uniform.

Some users will appear more frequently than others to create repeated-user
behavior within the dataset.

---

### 7.4 Generate Transaction Timestamps

Transaction timestamps will be generated within the defined analysis period.

The timestamp-generation process will account for:

- Date
- Hour of day
- Non-uniform hourly transaction activity
- Moderate variation in daily transaction volume

The final timestamps will support monthly, daily, weekday, and hourly analysis.

---

### 7.5 Generate Transaction Amounts

Transaction amounts will be generated using a right-skewed distribution.

Generated amounts will then be constrained to the planned minimum and maximum
transaction values and rounded to two decimal places.

This approach will create:

- Many low-value transactions
- A meaningful number of medium-value transactions
- Relatively fewer high-value transactions

---

### 7.6 Assign Transaction Dimensions

Each transaction will be assigned categorical attributes based on the planned
distributions.

These include:

- bank_name
- city
- device_type
- app_version

Bank, city, and device assignments will use controlled probability
distributions.

Application-version assignment may also depend on transaction date to simulate
version adoption and rollout over time.

---

### 7.7 Calculate Transaction Failure Probability

Every transaction will begin with the baseline failure probability.

The probability may then be adjusted based on the simulated risk patterns
defined in Section 6.

Conceptually:

Final Failure Probability =
Baseline Probability
+ Bank Effect
+ App Version Effect
+ Device/App Interaction Effect
+ Time Effect
+ Transaction Amount Effect
+ Temporary Event Effect

Not every transaction will receive every adjustment.

The final probability will be constrained to a predefined reasonable range to
prevent invalid or unrealistic probability values.

---

### 7.8 Generate Transaction Status

After calculating the final failure probability, a random value between 0 and 1
will be generated for each transaction.

Conceptually:

If random value < Final Failure Probability:
    status = FAILED
Else:
    status = SUCCESS

This means transactions with higher simulated risk have a greater probability
of failure but are not guaranteed to fail.

---

### 7.9 Assign Failure Reasons

Failure reasons will be assigned only to transactions where:

status = FAILED

The probability of each failure reason may depend on selected transaction
characteristics and simulated failure patterns.

Successful transactions will have:

failure_reason = NULL

---

### 7.10 Construct Final Dataset

The generated fields will be combined into a single transaction-level dataset
using the schema defined in Section 3.

The final raw dataset will contain:

- transaction_id
- user_id
- txn_timestamp
- amount
- status
- failure_reason
- bank_name
- app_version
- device_type
- city

Derived analytical fields will not be permanently added to the initial raw
dataset unless required later.

---

### 7.11 Validate Generated Dataset

Before the dataset is accepted for analysis, validation checks will be
performed for:

- Row count
- Transaction ID uniqueness
- Missing values
- Date range
- Transaction amount range
- Allowed categorical values
- SUCCESS / FAILED distribution
- Failure reason consistency
- Bank distribution
- City distribution
- Device distribution
- App-version distribution
- Overall failure rate
- Failed GMV
- Intended simulated failure patterns

The generated dataset will only be used for downstream analysis after these
checks are completed.

---

### 7.12 Export Dataset

After successful validation, the transaction dataset will be exported to a
standard file format for downstream analysis.

The generated data file will be stored in the project `data/` directory.

The dataset can then be loaded into MySQL for SQL analysis and accessed through
Python and Power BI for subsequent analytical stages.

## 8. Reproducibility

The synthetic data generation process will be designed to be reproducible.

### 8.1 Random Seed

A fixed random seed will be used during dataset generation.

Planned random seed:

42

Using a fixed random seed ensures that running the generation script with the
same code and configuration produces the same simulated dataset and analytical
patterns.

This is important for:

- Reproducible analysis
- Consistent SQL results
- Consistent Python results
- Stable Power BI metrics
- Debugging and testing
- GitHub portfolio reproducibility

### 8.2 Configuration-Driven Generation

Important generation parameters will be defined clearly near the beginning of
the Python script rather than being hard-coded throughout the logic.

Examples include:

- Number of transactions
- Number of users
- Date range
- Random seed
- Category values
- Category probabilities
- Baseline failure probability
- Failure-risk adjustments

This makes the generation process easier to understand, modify, and reproduce.

### 8.3 Deterministic Output

If the generation logic, configuration values, Python environment, and random
seed remain unchanged, the generated dataset should remain reproducible.

Any intentional change to the generation assumptions should be documented.

## 9. Data Quality and Validation Rules

The generated dataset must pass a defined set of validation checks before it is
used for SQL, Python, or Power BI analysis.

### 9.1 Row Count Validation

Expected number of rows:

Approximately 1,000,000 transactions.

The generated row count must match the configured number of transactions.

---

### 9.2 Transaction ID Validation

- transaction_id must not contain null values.
- transaction_id must be unique.
- Duplicate transaction IDs are not allowed.

Expected condition:

Unique transaction IDs = Total transaction rows

---

### 9.3 User ID Validation

- user_id must not contain null values.
- Every user ID must follow the defined synthetic ID format.
- A user may appear in multiple transactions.

---

### 9.4 Timestamp Validation

All transaction timestamps must fall within:

2025-01-01 00:00:00

and

2025-12-31 23:59:59

No transaction should fall outside the defined analysis period.

---

### 9.5 Transaction Amount Validation

Transaction amounts must:

- Be greater than zero.
- Fall within the planned ₹10 to ₹50,000 range.
- Contain no null values.
- Be stored with appropriate numeric precision.

The distribution should also be reviewed to confirm that it remains
right-skewed as intended.

---

### 9.6 Transaction Status Validation

Allowed values:

- SUCCESS
- FAILED

No other transaction status should exist.

The overall failure rate should also be reviewed against the intended simulated
range.

---

### 9.7 Failure Reason Consistency

The following relationship must hold:

If status = SUCCESS:
    failure_reason must be NULL

If status = FAILED:
    failure_reason must not be NULL

Any record violating this rule will be treated as a data-quality failure.

---

### 9.8 Categorical Value Validation

Values for the following columns must belong to their documented allowed
categories:

- bank_name
- app_version
- device_type
- city
- failure_reason

Unexpected categorical values should not appear in the generated dataset.

---

### 9.9 Distribution Validation

Observed distributions will be compared with the planned distributions for:

- Banks
- Cities
- Device types
- Application versions
- Transaction amounts
- Transaction timestamps

Small differences are expected because of random sampling.

Large deviations will be investigated before accepting the dataset.

---

### 9.10 Failure Pattern Validation

The generated data will be checked to confirm that the intended simulated
failure patterns are present without becoming excessively dominant.

Validation will include comparisons of failure rates across:

- Banks
- Application versions
- Device types
- App-version and device combinations
- Transaction amount ranges
- Hours of day
- Temporary anomaly periods

The purpose of this validation is to confirm that the dataset contains
meaningful but non-deterministic analytical signals.

Validation confirms that the simulation behaves as designed; it is not an
analytical conclusion about real-world UPI behavior.

## 10. Output Files and Folder Strategy

Generated data and supporting Python files will follow the project repository
structure.

### 10.1 Python Generation Script

The synthetic data generation code will be stored in the `python/` directory.

Planned file:

python/generate_data.py

This script will contain the reproducible logic required to generate the
transaction dataset.

### 10.2 Validation Script or Notebook

Data validation and exploratory checks will also be maintained in the
`python/` directory.

The exact implementation may use Python scripts and/or Jupyter notebooks
depending on the analytical requirement.

### 10.3 Generated Dataset

The generated transaction dataset will be stored locally in the `data/`
directory.

Planned output:

data/upi_transactions.csv

### 10.4 GitHub Data Storage

The full generated dataset may be excluded from Git version control because a
dataset containing approximately 1,000,000 rows can unnecessarily increase
repository size.

The reproducible generation script will remain in GitHub so that the dataset can
be recreated locally.

A smaller sample dataset may be included later if useful for demonstrating the
data structure.

### 10.5 Downstream Usage

After generation and validation, the dataset will be used for:

1. MySQL data loading and SQL analysis.
2. Python exploratory and statistical analysis.
3. Power BI dashboard development.
4. Business insight and recommendation development.