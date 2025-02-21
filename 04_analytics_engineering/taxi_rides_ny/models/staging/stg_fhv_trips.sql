{{ config(materialized='view') }}

SELECT 
    pickup_datetime,
    dropoff_datetime,
    PULocationID,
    DOLocationID,
    dispatching_base_num
FROM {{ source('your_source_dataset', 'fhv_tripdata_2019') }}
WHERE dispatching_base_num IS NOT NULL
