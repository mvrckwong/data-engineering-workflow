{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_id',
        tags=['tests']
    )
}}

-- insert general transformations here,
-- including joining, cleaning, type conversion, renaming
-- including testing, validation processes

SELECT
    *
FROM 
    {{ ref('raw_customers_adworks') }}