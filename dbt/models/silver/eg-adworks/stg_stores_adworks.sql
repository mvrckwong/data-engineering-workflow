{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='store_id',
        cluster_by=[
            'region_id', 
            'store_type', 
            'store_country'
        ],
        on_schema_change='sync_all_columns',
        tags=['eg']
    )
}}

-- insert general transformations here,
-- including joining, cleaning, type conversion, renaming
-- including testing, validation processes
-- workflow: raw -> silver -> snapshot -> gold

WITH source AS (
    SELECT
        *
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        {{ ref('raw_stores_adworks') }}
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
    store_id NOT IN (
        SELECT store_id 
        FROM {{ this }}
    )

{% endif %}