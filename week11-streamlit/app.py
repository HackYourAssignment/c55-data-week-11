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

payment_types_query = f"""
SELECT DISTINCT payment_type_label
FROM {DB_SCHEMA}.fct_trips
WHERE payment_type_label IS NOT NULL
ORDER BY payment_type_label
"""

payment_types = run_query(payment_types_query)["payment_type_label"].tolist()

selected_payment = st.sidebar.selectbox(
    "Payment Type",
    ["All"] + payment_types,
)

if selected_payment == "All":
    where_clause = ""
else:
    escaped_payment = selected_payment.replace("'", "''")
    where_clause = (
        f"WHERE payment_type_label = '{escaped_payment}'"
    )

st.subheader("Headline KPIs")

kpi_query = f"""
SELECT
    COUNT(*) AS total_trips,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(fare_per_mile) AS avg_fare_per_mile
FROM {DB_SCHEMA}.fct_trips
{where_clause}
"""

kpi_data = run_query(kpi_query).iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Total Trips",
    value=f"{int(kpi_data['total_trips']):,}",
)

col2.metric(
    label="Average Trip Distance",
    value=(
        f"{kpi_data['avg_trip_distance']:.2f} miles"
        if pd.notna(kpi_data["avg_trip_distance"])
        else "No data"
    ),
)

col3.metric(
    label="Average Fare per Mile",
    value=(
        f"${kpi_data['avg_fare_per_mile']:.2f}"
        if pd.notna(kpi_data["avg_fare_per_mile"])
        else "No data"
    ),
)

st.subheader("Trips by Hour of Day")

hourly_query = f"""
SELECT
    EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour,
    COUNT(*) AS trip_count
FROM {DB_SCHEMA}.fct_trips
{where_clause}
GROUP BY pickup_hour
ORDER BY pickup_hour
"""

hourly_data = run_query(hourly_query)

st.line_chart(
    hourly_data,
    x="pickup_hour",
    y="trip_count",
)

st.subheader("Data Freshness")

freshness_query = f"""
SELECT
    COUNT(*) AS row_count,
    MAX(pickup_datetime) AS latest_pickup
FROM {DB_SCHEMA}.fct_trips
{where_clause}
"""

freshness = run_query(freshness_query).iloc[0]

col1, col2 = st.columns(2)

col1.metric(
    label="Row Count",
    value=f"{int(freshness['row_count']):,}",
)

col2.metric(
    label="Latest Pickup",
    value=(
        freshness["latest_pickup"].strftime("%Y-%m-%d %H:%M:%S")
        if pd.notna(freshness["latest_pickup"])
        else "No data"
    ),
)