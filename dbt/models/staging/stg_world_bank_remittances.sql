select
    country_code,
    country,
    indicator_code,
    indicator_name,
    year,
    cast(value as double) as value,
    source
from {{ source('world_bank_remittances', 'raw_world_bank_remittances') }}