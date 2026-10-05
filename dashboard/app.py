import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TeleConnect Analytics",
    page_icon="📊",
    layout="wide"
)

# PostgreSQL connection
engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# Title
st.title("📊 TeleConnect Analytics Dashboard")
st.markdown("### Telecom Data Engineering & Customer Analytics")

# -----------------------------
# KPI DATA
# -----------------------------

customer_count = pd.read_sql(
    """
    SELECT COUNT(*) AS total_customers
    FROM dw.dim_customer
    """,
    engine
)

revenue = pd.read_sql(
    """
    SELECT COALESCE(SUM(amount), 0) AS total_revenue
    FROM dw.fact_recharge
    """,
    engine
)

data_usage = pd.read_sql(
    """
    SELECT COALESCE(SUM(data_used_gb), 0) AS total_data_usage
    FROM dw.fact_usage
    """,
    engine
)

complaints = pd.read_sql(
    """
    SELECT COUNT(*) AS total_complaints
    FROM dw.fact_complaint
    """,
    engine
)

payment_success = pd.read_sql(
    """
    SELECT
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN status = 'SUCCESS' THEN 1
                    ELSE 0
                END
            ) / COUNT(*),
            2
        ) AS success_rate
    FROM dw.fact_payment
    """,
    engine
)

# -----------------------------
# KPI CARDS
# -----------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Customers",
    f"{customer_count.iloc[0]['total_customers']:,}"
)

col2.metric(
    "Recharge Revenue",
    f"₹{revenue.iloc[0]['total_revenue']:,.0f}"
)

col3.metric(
    "Data Usage (GB)",
    f"{data_usage.iloc[0]['total_data_usage']:,.2f}"
)

col4.metric(
    "Total Complaints",
    f"{complaints.iloc[0]['total_complaints']:,}"
)

col5.metric(
    "Payment Success Rate",
    f"{payment_success.iloc[0]['success_rate']:.2f}%"
)

st.divider()

# -----------------------------
# MONTHLY REVENUE
# -----------------------------

st.subheader("Monthly Recharge Revenue")

monthly_revenue = pd.read_sql(
    """
    SELECT
        d.year,
        d.month,
        d.month_name,
        SUM(f.amount) AS revenue
    FROM dw.fact_recharge f
    JOIN dw.dim_date d
        ON f.date_key = d.date_key
    GROUP BY
        d.year,
        d.month,
        d.month_name
    ORDER BY
        d.year,
        d.month
    """,
    engine
)

monthly_revenue["period"] = (
    monthly_revenue["year"].astype(str)
    + "-"
    + monthly_revenue["month"].astype(str).str.zfill(2)
)

st.line_chart(
    monthly_revenue.set_index("period")["revenue"]
)

# -----------------------------
# REVENUE BY PLAN
# -----------------------------

st.subheader("Revenue by Plan")

revenue_by_plan = pd.read_sql(
    """
    SELECT
        p.plan_name,
        SUM(f.amount) AS revenue
    FROM dw.fact_recharge f
    JOIN dw.dim_customer c
        ON f.customer_key = c.customer_key
    JOIN dw.dim_plan p
        ON c.plan_id = p.plan_id
    GROUP BY p.plan_name
    ORDER BY revenue DESC
    """,
    engine
)

st.bar_chart(
    revenue_by_plan.set_index("plan_name")["revenue"]
)

# -----------------------------
# DATA USAGE BY MONTH
# -----------------------------

st.subheader("Monthly Data Usage")

monthly_usage = pd.read_sql(
    """
    SELECT
        d.year,
        d.month,
        d.month_name,
        SUM(f.data_used_gb) AS data_usage_gb
    FROM dw.fact_usage f
    JOIN dw.dim_date d
        ON f.date_key = d.date_key
    GROUP BY
        d.year,
        d.month,
        d.month_name
    ORDER BY
        d.year,
        d.month
    """,
    engine
)

monthly_usage["period"] = (
    monthly_usage["year"].astype(str)
    + "-"
    + monthly_usage["month"].astype(str).str.zfill(2)
)

st.line_chart(
    monthly_usage.set_index("period")["data_usage_gb"]
)

# -----------------------------
# COMPLAINTS BY CATEGORY
# -----------------------------

st.subheader("Complaints by Category")

complaints_category = pd.read_sql(
    """
    SELECT
        category,
        COUNT(*) AS complaint_count
    FROM dw.fact_complaint
    GROUP BY category
    ORDER BY complaint_count DESC
    """,
    engine
)

st.bar_chart(
    complaints_category.set_index("category")["complaint_count"]
)

# -----------------------------
# NETWORK EVENTS BY CITY
# -----------------------------

st.subheader("Network Events by City")

network_events = pd.read_sql(
    """
    SELECT
        city,
        COUNT(*) AS event_count
    FROM dw.fact_network_event
    GROUP BY city
    ORDER BY event_count DESC
    """,
    engine
)

st.bar_chart(
    network_events.set_index("city")["event_count"]
)

# -----------------------------
# CUSTOMER 360
# -----------------------------

st.subheader("Customer 360")

customer_360 = pd.read_sql(
    """
    SELECT *
    FROM dw.customer_360
    ORDER BY customer_id
    LIMIT 100
    """,
    engine
)

st.dataframe(
    customer_360,
    use_container_width=True
)