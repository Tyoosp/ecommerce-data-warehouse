SELECT
    ds.seller_id,
    ds.city AS seller_city,
    ds.state AS seller_state,

    COUNT(*) AS total_items_sold,

    COUNT(DISTINCT foi.order_id) AS total_orders,

    COUNT(DISTINCT foi.product_id) AS total_products,

    SUM(foi.price) AS total_product_revenue,

    SUM(foi.freight_value) AS total_freight_value,

    SUM(foi.total_item_value) AS total_sales_value,

    AVG(foi.price) AS average_item_price

FROM {{ ref('dim_seller') }} AS ds

INNER JOIN {{ ref('fact_order_items') }} AS foi
    ON ds.seller_id = foi.seller_id

GROUP BY
    ds.seller_id,
    ds.city,
    ds.state
