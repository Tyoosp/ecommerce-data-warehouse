SELECT
    dc.customer_unique_id,
    dc.city AS customer_city,
    dc.state AS customer_state,

    COUNT(DISTINCT fo.order_id) AS total_orders,

    MIN(fo.order_purchase_timestamp::DATE) AS first_order_date,

    MAX(fo.order_purchase_timestamp::DATE) AS last_order_date,

    SUM(COALESCE(foi.price, 0)) AS total_spending,

    AVG(order_values.order_value) AS average_order_value,

    CASE
        WHEN COUNT(DISTINCT fo.order_id) = 1
            THEN 'One-time Customer'
        WHEN COUNT(DISTINCT fo.order_id) BETWEEN 2 AND 3
            THEN 'Repeat Customer'
        ELSE 'Loyal Customer'
    END AS customer_segment

FROM {{ ref('dim_customer') }} AS dc

INNER JOIN {{ ref('fact_orders') }} AS fo
    ON dc.customer_id = fo.customer_id

LEFT JOIN {{ ref('fact_order_items') }} AS foi
    ON fo.order_id = foi.order_id

LEFT JOIN (
    SELECT
        order_id,
        SUM(price) AS order_value
    FROM {{ ref('fact_order_items') }}
    GROUP BY order_id
) AS order_values
    ON fo.order_id = order_values.order_id

GROUP BY
    dc.customer_unique_id,
    dc.city,
    dc.state
