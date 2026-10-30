SELECT
    o.order_id,
    o.customer_id,
    o.customer_unique_id,

    o.order_status,

    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN (
            o.order_delivered_customer_date::DATE
            - o.order_purchase_timestamp::DATE
        )
        ELSE NULL
    END AS delivery_days,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
         AND o.order_delivered_customer_date
             <= o.order_estimated_delivery_date
        THEN TRUE
        WHEN o.order_delivered_customer_date IS NOT NULL
        THEN FALSE
        ELSE NULL
    END AS delivered_on_time

FROM {{ ref('int_orders_enriched') }} AS o
