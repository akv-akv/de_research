{{ config(
    materialized='external',
    location='s3://de_research/dbt_duckdb/processed/result.csv') }}

select count(*) from {{ source('s3_raw_data','csv_raw_table') }}
