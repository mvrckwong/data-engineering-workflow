{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=[
            'transaction_date', 
            'product_id', 
            'customer_id', 
            'store_id'
        ],
        cluster_by=[
            'product_id', 
            'customer_id'
        ],
        on_schema_change='sync_all_columns',
        tags=['sales_fact'],
        enabled=false
    )
}}

WITH source AS (
    SELECT
        *
    FROM 
        {{ ref('raw_sales_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        -- Use parsed transaction_date for incremental loads
        PARSE_DATE('%m/%d/%Y', transaction_date) > (
            SELECT 
                MAX(transaction_date) 
            FROM 
                {{ this }}
        )
    {% endif %}
),

transformed_source AS (
    SELECT
        -- Parse and standardize dates
        CAST(PARSE_DATE('%m/%d/%Y', transaction_date) AS DATE) AS transaction_date
        , CAST(PARSE_DATE('%m/%d/%Y', stock_date) AS DATE) AS stock_date
        
        -- Standardize IDs as integers
        , CAST(product_id AS INT64) AS product_id
        , CAST(customer_id AS INT64) AS customer_id
        , CAST(store_id AS INT64) AS store_id
        , CAST(quantity AS INT64) AS quantity
        
        -- Metadata
        , CURRENT_TIMESTAMP() AS _extracted_at
    FROM 
        source
    WHERE
        transaction_date IS NOT NULL
        AND product_id IS NOT NULL
        AND customer_id IS NOT NULL
        AND store_id IS NOT NULL
)

SELECT 
    * 
FROM 
    transformed_source