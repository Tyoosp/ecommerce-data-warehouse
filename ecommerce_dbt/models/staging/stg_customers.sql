SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix AS zip_code_prefix,
    TRIM(customer_city) AS city,
    UPPER(TRIM(customer_state)) AS state,
    ingested_at
FROM {{ source('raw', 'customers') }}

