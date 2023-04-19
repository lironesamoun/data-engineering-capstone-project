{{ config(materialized='table') }}

select 
    id,
    upper(alpha2) as iso_code_alpha2,
    upper(alpha3) as iso_code_alpha3,
    name
from
{{ ref('countries_codes_seed') }}
