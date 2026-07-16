# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel. Copy this file to `metric_definitions.md` inside your `week11-streamlit/` folder and fill it in.

## Metabase panels


### Panel 1: Trip count

- **Name**: Trip count by payment type
- **Description**: bar chart to understand which payment methods are most popular among riders.
Y axis is trip count, X axis is payment type
- **Calculation**: `COUNT(*)` grouped by `payment_type_label` where `payment_type_label IS NOT NULL`
- **Data source**: dev_bader.fct_trips
- **Refresh frequency**: once per day

### Panel 2: Average fare

- **Name**: Average Fare per Mile by Dropoff Borough
- **Description**: Identify which destinations have the highest average fares per mile
X is dropoff borough and Y is average fare per mile
- **Calculation**: `AVG(fare_per_mile)` grouped by `dropoff_borough` where `dropoff_borough IS NOT NULL`
- **Data source**: dev_bader.fct_trips
- **Refresh frequency**: once per day

### Panel 3: Average trip duration

- **Name**: Average Trip Duration by hour of day
- **Description**: Track how the average trip length in minutes during hours of the day
X axis and Y are hours of the day,  Line is the average trip duration in minutes
- **Calculation**: `AVG((dropoff_datetime - pickup_datetime) in minutes)` grouped by `EXTRACT(HOUR FROM pickup_datetime)`
- **Data source**: dev_bader.fct_trips
- **Refresh frequency**: once per day

## Streamlit panels


### Panel 1: Headline KPIs

- **Name**: Total Trips, Average Trip Distance, Average Fare per Mile
- **Description**: Count of trips, mean trip distance, and mean fare per mile
- **Calculation**: `count(*)`, `avg(trip_distance)`, `avg(fare_per_mile)`
- **Data source**: `dev_bader.fct_trips`
- **Refresh frequency**: 5 min cache (`ttl=300`)

### Panel 2: Trips by Hour of Day

- **Name**: Trip Count by Pickup Hour
- **Description**: Trip count grouped by hour of day
- **Calculation**: `count(*) group by extract(hour from pickup_datetime)`
- **Data source**: `dev_bader.fct_trips`
- **Refresh frequency**: 5 min cache (`ttl=300`)

### Panel 3: Data Freshness

- **Name**: Row Count, Latest Pickup Timestamp
- **Description**: Total rows and most recent pickup timestamp
- **Calculation**: `count(*)`, `max(pickup_datetime)`
- **Data source**: `dev_bader.fct_trips`
- **Refresh frequency**: 5 min cache (`ttl=300`)