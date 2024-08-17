{{ config(
    materialized='external'
) }}

select
    round(trip_distance),
    passenger_count,
    count(*)
from {{ source('de_research_s3','nyctaxi/*/yellow_tripdata_*') }}
group by 1,2
order by 3 desc