# KPI Definitions

## 1. Purpose

This document defines the key performance indicators (KPIs) used throughout the
UPI Payment Reliability & Revenue Impact Analysis project.

The purpose of defining KPIs before performing the analysis is to ensure that
metrics are calculated consistently across SQL, Python, and Power BI.

The KPIs focus on three primary areas:

- Transaction volume
- Payment reliability
- Transaction value associated with successful and failed payments

All metrics in this project are calculated using synthetic transaction data and
represent the simulated business scenario defined in the business requirements.

## 2. Core Transaction KPIs

### 2.1 Total Transactions

**Definition:**  
Total number of payment attempts processed during the selected analysis period.

**Formula:**

Total Transactions = Count of unique transaction IDs

**Business Interpretation:**  
Measures the overall transaction volume processed by the platform.

---

### 2.2 Successful Transactions

**Definition:**  
Number of transactions with a status of `SUCCESS`.

**Formula:**

Successful Transactions = Count of transactions where status = SUCCESS

**Business Interpretation:**  
Represents payment attempts that were successfully completed.

---

### 2.3 Failed Transactions

**Definition:**  
Number of transactions with a status of `FAILED`.

**Formula:**

Failed Transactions = Count of transactions where status = FAILED

**Business Interpretation:**  
Represents unsuccessful payment attempts and provides the base measure for
transaction failure analysis.

---

### 2.4 Success Rate

**Definition:**  
Percentage of total transactions that were successfully completed.

**Formula:**

Success Rate (%) = (Successful Transactions / Total Transactions) × 100

**Business Interpretation:**  
Measures the overall reliability of payment completion. A higher success rate
indicates that a larger proportion of payment attempts are completed
successfully.

---

### 2.5 Failure Rate

**Definition:**  
Percentage of total transactions that failed.

**Formula:**

Failure Rate (%) = (Failed Transactions / Total Transactions) × 100

**Business Interpretation:**  
Measures the proportion of unsuccessful payment attempts and serves as one of
the primary reliability KPIs in this project.

For a dataset containing only `SUCCESS` and `FAILED` statuses:

Success Rate + Failure Rate = 100%

## 3. Transaction Value KPIs

### 3.1 Total GMV

**Definition:**  
Total monetary value of all payment attempts processed during the selected
analysis period, including both successful and failed transactions.

**Formula:**

Total GMV = Sum of transaction amount for all transactions

**Business Interpretation:**  
Represents the total payment value attempted through the platform during the
analysis period.

---

### 3.2 Successful GMV

**Definition:**  
Total monetary value of transactions with a status of `SUCCESS`.

**Formula:**

Successful GMV = Sum of transaction amount where status = SUCCESS

**Business Interpretation:**  
Represents the transaction value associated with successfully completed
payments.

---

### 3.3 Failed GMV / GMV at Risk

**Definition:**  
Total monetary value associated with transactions with a status of `FAILED`.

**Formula:**

Failed GMV = Sum of transaction amount where status = FAILED

**Business Interpretation:**  
Represents the value of payment attempts that were not successfully completed
during the transaction attempt.

In this project, Failed GMV may also be referred to as GMV at Risk.

Failed GMV should not be interpreted as confirmed revenue loss because a failed
transaction may later be retried successfully or completed using another payment
method.

---

### 3.4 Failed GMV Rate

**Definition:**  
Percentage of total attempted transaction value associated with failed
transactions.

**Formula:**

Failed GMV Rate (%) = (Failed GMV / Total GMV) × 100

**Business Interpretation:**  
Measures the proportion of attempted transaction value associated with
unsuccessful payment attempts.

This metric complements transaction Failure Rate because transaction count and
transaction value can produce different business perspectives.

---

### 3.5 Average Transaction Value (ATV)

**Definition:**  
Average monetary value of a transaction during the selected analysis period.

**Formula:**

Average Transaction Value = Total GMV / Total Transactions

**Business Interpretation:**  
Measures the average value of payment attempts processed by the platform.

ATV can also be calculated for specific transaction segments, such as successful
transactions, failed transactions, banks, cities, devices, or application
versions.

## 4. Segment and Diagnostic KPIs

The following KPIs are used to compare transaction performance across dimensions
such as bank, city, application version, device type, transaction amount band,
time period, and failure reason.

### 4.1 Transaction Volume Share

**Definition:**  
Percentage of total transactions contributed by a particular segment.

**Formula:**

Transaction Volume Share (%) =
(Segment Transactions / Total Transactions) × 100

**Business Interpretation:**  
Shows how much of the platform's overall transaction activity comes from a
specific segment.

This metric provides context when interpreting failure counts and failure rates.

---

### 4.2 Failure Contribution

**Definition:**  
Percentage of all failed transactions contributed by a particular segment.

**Formula:**

Failure Contribution (%) =
(Segment Failed Transactions / Total Failed Transactions) × 100

**Business Interpretation:**  
Measures how much a segment contributes to the platform's total failed
transaction count.

A segment may have a moderate failure rate but still contribute a large number
of failures because it processes a high transaction volume.

