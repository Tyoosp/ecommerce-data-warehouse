SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value,
    ingested_at
FROM {{ source('raw', 'order_items') }}
