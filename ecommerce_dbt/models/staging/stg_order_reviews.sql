SELECT
    review_id,
    order_id,
    review_score,
    NULLIF(TRIM(review_comment_title), '') AS review_comment_title,
    NULLIF(TRIM(review_comment_message), '') AS review_comment_message,
    review_creation_date,
    review_answer_timestamp,
    ingested_at
FROM {{ source('raw', 'order_reviews') }}
