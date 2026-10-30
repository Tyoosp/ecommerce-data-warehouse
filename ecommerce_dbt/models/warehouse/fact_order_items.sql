SELECT
    oi.order_id,
    oi.order_item_id,

    oi.product_id,
    oi.seller_id,

    oi.shipping_limit_date,

    oi.price,
    oi.freight_value,

    oi.price + oi.freight_value AS total_item_value

FROM {{ ref('int_order_items_enriched') }} AS oi
