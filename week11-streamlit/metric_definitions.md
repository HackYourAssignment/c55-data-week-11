# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel. Copy this file to `metric_definitions.md` inside your `week11-streamlit/` folder and fill it in.

## Metabase panels

<!-- One block per Question: trip count by payment type, average fare per
     mile by dropoff borough, average trip duration by hour of day. -->

### Panel 1: Trip Count by Payment Type

- **Name**: `trip_count_by_payment_type`
- **Description**: Number of taxi trips grouped by payment type. This shows which payment methods are used most often in the dataset.
- **Calculation**: `COUNT(*)` grouped by `payment_type_label`
- **Data source**: `dev_halyna.fct_trips`
- **Refresh frequency**: Updated when the `fct_trips` mart is rebuilt. Metabase reads the current database table when the dashboard is opened.

### Panel 2: Average Fare per Mile by Dropoff Borough

- **Name**: `avg_fare_per_mile_by_dropoff_borough`
- **Description**: Average fare charged per mile, grouped by the borough where the trip ended. Unit: US dollars per mile.
- **Calculation**: `AVG(fare_per_mile)` grouped by `dropoff_borough`
- **Data source**: `dev_halyna.fct_trips`
- **Refresh frequency**: Updated when the `fct_trips` mart is rebuilt. Metabase reads the current database table when the dashboard is opened.

### Panel 3: Average Trip Duration by Hour

- **Name**: `avg_trip_duration_by_pickup_hour`
- **Description**: Average trip duration in minutes, grouped by pickup hour of day. This shows how trip duration changes during the day.
- **Calculation**: `AVG(EXTRACT(EPOCH FROM (dropoff_datetime - pickup_datetime)) / 60)` grouped by `EXTRACT(HOUR FROM pickup_datetime)`
- **Data source**: `dev_halyna.fct_trips`
- **Refresh frequency**: Updated when the `fct_trips` mart is rebuilt. Metabase reads the current database table when the dashboard is opened.

## Streamlit panels

<!-- Headline KPIs panel: total trips, average trip distance, average
     fare per mile. -->

### Panel 1: Headline KPIs

- **Name**: `headline_kpis`
- **Description**: Three headline metrics for the selected payment type: total trips, average trip distance, and average fare per mile.
- **Calculation**:
  - `total_trips`: `COUNT(*)`
  - `avg_trip_distance`: `AVG(trip_distance)`
  - `avg_fare_per_mile`: `AVG(fare_per_mile)`
  - If a payment type is selected, the query adds `WHERE payment_type_label = selected_payment_type`.
- **Data source**: `dev_halyna.fct_trips`
- **Refresh frequency**: Streamlit caches the query result for 300 seconds using `@st.cache_data(ttl=300)`. The underlying data updates when the `fct_trips` mart is rebuilt.

### Panel 2: Trips by Pickup Hour

- **Name**: `trip_count_by_pickup_hour`
- **Description**: Number of taxi trips grouped by pickup hour of day. This shows the daily demand pattern across the 24-hour cycle.
- **Calculation**: `COUNT(*)` grouped by `EXTRACT(HOUR FROM pickup_datetime)`. If a payment type is selected, the query adds `WHERE payment_type_label = selected_payment_type`.
- **Data source**: `dev_halyna.fct_trips`
- **Refresh frequency**: Streamlit caches the query result for 300 seconds using `@st.cache_data(ttl=300)`. The underlying data updates when the `fct_trips` mart is rebuilt.

### Panel 3: Data Freshness

- **Name**: `data_freshness`
- **Description**: Data-quality panel showing the number of rows available and the latest pickup timestamp in the selected dataset.
- **Calculation**:
  - `row_count`: `COUNT(*)`
  - `last_pickup`: `MAX(pickup_datetime)`
  - If a payment type is selected, the query adds `WHERE payment_type_label = selected_payment_type`.
- **Data source**: `dev_halyna.fct_trips`
- **Refresh frequency**: Streamlit caches the query result for 300 seconds using `@st.cache_data(ttl=300)`. The underlying data updates when the `fct_trips` mart is rebuilt.

<!-- Add more ### Panel blocks under either section if you build more (the Required tier adds
     an hour-of-day trend and a freshness panel to Streamlit; a Metabase date filter is Extra,
     bonus credit, not required). -->
