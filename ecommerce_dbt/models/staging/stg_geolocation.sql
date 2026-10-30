SELECT
    geolocation_zip_code_prefix AS zip_code_prefix,
    geolocation_lat AS latitude,
    geolocation_lng AS longitude,
    TRIM(geolocation_city) AS city,
    UPPER(TRIM(geolocation_state)) AS state,
    ingested_at
FROM {{ source('raw', 'geolocation') }}
