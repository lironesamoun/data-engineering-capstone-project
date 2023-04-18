{{ config(materialized='table') }}

with countries_codes as (
    select * 
    from {{ ref('countries_codes') }}
),

global_terrorism_data as (
    select *
    from {{ ref('stg_parquet_globalterrorism') }}
)

select * ,
upper(countries_codes.alpha2) as iso_code_alpha2,
upper(countries_codes.alpha3) as iso_code_alpha3
from global_terrorism_data
inner join countries_codes
on global_terrorism_data.country = countries_codes.name