SELECT
    product_id,
    NULLIF(TRIM(product_category_name), '') AS product_category_name,
    product_name_lenght,
    product_description_lenght,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm,
    ingested_at
FROM {{ source('raw', 'products') }}

