# Business Requirements

## 1. Business Scenario

A digital payments platform processes a large volume of UPI transactions across
multiple banks, cities, devices, and application versions.

Although the majority of transactions are completed successfully, a portion of
transactions fail due to different technical and operational reasons.

Even a relatively small failure rate can affect a large number of transactions
when overall transaction volume is high. These failures may negatively impact
customer experience and may also put transaction value at risk.

The analytics team has been asked to investigate transaction reliability and
identify patterns associated with failed transactions.

The analysis will focus on understanding:

- How frequently UPI transactions fail.
- When transaction failures are most common.
- Whether failure rates differ across banks.
- Whether certain application versions or device types show higher failure rates.
- Which failure reasons contribute most to unsuccessful transactions.
- How much transaction value is associated with failed transactions.
- Which segments should be investigated first for reliability improvements.

## 2. Business Problem Statement

UPI transaction failures can negatively affect payment reliability and customer
experience. At high transaction volumes, even a small failure rate can represent
a significant number of unsuccessful payment attempts and a substantial amount
of transaction value.

The business currently needs better visibility into where and when transaction
failures occur and which dimensions are most strongly associated with them.

The key business problem is therefore to identify and quantify transaction
failure patterns across different dimensions such as:

- Time periods
- Banks
- Failure reasons
- Application versions
- Device types
- Cities
- Transaction amount ranges

The analysis should help stakeholders identify high-impact failure segments,
understand the transaction value associated with failed payments, and prioritize
areas for further investigation and reliability improvement.

This project does not assume that correlation between a dimension and failure
rate proves that the dimension caused the failure. The analysis is intended to
identify patterns and potential areas for investigation rather than establish
causality.

## 3. Business Objectives

The primary objective of this project is to evaluate UPI payment reliability
and identify transaction segments associated with elevated failure rates and
high failed transaction value.

The analysis aims to:

1. Measure the overall transaction success and failure rates.

2. Track transaction volume and failure rate over time to identify trends,
   spikes, and unusual periods.

3. Compare payment reliability across banks and identify banks with relatively
   high failure rates or failed transaction volumes.

4. Analyze failure reasons to understand which categories account for the
   largest share of failed transactions.

5. Evaluate transaction reliability across application versions and device
   types to identify potential technical patterns.

6. Analyze geographic differences in transaction performance across cities.

7. Determine whether transaction amount ranges show different failure patterns.

8. Quantify the total transaction value associated with failed payments
   (Failed GMV / GMV at Risk).

9. Identify high-impact combinations of dimensions, such as bank, app version,
   device type, time period, or failure reason, that warrant further
   investigation.

10. Translate analytical findings into prioritized, evidence-based business
    recommendations.

## 4. Analytical Questions

The analysis will answer the following business questions.

### 4.1 Overall Payment Reliability

1. How many transactions were processed during the analysis period?
2. What percentage of transactions were successful versus failed?
3. What is the overall transaction failure rate?
4. What is the total transaction value (GMV)?
5. What transaction value is associated with failed transactions (Failed GMV / GMV at Risk)?

### 4.2 Failure Trends Over Time

6. How does the transaction failure rate change over time?
7. Are there specific dates or periods with unusually high failure rates?
8. How does failure rate vary by hour of the day?
9. Are there differences in transaction reliability across days of the week?
10. Do high-volume periods also experience higher failure rates?

### 4.3 Bank-Level Analysis

11. How does transaction failure rate vary across banks?
12. Which banks contribute the largest number of failed transactions?
13. Which banks account for the highest failed transaction value?
14. Are high failure counts driven by high transaction volume or by unusually high failure rates?

### 4.4 Failure Reason Analysis

15. What are the most common reasons for failed transactions?
16. What percentage of total failures does each failure reason represent?
17. Which failure reasons account for the highest failed transaction value?
18. Do failure-reason patterns differ across banks or other transaction segments?

### 4.5 Application and Device Analysis

19. How does failure rate vary across application versions?
20. Are older or specific application versions associated with elevated failure rates?
21. How does transaction reliability differ across device types?
22. Are there particular app-version and device-type combinations with unusually high failure rates?

### 4.6 Geographic Analysis

23. How does transaction volume vary across cities?
24. How does transaction failure rate vary across cities?
25. Which cities contribute the highest number and value of failed transactions?

### 4.7 Transaction Amount Analysis

26. Does failure rate vary across transaction amount ranges?
27. Are higher-value transactions associated with different failure patterns?
28. Which amount ranges contribute the most to Failed GMV?

### 4.8 Multi-Dimensional Investigation

29. Which combinations of bank, app version, device type, city, time period,
    and failure reason show elevated failure rates?

