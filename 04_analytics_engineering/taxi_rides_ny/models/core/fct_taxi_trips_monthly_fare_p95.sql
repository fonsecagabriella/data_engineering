{{ config(materialized='table') }}  

WITH filtered_trips AS (
    SELECT 
        service_type,
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(MONTH FROM pickup_datetime) AS month,
        fare_amount
    FROM {{ ref('fact_trips') }}
    WHERE 
        fare_amount > 0 
        AND trip_distance > 0 
        AND payment_type_description IN ('Cash', 'Credit Card')
),

percentile_fares AS (
    SELECT 
        service_type,
        year,
        month,
        APPROX_QUANTILES(fare_amount, 100)[SAFE_OFFSET(97)] AS fare_p97,
        APPROX_QUANTILES(fare_amount, 100)[SAFE_OFFSET(95)] AS fare_p95,
        APPROX_QUANTILES(fare_amount, 100)[SAFE_OFFSET(90)] AS fare_p90
    FROM filtered_trips
    GROUP BY 1, 2, 3
)

SELECT * FROM percentile_fares
