{{ config(materialized='table') }}

with global_terrorism_data as (
    select * from {{ ref('global_terrorism_data_with_countries_codes') }}
)

SELECT
   count(*) as num_attacks,
   FORMAT_DATE('%Y-%m', event_date_month) as event_month,
   country
FROM
  global_terrorism_data
GROUP BY 
  2, 3
ORDER BY 
  num_attacks DESC