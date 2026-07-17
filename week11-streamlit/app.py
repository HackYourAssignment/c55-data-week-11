"""NYC Taxi metrics dashboard — Week 11 assignment starter.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. The page
setup and the ``run_query`` caching helper are already wired up (same
pattern taught in "Building a Metrics Dashboard"). Your job: implement the
three TODO-stubbed KPI queries below with your own SQL, then (Required tier)
add the hour-of-day trend, freshness panel, and payment-type filter
described in the assignment brief.
"""

import os

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # reads .env file if present

POSTGRES_URL = os.environ["POSTGRES_URL"]
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname")

st.set_page_config(page_title="NYC Taxi Metrics", layout="wide")
st.title("NYC Taxi Metrics")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


payment_options_query = f"""
SELECT DISTINCT
    CASE
        WHEN payment_type = 1 THEN 'Credit card'
        WHEN payment_type = 2 THEN 'Cash'
        WHEN payment_type = 3 THEN 'No charge'
        WHEN payment_type = 4 THEN 'Dispute'
        WHEN payment_type = 5 THEN 'Unknown'
        WHEN payment_type = 6 THEN 'Voided trip'
        WHEN payment_type IS NULL THEN 'Not Recorded'
        ELSE 'Other'
    END AS payment_type_label
FROM {DB_SCHEMA}.vw_fact_trips;
"""

payment_df = run_query(payment_options_query)
payment_options = ["All"] + sorted(
    [val for val in payment_df["payment_type_label"].unique() if val is not None]
)
selected_payment = st.sidebar.selectbox("Filter by Payment Type", payment_options)

st.subheader("Headline KPIs")
kpi_query = f"""
WITH base_trips AS (
    SELECT 
        *,
        CASE
            WHEN payment_type = 1 THEN 'Credit card'
            WHEN payment_type = 2 THEN 'Cash'
            WHEN payment_type = 3 THEN 'No charge'
            WHEN payment_type = 4 THEN 'Dispute'
            WHEN payment_type = 5 THEN 'Unknown'
            WHEN payment_type = 6 THEN 'Voided trip'
            WHEN payment_type IS NULL THEN 'Not Recorded'
            ELSE 'Other'
        END AS payment_type_label
    FROM {DB_SCHEMA}.vw_fact_trips
)
SELECT
    COUNT(*) AS total_trips,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(
        CASE 
            WHEN trip_distance > 0 THEN fare_amount / trip_distance 
            ELSE 0 
        END
    ) AS avg_fare_per_mile
FROM base_trips
WHERE 1=1
"""

if selected_payment != "All":
    kpi_query += f" AND payment_type_label = '{selected_payment}'"

kpi_df = run_query(kpi_query)
total_trips = kpi_df["total_trips"].iloc[0] or 0
avg_trip_distance = kpi_df["avg_trip_distance"].iloc[0] or 0
avg_fare_per_mile = kpi_df["avg_fare_per_mile"].iloc[0] or 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=f"{total_trips:,}")
with col2:
    st.metric(label="Avg Trip Distance", value=f"{avg_trip_distance:.2f} miles")
with col3:
    st.metric(label="Avg Fare per Mile", value=f"${avg_fare_per_mile:.2f}")

st.subheader("Trip Count by Hour of Day")

hour_query = f"""
WITH base_trips AS (
    SELECT 
        *,
        CASE
            WHEN payment_type = 1 THEN 'Credit card'
            WHEN payment_type = 2 THEN 'Cash'
            WHEN payment_type = 3 THEN 'No charge'
            WHEN payment_type = 4 THEN 'Dispute'
            WHEN payment_type = 5 THEN 'Unknown'
            WHEN payment_type = 6 THEN 'Voided trip'
            WHEN payment_type IS NULL THEN 'Not Recorded'
            ELSE 'Other'
        END AS payment_type_label
    FROM {DB_SCHEMA}.vw_fact_trips
)
SELECT 
    EXTRACT(HOUR FROM pickup_datetime) AS hour_of_day,
    COUNT(*) AS trip_count
FROM base_trips
WHERE 1=1
"""

if selected_payment != "All":
    hour_query += f" AND payment_type_label = '{selected_payment}'"

hour_query += " GROUP BY 1 ORDER BY 1;"

hour_df = run_query(hour_query)

st.line_chart(data=hour_df.set_index("hour_of_day"), y="trip_count")

st.subheader("Data Freshness Status")
freshness_query = f"""
SELECT 
    COUNT(*) AS total_rows,
    MAX(pickup_datetime) AS latest_pickup
FROM {DB_SCHEMA}.vw_fact_trips;
"""
fresh_df = run_query(freshness_query)
total_rows = fresh_df["total_rows"].iloc[0] or 0
latest_pickup = fresh_df["latest_pickup"].iloc[0]

col_f1, col_f2 = st.columns(2)
with col_f1:
    st.metric(label="Total Database Rows", value=f"{total_rows:,}")
with col_f2:
    st.metric(label="Latest Pickup Datetime", value=str(latest_pickup))
