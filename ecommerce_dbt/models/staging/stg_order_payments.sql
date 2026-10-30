SELECT
    order_id,
    payment_sequential,
    LOWER(TRIM(payment_type)) AS payment_type,
    payment_installments,
    payment_value,
    ingested_at
FROM {{ source('raw', 'order_payments') }}
