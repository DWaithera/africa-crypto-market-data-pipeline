select
    country_code,
    country,
    indicator_code,
    indicator_name,
    year,
    value,
    source,
    cast(extracted_at as timestamp) as extracted_at
from {{ source('world_bank', 'raw_world_bank_indicators') }}