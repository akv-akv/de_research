{{ config(materialized='external', location='s3://de_research/dbt_duckdb/processed/result.csv') }}
select count(*)
from {{ source('my_source','actual_data_raw') }}
