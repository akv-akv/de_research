select
    Hvfhs_license_num::VARCHAR as hvfhs_license_num,
    case
        when Hvfhs_license_num = 'HV0002' then 'Juno'
        when Hvfhs_license_num = 'HV0003' then 'Uber'
        when Hvfhs_license_num = 'HV0004' then 'Via'
        when Hvfhs_license_num = 'HV0005' then 'Lyft'
        else 'Unknown'
    end as hvfhs_license_description,

    Dispatching_base_num::VARCHAR as dispatching_base_num,
    Pickup_datetime::TIMESTAMP as pickup_datetime,
    DropOff_datetime::TIMESTAMP as dropoff_datetime,
    PULocationID::INTEGER as pickup_location_id,
    DOLocationID::INTEGER as dropoff_location_id,
    originating_base_num::VARCHAR as originating_base_num,
    request_datetime::TIMESTAMP as request_datetime,
    on_scene_datetime::TIMESTAMP as on_scene_datetime,
    trip_miles::DOUBLE as trip_miles,
    trip_time::INTEGER as trip_time,
    base_passenger_fare::DOUBLE as base_passenger_fare,
    tolls::DOUBLE as tolls,
    bcf::DOUBLE as bcf,
    sales_tax::DOUBLE as sales_tax,
    congestion_surcharge::DOUBLE as congestion_surcharge,
    airport_fee::DOUBLE as airport_fee,
    tips::DOUBLE as tips,
    driver_pay::DOUBLE as driver_pay

from {{ source('de_research_s3','nyctaxi/*/fhvhv_tripdata_*') }}
where Pickup_datetime >= '{{ var('start_date') }}'::timestamp
    and Pickup_datetime < '{{ var('end_date') }}'::timestamp
