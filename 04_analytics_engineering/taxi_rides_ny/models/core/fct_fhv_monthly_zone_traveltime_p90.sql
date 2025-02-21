{{ config(materialized='table') }}

WITH trip_durations AS (
    SELECT 
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(MONTH FROM pickup_datetime) AS month,
        pickup_locationid,
        dropoff_locationid,
        TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, SECOND) AS trip_duration
    FROM {{ ref('dim_fhv_trips') }}
    WHERE 
        pickup_datetime IS NOT NULL 
        AND dropoff_datetime IS NOT NULL
        AND pickup_locationid IS NOT NULL
        AND dropoff_locationid IS NOT NULL
),

p90_travel_time AS (
    SELECT 
        year,
        month,
        pickup_locationid,
        dropoff_locationid,
        PERCENTILE_CONT(trip_duration, 0.90) OVER (
            PARTITION BY year, month, pickup_locationid, dropoff_locationid
        ) AS travel_time_p90
    FROM trip_durations
)

SELECT DISTINCT 
    year, 
    month, 
    pickup_locationid, 
    dropoff_locationid, 
    travel_time_p90
FROM p90_travel_time