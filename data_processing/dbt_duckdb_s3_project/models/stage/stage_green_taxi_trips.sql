
select
    VendorID::SMALLINT as vendor_id,
    case
        when VendorID = 1 then 'Creative Mobile Technologies, LLC'
        when VendorID = 2 then 'VeriFone Inc.'
        else 'Unknown'
    end as vendor_description,

    lpep_pickup_datetime::TIMESTAMP as pickup_datetime,
    lpep_dropoff_datetime::TIMESTAMP as dropoff_datetime,
    Passenger_count::SMALLINT as passenger_count,
    Trip_distance::DOUBLE as trip_distance,
    PULocationID::INTEGER as pickup_location_id,
    DOLocationID::INTEGER as dropoff_location_id,

    RateCodeID::SMALLINT as rate_code_id,
    case
        when RateCodeID = 1 then 'Standard rate'
        when RateCodeID = 2 then 'JFK'
        when RateCodeID = 3 then 'Newark'
        when RateCodeID = 4 then 'Nassau or Westchester'
        when RateCodeID = 5 then 'Negotiated fare'
        when RateCodeID = 6 then 'Group ride'
        else 'Unknown'
    end as rate_code_description,

    Store_and_fwd_flag::VARCHAR as store_and_fwd_flag,
    case
        when Store_and_fwd_flag = 'Y' then 'Store and forward trip'
        when Store_and_fwd_flag = 'N' then 'Not a store and forward trip'
        else 'Unknown'
    end as store_and_fwd_description,

    Payment_type::SMALLINT as payment_type,
    case
        when Payment_type = 1 then 'Credit card'
        when Payment_type = 2 then 'Cash'
        when Payment_type = 3 then 'No charge'
        when Payment_type = 4 then 'Dispute'
        when Payment_type = 5 then 'Unknown'
        when Payment_type = 6 then 'Voided trip'
        else 'Unknown'
    end as payment_type_description,

    Fare_amount::DOUBLE as fare_amount,
    Extra::DOUBLE as extra_charges,
    MTA_tax::DOUBLE as mta_tax,
    Improvement_surcharge::DOUBLE as improvement_surcharge,
    Tip_amount::DOUBLE as tip_amount,
    Tolls_amount::DOUBLE as tolls_amount,
    Total_amount::DOUBLE as total_amount,
    Trip_type::SMALLINT as trip_type,
    case
        when Trip_type = 1 then 'Street-hail'
        when Trip_type = 2 then 'Dispatch'
        else 'Unknown'
    end as trip_type_description
from {{ source('de_research_s3','nyctaxi/*/green_tripdata_*') }}
