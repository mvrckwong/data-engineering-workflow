{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_id',
        on_schema_change='sync_all_columns',
        tags=['eg']
    )
}}

-- insert general transformations here,
-- including joining, cleaning, type conversion, renaming
-- including testing, validation processes

WITH source AS (
    SELECT
        *
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        {{ ref('raw_customers_adworks') }}
)

SELECT 
    * 
FROM 
    source

{% if is_incremental() %}

WHERE
    -- This assumes your source data has an updated_at or similar field
    -- Change the field name to match your actual data
    -- updated_at > (
    --     SELECT MAX(updated_at) 
    --     FROM {{ this }}
    -- )
    
    -- Alternatively, if you don't have an updated_at field:
    customer_id NOT IN (
        SELECT customer_id 
        FROM {{ this }}
    )

{% endif %}