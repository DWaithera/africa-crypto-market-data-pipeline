/*
    MEPS Chainalysis staging model.

    Purpose:
        Standardize the raw Chainalysis Crypto Adoption Index
        data for downstream MEPS feature engineering.

    Important:
        The raw adoption rank is preserved.
        No normalization or scoring occurs in staging.
*/

with source_data as (

    select
        country_code,
        country,
        cast(year as integer) as year,
        indicator,
        cast(value as integer) as crypto_adoption_rank,
        source,
        source_dataset

    from {{ source('chainalysis', 'raw_chainalysis_crypto_adoption') }}

)

select
    country_code,
    country,
    year,
    indicator,
    crypto_adoption_rank,
    source,
    source_dataset

from source_data