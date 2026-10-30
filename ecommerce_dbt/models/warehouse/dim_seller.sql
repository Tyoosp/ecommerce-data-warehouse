SELECT
    seller_id,
    zip_code_prefix,
    city,
    state

FROM {{ ref('stg_sellers') }}
