# TeleConnect Data Engineering Platform

An end-to-end telecom data engineering project that simulates a real-world telecom company's data platform.

The project demonstrates data ingestion, data quality validation, ETL processing, PostgreSQL data warehousing, PySpark transformations, Customer 360 analytics, SQL analytics, and an interactive Streamlit dashboard.

---

## Project Objective

Build an end-to-end data pipeline that takes telecom source data through multiple processing layers and produces analytics-ready datasets.

The platform handles:

- Customer data
- Telecom plans
- Recharge transactions
- Usage data
- Complaints
- Payments
- Network events

The project also demonstrates how invalid records can be identified and separated before entering downstream processing.

---

## Architecture

```text
                    TELECOM SOURCE DATA
                           |
                           v
                    CSV Source Files
                           |
                           v
                  Python Data Validation
                           |
                +----------+----------+
                |                     |
                v                     v
          Valid Records         Rejected Records
                |                     |
                v                     v
        Processed CSV Files     Rejected CSV Files
                |
                v
        PostgreSQL RAW Layer
                |
                v
       PostgreSQL STAGING Layer
                |
                v
          PySpark Processing
                |
                +----------------+
                |                |
                v                v
        Analytical Data     Customer 360
                |                |
                +--------+-------+
                         |
                         v
               PostgreSQL DW Layer
                         |
                         v
                  SQL Analytics
                         |
                         v
               Streamlit Dashboard
```

---

## Technologies Used

### Programming

- Python
- PySpark

### Database

- PostgreSQL
- SQL
- pgAdmin

### Data Engineering

- ETL
- Data Quality Validation
- Referential Integrity
- Data Warehouse
- Star Schema
- Fact Tables
- Dimension Tables
- Surrogate Keys

### Analytics

- SQL Analytics
- Customer 360
- Streamlit Dashboard
- Pandas

### Development Tools

- VS Code
- Git
- GitHub

---

## Data Sources

The project uses synthetic telecom data.

| Dataset        | Records |
| -------------- | ------: |
| Customers      |   1,000 |
| Plans          |       4 |
| Recharges      |  10,000 |
| Usage          |  20,000 |
| Complaints     |   5,000 |
| Network Events |   3,000 |
| Payments       |  12,000 |

Total source records:

**51,004**

---

## Data Quality

The pipeline performs multiple validation checks before data moves downstream.

### Validation checks

- Record count validation
- Missing value validation
- Duplicate ID validation
- Business rule validation
- Referential integrity validation

Example:

```text
recharges.customer_id → customers.customer_id
```

Invalid records are separated into a rejected-data area instead of being loaded into the processed dataset.

### Example

The synthetic dataset intentionally contains invalid recharge records such as:

- Invalid customer ID
- Negative recharge amount
- Invalid payment mode
- Invalid recharge status

These records are rejected during processing.

---

## PostgreSQL Data Layers

### RAW Layer

The RAW layer stores source data with minimal transformation.

Tables:

```text
raw.customers
raw.plans
raw.recharges
raw.usage
raw.complaints
raw.network_events
raw.payments
```

### STAGING Layer

The STAGING layer contains validated and processed records.

Tables:

```text
staging.customers
staging.plans
staging.recharges
staging.usage
staging.complaints
staging.network_events
staging.payments
```

### Data Warehouse Layer

The warehouse follows a dimensional/star-schema design.

---

## Data Warehouse

### Dimension Tables

```text
dw.dim_customer
dw.dim_plan
dw.dim_date
```

### Fact Tables

```text
dw.fact_recharge
dw.fact_usage
dw.fact_payment
dw.fact_complaint
dw.fact_network_event
```

### Dimension Responsibilities

**dim_customer**

Contains customer-related descriptive information.

**dim_plan**

Contains telecom plan information.

**dim_date**

Provides reusable date attributes for analytical queries.

---

## Surrogate Keys

The warehouse uses surrogate keys such as:

```text
customer_key
recharge_key
date_key
```

These warehouse-generated keys provide stable identifiers for relationships between fact and dimension tables.

For example:

```text
fact_recharge.customer_key
        |
        v
dim_customer.customer_key
```

