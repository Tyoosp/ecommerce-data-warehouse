SELECT
    seller_id,
    seller_zip_code_prefix AS zip_code_prefix,
    TRIM(seller_city) AS city,
    UPPER(TRIM(seller_state)) AS state,
    ingested_at
FROM {{ source('raw', 'sellers') }}
