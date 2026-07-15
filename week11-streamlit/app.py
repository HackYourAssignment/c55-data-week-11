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
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_halyna")

st.set_page_config(page_title="NYC Taxi Metrics", layout="wide")
st.title("NYC Taxi Metrics")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    """Run a SQL query against the Postgres database and return a DataFrame."""
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


# Sidebar filter: payment type
# -----------------------------

st.sidebar.header("Filters")

payment_types = run_query(f"""
    SELECT DISTINCT payment_type_label
    FROM {DB_SCHEMA}.fct_trips
    WHERE payment_type_label IS NOT NULL
    ORDER BY payment_type_label
""")["payment_type_label"].tolist()

selected_payment_type = st.sidebar.selectbox(
    "Payment type",
    ["All"] + payment_types
)

if selected_payment_type == "All":
    WHERE_CLAUSE = ""
else:
    WHERE_CLAUSE = f"WHERE payment_type_label = '{selected_payment_type}'"


# -----------------------------
# Headline KPIs
# -----------------------------

st.subheader("Headline KPIs")

kpis = run_query(f"""
    SELECT
        COUNT(*) AS total_trips,
        AVG(trip_distance) AS avg_trip_distance,
        AVG(fare_per_mile) AS avg_fare_per_mile
    FROM {DB_SCHEMA}.fct_trips
    {WHERE_CLAUSE}
""").iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total trips",
    f"{int(kpis['total_trips']):,}"
)

col2.metric(
    "Average trip distance",
    f"{kpis['avg_trip_distance']:.2f} miles"
)

col3.metric(
    "Average fare per mile",
    f"${kpis['avg_fare_per_mile']:.2f}"
)


# -----------------------------
# Hour-of-day trend
# -----------------------------

st.subheader("Trips by pickup hour")

hourly = run_query(f"""
    SELECT
        EXTRACT(HOUR FROM pickup_datetime)::int AS pickup_hour,
        COUNT(*) AS trip_count
    FROM {DB_SCHEMA}.fct_trips
    {WHERE_CLAUSE}
    GROUP BY 1
    ORDER BY 1
""")

st.line_chart(hourly.set_index("pickup_hour"))


# -----------------------------
# Data freshness
# -----------------------------

st.subheader("Data freshness")

fresh = run_query(f"""
    SELECT
        COUNT(*) AS row_count,
        MAX(pickup_datetime) AS last_pickup
    FROM {DB_SCHEMA}.fct_trips
    {WHERE_CLAUSE}
""").iloc[0]

col1, col2 = st.columns(2)

col1.metric(
    "Row count",
    f"{int(fresh['row_count']):,}"
)

col2.metric(
    "Last pickup",
    str(fresh["last_pickup"])[:16]
)