The original business identifier such as `customer_id` is retained as a natural/source key.

---

## PySpark Processing

PySpark is used to perform analytical transformations on telecom data.

Current transformations include:

### Recharge Analysis

Calculates customer-level:

- Successful recharge count
- Total recharge amount
- Average recharge amount

### Usage Analysis

Calculates customer-level:

- Total data usage
- Total voice minutes
- Total SMS
- Usage record count

### Customer 360

The recharge and usage summaries are combined to create an analytical Customer 360 dataset.

Example metrics:

```text
customer_id
successful_recharges
total_recharge_amount
average_recharge_amount
total_data_used_gb
total_voice_minutes
total_sms
usage_records
```

The Customer 360 dataset currently contains 999 customers because it is based on successful recharge activity; customers with only failed recharge transactions are not included in the recharge aggregation.

---

## SQL Analytics

The project includes analytical SQL queries for areas such as:

- Monthly recharge revenue
- Revenue by plan
- Active customers by plan
- Monthly data usage
- Top customers by data usage
- Complaints by category
- Complaints by priority
- Monthly complaint trends
- Payment success rate
- Network events by city
- Network events by severity
- Network events by event type
- Monthly payment revenue

---

## Streamlit Dashboard

An interactive dashboard has been created using Streamlit.

### Dashboard KPIs

- Total Customers
- Recharge Revenue
- Total Data Usage
- Total Complaints
- Payment Success Rate

### Dashboard Charts

- Monthly Recharge Revenue
- Revenue by Plan
- Monthly Data Usage
- Complaints by Category
- Network Events by City

The dashboard also displays a Customer 360 data table.

---

## Pipeline Execution

The project includes a central pipeline controller:

```text
main.py
```

The pipeline coordinates the major processing stages.

Run:

```powershell
python main.py
```

The pipeline processes validated data, loads the staging layer, and loads the data warehouse.

---

## Dashboard Execution

Start the Streamlit dashboard using:

```powershell
streamlit run dashboard/app.py
```

The dashboard runs locally in the browser.

---

## Final Warehouse Validation

The final V1 pipeline was tested successfully.

| Warehouse Table    | Records |
| ------------------ | ------: |
| dim_customer       |   1,000 |
| dim_plan           |       4 |
| dim_date           |   1,096 |
| fact_recharge      |   9,996 |
| fact_usage         |  20,000 |
| fact_payment       |  12,000 |
| fact_complaint     |   5,000 |
| fact_network_event |   3,000 |
| customer_360       |     999 |

All expected warehouse record counts were successfully validated.

---

## Project Structure

```text
telecom-data-engineering-platform/
│
├── data/
│   ├── source/
│   ├── raw/
│   ├── processed/
│   ├── archive/
│   └── rejected/
│
├── src/
│   ├── database.py
│   ├── data_quality.py
│   ├── process_dataset.py
│   ├── process_all.py
│   ├── simulate_bad_data.py
│   ├── load_processed_to_staging.py
│   └── pyspark_transform.py
│
├── sql/
│   ├── create_raw_schema.sql
│   ├── create_staging_schema.sql
│   ├── create_dw_schema.sql
│   ├── load_dw.sql
│   └── analytics.sql
│
├── dashboard/
│   └── app.py
│
├── tests/
│
├── logs/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Key Data Engineering Concepts Demonstrated

This project demonstrates practical understanding of:

- ETL pipelines
- Data ingestion
- Data validation
- Data quality
- Referential integrity
- Rejected-record handling
- RAW and STAGING layers
- Data warehouse design
- Star schema
- Fact and dimension tables
- Surrogate keys
- SQL analytics
- PySpark DataFrames
- Aggregations
- Joins
- PostgreSQL JDBC connectivity
- Customer 360 analytics
- Dashboard development

---

## Future Enhancements

The following technologies are planned as future improvements and are **not part of the current V1 implementation**:

- Apache Airflow for workflow orchestration
- dbt for SQL transformation management
- AWS S3 / Glue / Redshift
- Kafka for real-time streaming
- Incremental data loading
- Change Data Cap
