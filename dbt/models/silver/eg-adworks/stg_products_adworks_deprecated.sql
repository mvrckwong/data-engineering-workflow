{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='product_id',
        cluster_by=[
            'product_brand'
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
        {{ ref('raw_products_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        -- This assumes your source data has an updated_at or similar field
        -- Change the field name to match your actual data
        -- updated_at > (
        --     SELECT MAX(updated_at) 
        --     FROM {{ this }}
        -- )
        
        -- Alternatively, if you don't have an updated_at field:
        product_id NOT IN (
            SELECT product_id 
            FROM {{ this }}
        )
    {% endif %}
),

transformed_source AS (
    SELECT
        CAST(product_id AS INT64) AS product_id
        , product_brand
        , product_name
        , product_sku
        , CAST(product_retail_price AS FLOAT64) AS product_retail_price
        , CAST(product_cost AS FLOAT64) AS product_cost
        , CAST(product_weight AS FLOAT64) AS product_weight
        , CASE WHEN CAST(recyclable AS STRING) = '1' THEN TRUE ELSE FALSE END AS is_recyclable
        , CASE WHEN CAST(low_fat AS STRING) = '1' THEN TRUE ELSE FALSE END AS is_low_fat
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        source
)

SELECT 
    * 
FROM 
    transformed_source