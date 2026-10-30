SELECT
    TRIM(product_category_name) AS product_category_name,
    TRIM(product_category_name_english) AS product_category_name_english,
    ingested_at
FROM {{ source('raw', 'product_category_translation') }}
