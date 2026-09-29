select
    country_code,
    country,
    cast(year as integer) as year,
    indicator,
    cast(value as double) as value,
    source
from {{ source('google_trends', 'raw_google_trends') }}