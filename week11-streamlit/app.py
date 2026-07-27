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
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_hannahwn")

st.set_page_config(page_title="NYC Taxi Metrics", layout="wide")
st.title("NYC Taxi Metrics")




@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)

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
    where_clause = ""
else:
    where_clause = f"WHERE payment_type_label = '{selected_payment_type}'"


st.subheader("Headline KPIs")
KPIs= run_query(f"""
    SELECT
        COUNT(*) AS total_trips,
        AVG(trip_distance) AS avg_trip_distance,
        AVG(fare_per_mile) AS avg_fare_per_mile
    FROM {DB_SCHEMA}.fct_trips
    {where_clause}
""").iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", f"{KPIs['total_trips']:,}")
col2.metric("Avg Trip Distance (miles)", f"{KPIs['avg_trip_distance']:.2f}")
col3.metric("Avg Fare per Mile ($)", f"{KPIs['avg_fare_per_mile']:.2f}")




st.subheader("Trip Distance Distribution")
hourly_dist = run_query(f"""
    SELECT
        EXTRACT(HOUR FROM pickup_datetime) AS hour_of_day,
        COUNT(*) AS trip_count
    FROM {DB_SCHEMA}.fct_trips
    GROUP BY 1
    ORDER BY 1
""")

if hourly_dist.empty:
    st.warning("No data available for the selected filters.")
else:
    st.bar_chart(hourly_dist.set_index("hour_of_day")["trip_count"])


st.subheader("Data Freshness")
freshness = run_query(f"""
    SELECT
        MAX(pickup_datetime) AS last_pickup,
        MAX(dropoff_datetime) AS last_dropoff
    FROM {DB_SCHEMA}.fct_trips
""").iloc[0]    

col1, col2 = st.columns(2)

col1.metric("Row count", f"{KPIs['total_trips']:,}")
col2.metric(
    "Last pickup", str(freshness["last_pickup"])[:16] if freshness["last_pickup"] else "unknown"
)

