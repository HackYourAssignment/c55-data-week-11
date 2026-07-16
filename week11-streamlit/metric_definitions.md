# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel. Copy this file to `metric_definitions.md` inside your `week11-streamlit/` folder and fill it in.

## Metabase panels

<!-- One block per Question: trip count by payment type, average fare per
     mile by dropoff borough, average trip duration by hour of day. -->

### Panel 1: Trip Count by Payment Type

- **Name**: Trip Count by Payment Type
- **Description**: Displays the total number of taxi trips grouped by their payment method (e.g., Credit card, Cash, Dispute, etc.) to understand customer payment preferences. Missing or null values are classified explicitly as "Not Recorded" or "Unknown".
- **Calculation**: $$\text{Trip Count} = \text{COUNT}(*)$$Categorized using a CASE WHEN statement mapping payment_type codes (1 to 6) to their official descriptions, grouping by this category, and sorting in descending order.
- **Data source**: dev_mareh.vw_fact_trips
- **Refresh frequency**: Daily (or upon ETL pipeline execution)

### Panel 2: Average Fare per Mile by Dropoff Borough

- **Name**: Average Fare per Mile by Dropoff Borough
- **Description**: Visualizes the average cost of a taxi ride per mile based on where passengers are dropped off (Dropoff Borough). This helps identify which destinations yield the highest fare rates relative to the distance traveled.
- **Calculation**: $$\text{Average Fare per Mile} = \text{AVG}\left(\frac{\text{fare\_amount}}{\text{trip\_distance}}\right)$$Note: A conditional check ($\text{trip\_distance} > 0$) is implemented to prevent division-by-zero errors.
- **Data source**: Joined tables dev_mareh.vw_fact_trips (fact) and dev_mareh.vw_dim_zones (dimension) on location IDs.
- **Refresh frequency**: Daily (or upon ETL pipeline execution)

### Panel 3: Average Trip Duration by Hour of Day

- **Name**: Average Trip Duration by Hour of Day
- **Description**: A line chart illustrating how the average duration of taxi trips (in minutes) fluctuates across different hours of the day (from 0 to 23). This highlights peak traffic congestion hours and off-peak travel times.
- **Calculation**: $$\text{Trip Duration (Minutes)} = \frac{\text{EXTRACT}(\text{EPOCH FROM } (\text{dropoff\_datetime} - \text{pickup\_datetime}))}{60}$$
$$\text{Average Trip Duration} = \text{AVG}(\text{Trip Duration})$$Grouped by $\text{EXTRACT}(\text{HOUR FROM } \text{pickup\_datetime})$ and sorted chronologically.
- **Data source**: dev_mareh.vw_fact_trips
- **Refresh frequency**: Daily (or upon ETL pipeline execution)

## Streamlit panels

## Streamlit panels

### Panel 1: Headline KPIs

- **Name**: Headline KPIs (Total Trips, Avg Trip Distance, Avg Fare per Mile)
- **Description**: Shows three main numbers to understand how many rides happened, how long they were on average, and the average cost for each mile.
- **Calculation**: 
  - `total_trips`: `COUNT(*)` (Total number of rides).
  - `avg_trip_distance`: `AVG(trip_distance)` (Average distance of a single ride, measured in miles).
  - `avg_fare_per_mile`: `AVG(CASE WHEN trip_distance > 0 THEN fare_amount / trip_distance ELSE 0 END)` (Calculates the cost per mile for each ride first, then finds the average of those rates. It safely ignores rides with zero distance).
- **Data source**: `dev_mareh.vw_fact_trips`
- **Refresh frequency**: Daily / Whenever the database is updated.

### Panel 2: Trip Count by Hour of Day

- **Name**: Hourly Trip Distribution
- **Description**: A line chart that shows the number of rides for every hour of the day (from 0 to 23) to see when the busiest times are.
- **Calculation**: `COUNT(*)` grouped by the hour of the ride start time using `EXTRACT(HOUR FROM pickup_datetime)`.
- **Data source**: `dev_mareh.vw_fact_trips`
- **Refresh frequency**: Daily / Whenever the database is updated.

### Panel 3: Data Freshness Status

- **Name**: Data Freshness and Row Count
- **Description**: Shows the total number of rows in the database and the time of the very last ride to make sure our data is up-to-date and not missing anything.
- **Calculation**: 
  - `total_rows`: `COUNT(*)` (Total rows in the table).
  - `latest_pickup`: `MAX(pickup_datetime)` (The timestamp of the newest ride recorded).
- **Data source**: `dev_mareh.vw_fact_trips`
- **Refresh frequency**: Daily / Whenever the database is updated.