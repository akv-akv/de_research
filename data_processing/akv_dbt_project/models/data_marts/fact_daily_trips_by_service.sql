{{ config(
    materialized='external',
) }}

select
    yr,
    mth,
    pickup_datetime::date as pickup_date,
    service_type,
    count(*) as trip_count
from {{ ref('fact_trips') }}
group by 1,2,3,4