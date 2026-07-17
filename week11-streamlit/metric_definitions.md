# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel. Copy this file to `metric_definitions.md` inside your `week11-streamlit/` folder and fill it in.

## Metabase panels

<!-- One block per Question: trip count by payment type, average fare per
     mile by dropoff borough, average trip duration by hour of day. -->

### Panel 1: Trip Count by Payment Type

- **Name**: trip_count_by_payment_type
- **Description**: Total number of taxi trips grouped by payment type. This metric shows which payment methods are most commonly used by passengers.
- **Calculation**: COUNT(*) grouped by payment_type_label.
- **Data source**: dev_baraah.fct_trips (dbt mart)
- **Refresh frequency**: Rebuilt once per day.

### Panel 2: Average Fare per Mile by Dropoff Borough

- **Name**: avg_fare_per_mile_by_dropoff_borough
- **Description**: Average fare earned per mile for taxi trips grouped by dropoff borough. This metric compares fare efficiency across boroughs.
- **Calculation**: AVG(fare_per_mile) grouped by dropoff_borough.
- **Data source**: dev_baraah.fct_trips (dbt mart)
- **Refresh frequency**: Rebuilt once per day.

### Panel 3: Average Trip Duration by Hour of Day

- **Name**: avg_trip_duration_by_hour
- **Description**: Average trip duration in minutes grouped by pickup hour. This metric helps identify how trip duration changes throughout the day.
- **Calculation**: AVG(EXTRACT(EPOCH FROM (dropoff_datetime - pickup_datetime)) / 60) grouped by EXTRACT(HOUR FROM pickup_datetime).
- **Data source**: dev_baraah.fct_trips (dbt mart)
- **Refresh frequency**: Rebuilt once per day.

## Streamlit panels

<!-- Headline KPIs panel: total trips, average trip distance, average
     fare per mile. -->

### Panel 1: Headline KPIs

- **Name**: taxi_headline_kpis
- **Description**: Displays the total trips, average trip distance, and average fare per mile.
- **Calculation**: COUNT(*), AVG(trip_distance), and AVG(fare_per_mile).
- **Data source**: dev_baraah.fct_trips (dbt mart)
- **Refresh frequency**: Rebuilt once per day.


### Panel 2: Trips by Hour of Day

- **Name**: trips_by_hour
- **Description**: Shows the number of taxi trips for each pickup hour.
- **Calculation**: COUNT(*) grouped by EXTRACT(HOUR FROM pickup_datetime).
- **Data source**: dev_baraah.fct_trips (dbt mart)
- **Refresh frequency**: Rebuilt once per day.

### Panel 3: Data Freshness

- **Name**: taxi_data_freshness
- **Description**: Shows the total number of rows and the latest pickup datetime to verify that the data is current.
- **Calculation**: COUNT(*) and MAX(pickup_datetime).
- **Data source**: dev_baraah.fct_trips (dbt mart)
- **Refresh frequency**: Rebuilt once per day.



<!-- Add more ### Panel blocks under either section if you build more (the Required tier adds
     an hour-of-day trend and a freshness panel to Streamlit; a Metabase date filter is Extra,
     bonus credit, not required). -->
