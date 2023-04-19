{{ config(materialized='table') }}

with countries_codes as (
    select * 
    from {{ ref('countries_codes') }}
),

global_terrorism_data as (
    select *
    from {{ ref('stg_parquet_globalterrorism') }}
)

select * 
from global_terrorism_data
inner join countries_codes
on global_terrorism_data.country = countries_codes.name