---

### 4.3 Failed GMV Contribution

**Definition:**  
Percentage of total Failed GMV contributed by a particular segment.

**Formula:**

Failed GMV Contribution (%) =
(Segment Failed GMV / Total Failed GMV) × 100

**Business Interpretation:**  
Shows which segments account for the largest share of transaction value
associated with failed payment attempts.

This metric helps identify segments with greater financial-value exposure even
when their failed transaction counts are relatively low.

---

### 4.4 Segment Failure Rate

**Definition:**  
Percentage of transactions within a specific segment that failed.

**Formula:**

Segment Failure Rate (%) =
(Segment Failed Transactions / Segment Total Transactions) × 100

**Business Interpretation:**  
Measures payment reliability within a particular segment.

It can be calculated for dimensions such as:

- Bank
- City
- Application version
- Device type
- Transaction amount band
- Hour
- Day of week
- Month

---

### 4.5 Failure Rate Index

**Definition:**  
Ratio of a segment's failure rate to the overall platform failure rate.

**Formula:**

Failure Rate Index =
Segment Failure Rate / Overall Failure Rate

**Business Interpretation:**  
Provides a normalized way to compare a segment's failure performance with the
overall platform baseline.

Interpretation:

- Failure Rate Index = 1.00 → Segment is equal to the overall failure rate.
- Failure Rate Index > 1.00 → Segment has a higher failure rate than the overall
  baseline.
- Failure Rate Index < 1.00 → Segment has a lower failure rate than the overall
  baseline.

This metric indicates relative performance and does not establish the cause of
the difference.

---

### 4.6 Segment Failed GMV Rate

**Definition:**  
Percentage of attempted transaction value within a segment that is associated
with failed transactions.

**Formula:**

Segment Failed GMV Rate (%) =
(Segment Failed GMV / Segment Total GMV) × 100

**Business Interpretation:**  
Measures the value-based impact of payment failures within a particular segment.

This metric is useful when transaction amounts vary significantly across
segments.

## 5. KPI Interpretation and Analytical Guardrails

The KPIs defined in this project should be interpreted together rather than in
isolation. The following analytical principles will be applied throughout the
analysis.

### 5.1 Count vs Rate

Failure count and failure rate measure different aspects of transaction
performance.

A high-volume segment may contribute a large number of failed transactions even
when its failure rate is relatively low. Conversely, a low-volume segment may
show a high failure rate while contributing relatively few failures overall.

Therefore, failure count, failure rate, and transaction volume should be
evaluated together.

---

### 5.2 Sample Size Awareness

Failure rates should be interpreted in the context of transaction volume.

Segments with very small transaction counts may show extremely high or low
failure rates due to limited observations.

For example, a segment with 2 failures out of 10 transactions has a 20% failure
rate, but this should not automatically be treated as more important than a
segment processing hundreds of thousands of transactions.

Transaction volume will therefore be considered when identifying high-impact
segments.

---

### 5.3 Failure Rate vs Failure Contribution

Failure Rate measures the percentage of transactions that fail within a
segment.

Failure Contribution measures the percentage of the platform's total failures
coming from that segment.

A segment can therefore have:

- High failure rate but low failure contribution.
- Low failure rate but high failure contribution.
- High failure rate and high failure contribution.

These situations may require different levels or types of investigation.

---

### 5.4 Transaction Count vs Transaction Value

Transaction-based KPIs and value-based KPIs may produce different conclusions.

A segment may contribute relatively few failed transactions but account for a
large proportion of Failed GMV if its transactions tend to have higher monetary
values.

For this reason, both failure volume and Failed GMV will be considered when
evaluating business impact.

---

### 5.5 Failed GMV Is Not Confirmed Revenue Loss

Failed GMV represents the transaction value associated with unsuccessful
payment attempts.

It does not represent confirmed revenue loss.

A failed payment may subsequently be:

- Retried successfully.
- Completed through another payment method.
- Abandoned by the customer.

Because the synthetic dataset does not currently track retry outcomes or actual
platform revenue, Failed GMV will be treated as transaction value at risk rather
than confirmed financial loss.

---

### 5.6 Association Does Not Establish Causation

A higher failure rate associated with a bank, application version, device type,
city, time period, or other dimension does not prove that the dimension caused
the transaction failure.

Observed relationships will be treated as signals for further investigation.

Where appropriate, multiple dimensions will be analyzed together to determine
whether an apparent pattern may be associated with other variables.

---

### 5.7 Percentage-Point vs Percentage Change

Changes in percentage-based KPIs should distinguish between percentage-point
change and relative percentage change.

For example, if failure rate increases from 5% to 6%:

Percentage-point increase = 6% - 5% = 1 percentage point

Relative percentage increase = ((6% - 5%) / 5%) × 100 = 20%

These two measures should not be used interchangeably.

---

### 5.8 Rounding

Rates and percentages displayed in reports may be rounded for readability.

Underlying calculations should use the available precision before presentation
rounding is applied.

Consistent rounding rules will be maintained across SQL, Python, and Power BI.