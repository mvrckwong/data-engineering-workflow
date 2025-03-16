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
-- workflow: raw -> silver -> snapshot -> gold
WITH source AS (
    SELECT
        *
    FROM 
        {{ ref('raw_stores_adworks') }}
    
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
),
transformed_source AS (
    SELECT
        CAST(store_id AS INT64) AS store_id
        , CAST(region_id AS INT64) AS region_id
        , store_type
        , store_name
        , store_street_address
        , store_city
        , store_state
        , store_country
        , store_phone
        , PARSE_DATE('%m/%d/%Y', first_opened_date) AS first_opened_date
        , PARSE_DATE('%m/%d/%Y', last_remodel_date) AS last_remodel_date
        , CAST(total_sqft AS INT64) AS total_sqft
        , CAST(grocery_sqft AS INT64) AS grocery_sqft
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        source
)
SELECT 
    * 
FROM 
    transformed_source