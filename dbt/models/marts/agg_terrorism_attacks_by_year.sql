{{ config(materialized='table') }}

with global_terrorism_data as (
    select * from {{ ref('global_terrorism_data_with_countries_codes') }}
)

SELECT
   count(*) as num_attacks,
   FORMAT_DATE('%Y', event_date_year) as event_year
FROM
  global_terrorism_data
GROUP BY 
  2
ORDER BY 
  num_attacks DESC