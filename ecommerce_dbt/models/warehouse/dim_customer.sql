SELECT
    customer_unique_id,
    MIN(customer_id) AS customer_id,
    MIN(zip_code_prefix) AS zip_code_prefix,
    MIN(city) AS city,
    MIN(state) AS state

FROM {{ ref('stg_customers') }}

GROUP BY customer_unique_id
