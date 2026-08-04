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

# Payment-type filter
payment_types_df = run_query(
    f"""
    SELECT DISTINCT payment_type_label
    FROM {DB_SCHEMA}.fct_trips
    WHERE payment_type_label IS NOT NULL
    ORDER BY payment_type_label
    """
)

payment_types = ["All"] + payment_types_df["payment_type_label"].tolist()

selected_payment_type = st.sidebar.selectbox(
    "Payment type",
    payment_types,
)

if selected_payment_type == "All":
    where_clause = ""
else:
    safe_payment_type = selected_payment_type.replace("'", "''")
    where_clause = (
        "WHERE payment_type_label = "
        f"'{safe_payment_type}'"
    )


# Panel 1: Headline KPIs
st.subheader("Headline KPIs")

kpi_df = run_query(
    f"""
    SELECT
        COUNT(*) AS total_trips,
        AVG(trip_distance) AS avg_trip_distance,
        AVG(fare_per_mile) AS avg_fare_per_mile
    FROM {DB_SCHEMA}.fct_trips
    {where_clause}
    """
)

kpis = kpi_df.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total trips",
    f"{int(kpis['total_trips']):,}",
)

col2.metric(
    "Average trip distance",
    f"{kpis['avg_trip_distance']:.2f} miles",
)

col3.metric(
    "Average fare per mile",
    f"${kpis['avg_fare_per_mile']:.2f}",
)


# Panel 2: Trip count by hour
st.subheader("Trip count by hour of day")

hourly_trips = run_query(
    f"""
    SELECT
        EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour,
        COUNT(*) AS trip_count
    FROM {DB_SCHEMA}.fct_trips
    {where_clause}
    GROUP BY EXTRACT(HOUR FROM pickup_datetime)
    ORDER BY pickup_hour
    """
)

st.line_chart(
    hourly_trips,
    x="pickup_hour",
    y="trip_count",
    x_label="Pickup hour (0–23)",
    y_label="Number of trips",
)


# Panel 3: Data freshness
st.subheader("Data freshness")

freshness_df = run_query(
    f"""
    SELECT
        COUNT(*) AS row_count,
        MAX(pickup_datetime) AS latest_pickup_datetime
    FROM {DB_SCHEMA}.fct_trips
    {where_clause}
    """
)

freshness = freshness_df.iloc[0]

fresh_col1, fresh_col2 = st.columns(2)

fresh_col1.metric(
    "Row count",
    f"{int(freshness['row_count']):,}",
)

fresh_col2.metric(
    "Latest pickup datetime",
    freshness["latest_pickup_datetime"].strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
)