# Metric definitions

Five fields per metric: Name, Description, Calculation, Data source, Refresh frequency. One block per panel.

## Metabase panels

### Panel 1: Trip Count by Payment Type

- **Name**: Trip Count by Payment Type
- **Description**: The number of NYC taxi trips recorded for each payment type. This metric shows which payment methods are used most frequently and highlights less common payment categories.
- **Calculation**: Count all rows in `fct_trips`, grouped by `payment_type_label`: `COUNT(*) GROUP BY payment_type_label`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Metabase Question or dashboard is refreshed. The underlying data changes when the dbt mart is rebuilt.

### Panel 2: Average Fare per Mile by Dropoff Borough

- **Name**: Average Fare per Mile by Dropoff Borough
- **Description**: The average fare per mile for trips ending in each dropoff borough. It compares normalized trip costs across destinations and includes the `Unknown` and `NaN` location categories present in the mart.
- **Calculation**: Calculate `AVG(fare_per_mile)` for all trips, grouped by `dropoff_borough`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database. The `fare_per_mile` field is calculated in the dbt mart from fare amount and trip distance.
- **Refresh frequency**: Recalculated when the Metabase Question or dashboard is refreshed. The underlying data changes when the dbt mart is rebuilt.

### Panel 3: Average Trip Duration by Hour of Day

- **Name**: Average Trip Duration by Hour of Day
- **Description**: The average duration in minutes of trips grouped by their pickup hour. It shows how average journey duration changes throughout the day.
- **Calculation**: For every trip, calculate duration as `EXTRACT(EPOCH FROM (dropoff_datetime - pickup_datetime)) / 60`. Average the result and group it by `EXTRACT(HOUR FROM pickup_datetime)`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Metabase Question or dashboard is refreshed. The underlying data changes when the dbt mart is rebuilt.

## Streamlit panels

The selected `payment_type_label` filter is applied to every Streamlit metric.
When `All` is selected, no payment-type filter is applied.

### Panel 1: Headline KPIs

#### Metric 1: Total Trips

- **Name**: Total Trips
- **Description**: The total number of taxi trips in the current payment-type selection.
- **Calculation**: Count all rows after applying the selected payment-type filter: `COUNT(*)`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Streamlit app reruns or the filter changes. Query results are cached for up to five minutes, and the underlying data changes when the dbt mart is rebuilt.

#### Metric 2: Average Trip Distance

- **Name**: Average Trip Distance
- **Description**: The average trip distance in miles for trips in the current payment-type selection.
- **Calculation**: Calculate `AVG(trip_distance)` after applying the selected payment-type filter.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Streamlit app reruns or the filter changes. Query results are cached for up to five minutes, and the underlying data changes when the dbt mart is rebuilt.

#### Metric 3: Average Fare per Mile
- **Name**: Average Fare per Mile
- **Description**: The average fare charged per mile for trips in the current payment-type selection.
- **Calculation**: Calculate `AVG(fare_per_mile)` after applying the selected payment-type filter.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database. The `fare_per_mile` field is calculated in the dbt mart from fare amount and trip distance.
- **Refresh frequency**: Recalculated when the Streamlit app reruns or the filter changes. Query results are cached for up to five minutes, and the underlying data changes when the dbt mart is rebuilt.

### Panel 2: Trips by Hour of Day

#### Metric 4: Trip Count by Pickup Hour
- **Name**: Trip Count by Pickup Hour
- **Description**: The number of trips beginning during each hour of the day for the current payment-type selection. It shows daily demand patterns across the 24-hour period.
- **Calculation**: Extract the hour from `pickup_datetime`, count rows, and group by pickup hour: `COUNT(*) GROUP BY EXTRACT(HOUR FROM pickup_datetime)`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Streamlit app reruns or the filter changes. Query results are cached for up to five minutes, and the underlying data changes when the dbt mart is rebuilt.

### Panel 3: Data Freshness

#### Metric 5: Row Count
- **Name**: Row Count
- **Description**: The number of rows currently available in `fct_trips` for the selected payment type. It provides a basic completeness check and should match Total Trips for the same selection.
- **Calculation**: Count all rows after applying the selected payment-type filter: `COUNT(*)`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Streamlit app reruns or the filter changes. Query results are cached for up to five minutes, and the underlying data changes when the dbt mart is rebuilt.

#### Metric 6: Latest Pickup Datetime
- **Name**: Latest Pickup Datetime
- **Description**: The most recent pickup timestamp represented in the current payment-type selection. It indicates how far the dataset extends in event time, but it is not the timestamp of the latest pipeline run.
- **Calculation**: Select the maximum pickup timestamp after applying the selected payment-type filter: `MAX(pickup_datetime)`.
- **Data source**: `dev_pavel_tisner.fct_trips` in the Azure PostgreSQL `team1` database.
- **Refresh frequency**: Recalculated when the Streamlit app reruns or the filter changes. Query results are cached for up to five minutes, and the underlying data changes when the dbt mart is rebuilt.
