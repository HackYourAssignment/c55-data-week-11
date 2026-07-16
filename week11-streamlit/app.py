"""NYC Taxi metrics dashboard — Week 11 assignment starter.

Reads the Week 10 dbt mart ``fct_trips`` from Azure Postgres. The page
setup and the ``run_query`` caching helper are already wired up (same
pattern taught in "Building a Metrics Dashboard"). Your job: implement the
three TODO-stubbed KPI queries below with your own SQL, then (Required tier)
add the hour-of-day trend, freshness panel, and payment-type filter
described in the assignment brief.
"""

import os
from pathlib import Path

import pandas as pd
import sqlalchemy
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

POSTGRES_URL = os.environ.get("POSTGRES_URL", "").strip()
DB_SCHEMA = os.environ.get("DB_SCHEMA", "dev_yourname").strip()

if not POSTGRES_URL or "your-pg-host" in POSTGRES_URL:
    st.error("POSTGRES_URL is not configured correctly. Update the project .env file with your real database connection string.")
    st.stop()

st.set_page_config(page_title="NYC Taxi Metrics", layout="wide")
st.title("NYC Taxi Metrics")


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(POSTGRES_URL)
    with engine.connect() as conn:
        return pd.read_sql(sql, conn)


st.subheader("Headline KPIs")
KPIs= run_query(f"""
    SELECT
        COUNT(*) AS total_trips,
        AVG(trip_distance) AS avg_trip_distance,
        AVG(fare_amount / trip_distance) AS avg_fare_per_mile
    FROM {DB_SCHEMA}.fct_trips
""").iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", f"{KPIs['total_trips']:,}")
col2.metric("Avg Trip Distance (miles)", f"{KPIs['avg_trip_distance']:.2f}")
col3.metric("Avg Fare per Mile ($)", f"{KPIs['avg_fare_per_mile']:.2f}")


