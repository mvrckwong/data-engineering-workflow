{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='region_id',
        cluster_by=[
            'sales_district', 
            'sales_region'
        ],
        on_schema_change='sync_all_columns',
        tags=['eg'],
        enabled=false
    )
}}

WITH source AS (
    SELECT
        *
    FROM 
        {{ ref('raw_regions_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        -- This assumes your source data has an updated_at or similar field
        -- Change the field name to match your actual data
        -- updated_at > (
        --     SELECT MAX(updated_at) 
        --     FROM {{ this }}
        -- )
        
        -- Alternatively, if you don't have an updated_at field:
        region_id NOT IN (
            SELECT region_id 
            FROM {{ this }}
        )
    {% endif %}
),

transformed_source AS (
    SELECT
        CAST(region_id AS INT64) AS region_id
        , sales_district
        , sales_region
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        source
)

SELECT 
    * 
FROM 
    transformed_source