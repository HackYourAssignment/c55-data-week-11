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


def get_engine() -> sqlalchemy.engine.Engine:
    return sqlalchemy.create_engine(POSTGRES_URL)


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn)

    # Sidebar filter — applies to every panel below


# ---------------------------------------------------------------------------
payment_options = ["All"] + run_query(f"""
    select distinct payment_type_label
    from {DB_SCHEMA}.fct_trips
    where payment_type_label is not null
    order by payment_type_label
""")["payment_type_label"].tolist()

selected_payment = st.sidebar.selectbox("Payment type", payment_options)

where_clause = (
    ""
    if selected_payment == "All"
    else f"where payment_type_label = '{selected_payment}'"
)


st.subheader("Headline KPIs")
kpis = run_query(f"""
    SELECT COUNT(*)          AS trip_count,
           AVG(fare_amount)  AS avg_fare,
           SUM(fare_amount)  AS total_fare
    FROM {DB_SCHEMA}.fct_trips
""").iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total trips", f"{int(kpis['trip_count']):,}")
col2.metric("Average fare", f"${kpis['avg_fare']:.2f}")
col3.metric("Total revenue", f"${kpis['total_fare']:,.0f}")

st.subheader("Trips by Hour of Day")

hour_df = run_query(f"""
    select
        extract(hour from pickup_datetime)::int as pickup_hour,
        count(*) as trip_count
    from {DB_SCHEMA}.fct_trips
    {where_clause}
    group by 1
    order by 1
""")

if hour_df.empty:
    st.info("No trips found for this filter.")
else:
    hour_df = hour_df.set_index("pickup_hour").reindex(range(24), fill_value=0)
    st.line_chart(hour_df["trip_count"])


# ---------------------------------------------------------------------------
# Freshness panel
# ---------------------------------------------------------------------------

st.subheader("Data freshness")
fresh = run_query(f"""
    SELECT COUNT(*)              AS row_count,
           MAX(pickup_datetime)  AS last_pickup
    FROM {DB_SCHEMA}.fct_trips
""").iloc[0]

col1, col2 = st.columns(2)
col1.metric("Row count", f"{int(fresh['row_count']):,}")
col2.metric(
    "Last pickup", str(fresh["last_pickup"])[:16] if fresh["last_pickup"] else "unknown"
)


# TODO: query total trip count, average trip_distance, and average
# fare_per_mile from {DB_SCHEMA}.fct_trips through run_query(), then
# render three tiles side by side with st.columns(3) and .metric().
# This is deliberately not the total-trips/avg-fare/total-revenue trio
# from the chapter: trip_distance and fare_per_mile are different columns,
# so copying the chapter's SQL verbatim will not answer this.
