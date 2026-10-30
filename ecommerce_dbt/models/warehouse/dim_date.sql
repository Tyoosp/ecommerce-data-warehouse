WITH date_spine AS (

    SELECT
        generate_series(
            DATE '2016-01-01',
            DATE '2018-12-31',
            INTERVAL '1 day'
        )::DATE AS date_day

)

SELECT
    date_day,
    EXTRACT(YEAR FROM date_day)::INTEGER AS year,
    EXTRACT(QUARTER FROM date_day)::INTEGER AS quarter,
    EXTRACT(MONTH FROM date_day)::INTEGER AS month,
    TO_CHAR(date_day, 'Month') AS month_name,
    EXTRACT(WEEK FROM date_day)::INTEGER AS week_of_year,
    EXTRACT(DAY FROM date_day)::INTEGER AS day_of_month,
    EXTRACT(DOW FROM date_day)::INTEGER AS day_of_week,
    TO_CHAR(date_day, 'Day') AS day_name,
    CASE
        WHEN EXTRACT(DOW FROM date_day) IN (0, 6)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM date_spine
