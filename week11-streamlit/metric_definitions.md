# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel. Copy this file to `metric_definitions.md` inside your `week11-streamlit/` folder and fill it in.

## Metabase panels

<!-- One block per Question: trip count by payment type, average fare per
     mile by dropoff borough, average trip duration by hour of day. -->

### Panel 1: 

- **Name**: Trip count by payment type
- **Description**: Helps identify which payment type is preffered
- **Calculation**: sum of payments grouped by type of payment
- **Data source**: fct_trips
- **Refresh frequency**: every time fct_trips is built

### Panel 2: 

- **Name**: Average fare per mile by dropoff borough
- **Description**: Helps show the average money paid per mile in every borough
- **Calculation**: finding the average of of fare paid by mile and grouping per borough
- **Data source**: the fct_trips
- **Refresh frequency**: every time fct_trips is built

### Panel 3: 

- **Name**: Average trip duration per hour
- **Description**: Shows which hours are busiest by average
- **Calculation**: we deduct the pickup time time from dropoff time and then find average
- **Data source**: fct_trips
- **Refresh frequency**: every time fct_trips is run

## Streamlit panels

<!-- Headline KPIs panel: total trips, average trip distance, average
     fare per mile. -->

### Panel 1: 

- **Name**: Headline KPIs
- **Description**: total trips,average_trip distance,average fare per mile
- **Calculation**:  COUNT(*) AS total_trips,
        AVG(trip_distance) AS avg_trip_distance,
        AVG(fare_per_mile) AS avg_fare_per_mile
- **Data source**: fct_trips
- **Refresh frequency**: when data is cached

<!-- Add more ### Panel blocks under either section if you build more (the Required tier adds
     an hour-of-day trend and a freshness panel to Streamlit; a Metabase date filter is Extra,
     bonus credit, not required). -->
