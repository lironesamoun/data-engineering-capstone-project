{{ config(materialized="table") }}


select
    eventid as event_id,
    case when iday != 0 then cast(concat(iyear, '-', imonth, '-', iday) as date) else null end as event_date,
    country_txt as country,
    region_txt as region,
    provstate,
    city,
    summary,
    cast(crit1 as integer) as reason1,
    cast(crit2 as integer) as reason2,
    cast(crit3 as integer) as reason3,
    cast(doubtterr as integer) as doubt_terrorism_proper,
    attacktype1_txt as attack_type,
    targtype1_txt as target_type,
    weaptype1_txt as weapon_type,
    gname as perpetrator_group_name,
    cast(nkill as integer) as nkill,
    cast(nwound as integer) as nwound,
    cast(ishostkid as integer) as ishostkid,
    cast(nhostkid as integer) as nhostkid
from {{ source("staging", "data") }}

{% if var("is_test_run", default=true) %} limit 100 {% endif %}
