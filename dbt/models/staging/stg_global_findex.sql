select
    country_code,
    country,
    cast(year as integer) as year,
    series,
    indicator,
    cast(value as double) as value,
    source
from {{ source('global_findex', 'raw_global_findex') }}