{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=[
            'return_date', 
            'product_id', 
            'store_id'
        ],
        cluster_by=[
            'product_id', 
            'store_id'
        ],
        on_schema_change='sync_all_columns'
    )
}}

WITH source AS (
    SELECT
        *
    FROM 
        {{ ref('raw_returns_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        -- Use parsed return_date for incremental loads
        PARSE_DATE('%m/%d/%Y', return_date) > (
            SELECT 
                MAX(return_date) 
            FROM 
                {{ this }}
        )
    {% endif %}
),

transformed_source AS (
    SELECT
        -- Parse and standardize dates
        CAST(PARSE_DATE('%m/%d/%Y', return_date) AS DATE) AS return_date
        
        -- Standardize IDs as integers
        , CAST(product_id AS INT64) AS product_id
        , CAST(store_id AS INT64) AS store_id
        , CAST(quantity AS INT64) AS quantity
        
        -- Metadata
        , CURRENT_TIMESTAMP() AS _extracted_at
    FROM 
        source
    WHERE
        return_date IS NOT NULL
        AND product_id IS NOT NULL
        AND store_id IS NOT NULL
)

SELECT 
    * 
FROM 
    transformed_source