30. Which segments combine high transaction volume, high failure rate, and high
    Failed GMV, making them important candidates for further investigation?

31. Are observed failure patterns concentrated within specific segments, or are
    they broadly distributed across the transaction population?

### 4.9 Business Impact and Prioritization

32. What proportion of total GMV is associated with failed transactions?
33. Which segments contribute most significantly to overall payment failures?
34. Which failure patterns should be prioritized for further technical or
    operational investigation based on transaction volume, failure rate, and
    Failed GMV?

## 5. Scope and Assumptions

### 5.1 Project Scope

This project analyzes synthetic UPI transaction data to evaluate payment
reliability, identify failure patterns, quantify failed transaction value,
and identify segments that may require further investigation.

The analysis will cover:

- Approximately 1,000,000 synthetic UPI transactions.
- Transactions occurring between January 2025 and December 2025.
- Transaction success and failure performance.
- Transaction volume and value trends over time.
- Failure patterns across banks.
- Failure reason analysis.
- Application version and device-level analysis.
- Geographic analysis across selected cities.
- Transaction amount-based analysis.
- Failed transaction value (Failed GMV / GMV at Risk).
- Multi-dimensional analysis to identify high-impact failure segments.

SQL will be used for structured querying and business analysis, Python will be
used for data generation, validation, exploratory analysis, and deeper
statistical investigation, and Power BI will be used for interactive reporting
and business-facing visualization.

### 5.2 Assumptions

The following assumptions apply to this project:

1. The dataset is completely synthetic and does not represent transactions from
   any real UPI provider, bank, customer, or payment platform.

2. Transaction patterns, failure rates, failure reasons, bank performance,
   application-version behavior, and other relationships in the dataset are
   simulated for analytical and portfolio purposes.

3. Each transaction has a unique transaction ID and represents one payment
   attempt.

4. Transaction status will be classified primarily as SUCCESS or FAILED.

5. A failed transaction represents an unsuccessful payment attempt in the
   simulated dataset.

6. Failed transaction amount will be treated as Failed GMV / GMV at Risk for
   analytical purposes. It should not automatically be interpreted as permanent
   revenue loss because the customer may retry the payment or complete the
   transaction through another method.

7. Observed relationships between transaction dimensions and failure rates
   represent associations within the simulated dataset and do not establish
   causal relationships.

8. Failure reasons included in the dataset are simplified analytical categories
   and may not represent the complete complexity of real-world UPI payment
   failure systems.

9. The analysis will focus on transaction-level data. Customer-level retention,
   customer lifetime value, merchant economics, actual platform revenue, and
   retry behavior are outside the current scope unless additional simulated data
   is introduced later.

10. Business recommendations will be based on patterns observed in the synthetic
    dataset and should be interpreted as analytical recommendations for the
    simulated business scenario.

## 6. Expected Deliverables

The project will produce the following deliverables:

### 6.1 Business Documentation

- Business requirements document defining the business scenario, problem,
  objectives, analytical questions, scope, and assumptions.
- KPI definition document describing the business metrics used throughout the
  analysis.
- Data generation plan documenting the structure and simulated behavior of the
  synthetic dataset.

### 6.2 Synthetic Transaction Dataset

A reproducible synthetic UPI transaction dataset containing approximately
1,000,000 transaction records with relevant transaction, payment, technical,
and geographic attributes.

### 6.3 SQL Analysis

A structured collection of SQL queries covering:

- Overall transaction performance.
- Success and failure rates.
- Time-based transaction trends.
- Bank-level performance.
- Failure reason analysis.
- Application version and device analysis.
- Geographic analysis.
- Transaction amount analysis.
- Failed GMV analysis.
- Multi-dimensional failure investigation.

### 6.4 Python Analysis

Python notebooks/scripts covering:

- Synthetic data generation.
- Data quality validation.
- Exploratory data analysis.
- Statistical investigation of failure patterns.
- Segment-level analysis.
- Supporting visualizations where appropriate.

### 6.5 Power BI Dashboard

An interactive Power BI dashboard designed for business stakeholders,
including views for:

- Executive payment reliability overview.
- Failure trends over time.
- Bank performance.
- Failure reason analysis.
- Application and device performance.
- Geographic and transaction amount analysis.
- Failed GMV and high-impact segment identification.

### 6.6 Business Insights and Recommendations

A final set of evidence-based findings highlighting:

- Major transaction reliability patterns.
- High-impact failure segments.
- Important contributors to Failed GMV.
- Areas requiring further technical or operational investigation.
- Potential actions that could improve payment reliability in the simulated
  business scenario.

### 6.7 GitHub Portfolio Repository

A structured GitHub repository containing project documentation, SQL queries,
Python code, dashboard-related files, and a README summarizing the complete
analysis and key findings.