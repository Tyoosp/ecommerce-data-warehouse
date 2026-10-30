SELECT
    p.order_id,
    p.total_payment_value,
    p.max_payment_installments,
    p.payment_count

FROM {{ ref('int_order_payments') }} AS p

