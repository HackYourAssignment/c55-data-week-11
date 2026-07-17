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
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_baraah")

st.set_page_config(page_title="NYC Taxi Metrics", layout="wide")
st.title("NYC Taxi Metrics")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)

st.sidebar.header("Filters")

payment_query = f"""
SELECT DISTINCT payment_type_label
FROM {DB_SCHEMA}.fct_trips
ORDER BY payment_type_label;
"""

payment_df = run_query(payment_query)

payment_options = ["All"] + payment_df["payment_type_label"].tolist()

selected_payment = st.sidebar.selectbox(
    "Payment Type",
    payment_options
)

if selected_payment == "All":
    payment_filter = ""
else:
    payment_filter = f"WHERE payment_type_label = '{selected_payment}'"

st.subheader("Headline KPIs")

# TODO: query total trip count, average trip_distance, and average
# fare_per_mile from {DB_SCHEMA}.fct_trips through run_query(), then
# render three tiles side by side with st.columns(3) and .metric().
# This is deliberately not the total-trips/avg-fare/total-revenue trio
# from the chapter: trip_distance and fare_per_mile are different columns,
# so copying the chapter's SQL verbatim will not answer this.
# Query headline KPIs from fct_trips
kpi_query = f"""
SELECT
    COUNT(*) AS total_trips,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(fare_per_mile) AS avg_fare_per_mile
FROM {DB_SCHEMA}.fct_trips
{payment_filter};
"""

kpi_df = run_query(kpi_query)

total_trips = int(kpi_df["total_trips"].iloc[0])
avg_trip_distance = kpi_df["avg_trip_distance"].iloc[0]
avg_fare_per_mile = kpi_df["avg_fare_per_mile"].iloc[0]


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Trips",
        f"{total_trips:,}"
    )

with col2:
    st.metric(
        "Average Trip Distance",
        f"{avg_trip_distance:.2f} miles"
    )

with col3:
    st.metric(
        "Average Fare per Mile",
        f"${avg_fare_per_mile:.2f}"
    )

st.subheader("Trips by Hour of Day")

hour_query = f"""
SELECT
    EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour,
    COUNT(*) AS trip_count
FROM {DB_SCHEMA}.fct_trips
{payment_filter}
GROUP BY pickup_hour
ORDER BY pickup_hour;
"""

hour_df = run_query(hour_query)

hour_df["pickup_hour"] = hour_df["pickup_hour"].astype(int)

st.line_chart(
    hour_df.set_index("pickup_hour")["trip_count"]
)

st.subheader("Data Freshness")

freshness_query = f"""
SELECT
    COUNT(*) AS row_count,
    MAX(pickup_datetime) AS latest_pickup_datetime
FROM {DB_SCHEMA}.fct_trips
{payment_filter};
"""

freshness_df = run_query(freshness_query)

row_count = int(freshness_df["row_count"].iloc[0])
latest_pickup = freshness_df["latest_pickup_datetime"].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Rows in fct_trips",
        f"{row_count:,}"
    )

with col2:
    st.metric(
        "Latest Pickup Datetime",
        str(latest_pickup)
    )
