SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.city AS customer_city,
    c.state AS customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date
FROM {{ ref('stg_orders') }} AS o
LEFT JOIN {{ ref('stg_customers') }} AS c
    ON o.customer_id = c.customer_id
