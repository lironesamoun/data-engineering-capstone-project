{{ config(materialized='table') }}

select 
    id,
    upper(alpha2) as alpha2,
    upper(alpha3) as alpha3,
    name
from
{{ ref('countries_codes_seed') }}
