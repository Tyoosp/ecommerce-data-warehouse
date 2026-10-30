SELECT
    fo.order_purchase_timestamp::DATE AS sales_date,

    COUNT(DISTINCT fo.order_id) AS total_orders,

    COUNT(DISTINCT foi.product_id) AS total_products_sold,

    SUM(foi.price) AS total_product_revenue,

    SUM(foi.freight_value) AS total_freight_value,

    SUM(foi.total_item_value) AS total_sales_value,

    AVG(foi.price) AS average_item_price

FROM {{ ref('fact_orders') }} AS fo
INNER JOIN {{ ref('fact_order_items') }} AS foi
    ON fo.order_id = foi.order_id

GROUP BY fo.order_purchase_timestamp::DATE
ORDER BY sales_date
