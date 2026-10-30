SELECT
    dp.product_id,
    dp.product_category_name,
    dp.product_category_name_english,

    COUNT(*) AS total_items_sold,

    COUNT(DISTINCT foi.order_id) AS total_orders,

    SUM(foi.price) AS total_product_revenue,

    SUM(foi.freight_value) AS total_freight_value,

    SUM(foi.total_item_value) AS total_sales_value,

    AVG(foi.price) AS average_product_price

FROM {{ ref('dim_product') }} AS dp

INNER JOIN {{ ref('fact_order_items') }} AS foi
    ON dp.product_id = foi.product_id

GROUP BY
    dp.product_id,
    dp.product_category_name,
    dp.product_category_name_english
