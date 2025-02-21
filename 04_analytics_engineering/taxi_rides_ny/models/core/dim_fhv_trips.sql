{{
    config(
        materialized='table'
    )
}}

WITH base_trips AS (
    SELECT 
        tripid,
        dispatching_base_num,
        pickup_datetime,
        dropoff_datetime,
        year,
        month,
        pickup_locationid,
        dropoff_locationid,
        sr_flag,
        affiliated_base_number
    FROM {{ ref('stg_fhv_trips') }}
)

SELECT
    bt.tripid,
    bt.dispatching_base_num,
    bt.pickup_datetime,
    bt.dropoff_datetime,
    bt.year,
    bt.month,

    -- Pickup location details
    bt.pickup_locationid,
    pz.borough AS pickup_borough,
    pz.zone AS pickup_zone,
    pz.service_zone AS pickup_service_zone,

    -- Dropoff location details
    bt.dropoff_locationid,
    dz.borough AS dropoff_borough,
    dz.zone AS dropoff_zone,
    dz.service_zone AS dropoff_service_zone,

    bt.sr_flag,
    bt.affiliated_base_number

FROM base_trips bt
LEFT JOIN {{ ref('dim_zones') }} pz ON bt.pickup_locationid = pz.locationid
LEFT JOIN {{ ref('dim_zones') }} dz ON bt.dropoff_locationid = dz.locationid
