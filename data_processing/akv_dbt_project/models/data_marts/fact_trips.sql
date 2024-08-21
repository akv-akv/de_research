{{ config(
    materialized='external',
    options={"partition_by": "yr, mth",
        "overwrite_or_ignore": true
    }
) }}

with yellow_taxi_stage as (
    select
        year(pickup_datetime) as yr,
        month(pickup_datetime) as mth,
        'yellow_taxi' as service_type,
        vendor_id,
        vendor_description,
        pickup_datetime,
        dropoff_datetime,
        passenger_count,
        trip_distance,
        pickup_location_id,
        dropoff_location_id,
        rate_code_id,
        rate_code_description,
        store_and_fwd_flag,
        store_and_fwd_description,
        payment_type,
        payment_type_description,
        fare_amount,
        extra_charges,
        mta_tax,
        improvement_surcharge,
        tip_amount,
        tolls_amount,
        total_amount,
        congestion_surcharge,
        airport_fee,
        NULL::SMALLINT as trip_type,
        NULL::VARCHAR as trip_type_description
    from {{ ref('stage_yellow_taxi_trips') }} -- Replace with your yellow taxi stage model reference
),

green_taxi_stage as (
    select
        year(pickup_datetime) as yr,
        month(pickup_datetime) as mth,
        'green_taxi' as service_type,
        vendor_id,
        vendor_description,
        pickup_datetime,
        dropoff_datetime,
        passenger_count,
        trip_distance,
        pickup_location_id,
        dropoff_location_id,
        rate_code_id,
        rate_code_description,
        store_and_fwd_flag,
        store_and_fwd_description,
        payment_type,
        payment_type_description,
        fare_amount,
        extra_charges,
        mta_tax,
        improvement_surcharge,
        tip_amount,
        tolls_amount,
        total_amount,
        NULL::DOUBLE as congestion_surcharge,
        NULL::DOUBLE as airport_fee,
        trip_type,
        trip_type_description
    from {{ ref('stage_green_taxi_trips') }} -- Replace with your green taxi stage model reference
),

fhvhv_stage as (
    select
        year(pickup_datetime) as yr,
        month(pickup_datetime) as mth,
        'fhvhv' as service_type,
        NULL::SMALLINT as vendor_id,
        NULL::VARCHAR as vendor_description,
        pickup_datetime,
        dropoff_datetime,
        NULL::SMALLINT as passenger_count,
        trip_miles as trip_distance,
        pickup_location_id,
        dropoff_location_id,
        NULL::SMALLINT as rate_code_id,
        NULL::VARCHAR as rate_code_description,
        NULL::VARCHAR as store_and_fwd_flag,
        NULL::VARCHAR as store_and_fwd_description,
        NULL::SMALLINT as payment_type,
        NULL::VARCHAR as payment_type_description,
        base_passenger_fare as fare_amount,
        NULL::DOUBLE as extra_charges,
        NULL::DOUBLE as mta_tax,
        NULL::DOUBLE as improvement_surcharge,
        tips as tip_amount,
        tolls as tolls_amount,
        base_passenger_fare + tolls + congestion_surcharge + airport_fee + tips as total_amount,
        congestion_surcharge,
        airport_fee,
        NULL::SMALLINT as trip_type,
        NULL::VARCHAR as trip_type_description
    from {{ ref('stage_fhvhv_trips') }} -- Replace with your FHvhV stage model reference
)

select * from yellow_taxi_stage
union all
select * from green_taxi_stage
union all
select * from fhvhv_stage