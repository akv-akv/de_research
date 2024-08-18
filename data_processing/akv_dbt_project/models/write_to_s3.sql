{{ config(
    materialized='external'
) }}

select
    year(pickup_datetime),
    count(*)
from {{ ref('stage_fhvhv_trips') }}
group by 1
order by 2 desc
