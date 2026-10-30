SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,

    p.product_category_name,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,

    s.zip_code_prefix AS seller_zip_code_prefix,
    s.city AS seller_city,
    s.state AS seller_state,

    oi.shipping_limit_date,
    oi.price,
    oi.freight_value

FROM {{ ref('stg_order_items') }} AS oi

LEFT JOIN {{ ref('stg_products') }} AS p
    ON oi.product_id = p.product_id

LEFT JOIN {{ ref('stg_sellers') }} AS s
    ON oi.seller_id = s.seller_id
