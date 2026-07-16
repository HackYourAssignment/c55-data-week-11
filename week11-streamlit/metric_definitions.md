# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel. Copy this file to `metric_definitions.md` inside your `week11-streamlit/` folder and fill it in.

## Metabase panels

<!-- One block per Question: trip count by payment type, average fare per
     mile by dropoff borough, average trip duration by hour of day. -->

### Panel 1: Trip Count by Payment Type

- **Name**: Trip Count by Payment Type
- **Description**: Number of taxi trips grouped by payment method. Missing payment labels are shown as Unknown.
- **Calculation**: Count all rows using COUNT(\*), grouped by COALESCE(payment_type_label, 'Unknown').
- **Data source**: fct_trips in the Week 10 development schema; field payment_type_label.
- **Refresh frequency**: After every successful refresh of the Week 10 dbt mart.

### Panel 2: Average fare per mile by dropoff borough

- **Name**: Average fare per mile by dropoff borough
- **Description**: Average fare charged per mile for trips ending in each borough. Missing dropoff boroughs are shown as Unknown.
- **Calculation**: AVG(fare_per_mile) grouped by COALESCE(dropoff_borough, 'Unknown'); null fare_per_mile values are excluded by the average.
- **Data source**: fct_trips in the Week 10 development schema; fields fare_per_mile and dropoff_borough.
- **Refresh frequency**: After every successful refresh of the Week 10 dbt mart.

### Panel 3: Average trip duration by hour of day

- **Name**: Average trip duration by hour of day
- **Description**: Average trip duration in minutes grouped by the pickup hour from 0 through 23
- **Calculation**: Average of EXTRACT(EPOCH FROM (dropoff_datetime - pickup_datetime)) / 60, grouped by EXTRACT(HOUR FROM pickup_datetime). Trips with missing timestamps or negative durations are excluded.
- **Data source**: fct_trips in the Week 10 development schema; fields pickup_datetime and dropoff_datetime.
- **Refresh frequency**: After every successful refresh of the Week 10 dbt mart.

## Streamlit panels

<!-- Headline KPIs panel: total trips, average trip distance, average
     fare per mile. -->

### Panel 1: Headline KPIs

- **Name**: Headline trip KPIs
- **Description**: Shows total trips, average trip distance in miles, and average fare per mile. Results are recalculated for the selected payment type.
- **Calculation**: COUNT(\*), AVG(trip_distance), and AVG(fare_per_mile). When a payment type is selected, rows are filtered using payment_type_label before aggregation.
- **Data source**: fct_trips in the schema configured by DB_SCHEMA; fields trip_distance, fare_per_mile, and payment_type_label.

- **Refresh frequency**: After every successful dbt mart refresh; Streamlit query results can remain cached for up to five minutes.

<!-- Add more ### Panel blocks under either section if you build more (the Required tier adds
     an hour-of-day trend and a freshness panel to Streamlit; a Metabase date filter is Extra,
     bonus credit, not required). -->

### Panel 2: Trip count by hour of day

- **Name**: Trip count by hour of day
- **Description**: Shows the number of trips beginning during each hour from 0 through 23. Results follow the selected payment-type filter.
- **Calculation**: COUNT(\*) grouped by EXTRACT(HOUR FROM pickup_datetime).
- **Data source**: fct_trips in the schema configured by DB_SCHEMA; fields pickup_datetime and payment_type_label.

- **Refresh frequency**: After every successful dbt mart refresh; Streamlit query results can remain cached for up to five minutes.

### Panel 3: Data freshness

- **Name**: Trip-data freshness
- **Description**: Shows the number of rows and newest pickup timestamp in the current payment-type selection. The timestamp indicates data coverage and is not the pipeline execution time.
- **Calculation**: COUNT(\*) for row count and MAX(pickup_datetime) for the newest trip.
- **Data source**: fct_trips in the schema configured by DB_SCHEMA; fields pickup_datetime and payment_type_label.

- **Refresh frequency**: After every successful dbt mart refresh; Streamlit query results can remain cached for up to five minutes.
