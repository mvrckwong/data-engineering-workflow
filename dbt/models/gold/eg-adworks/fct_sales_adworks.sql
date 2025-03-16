{{
    config(
        materialized='incremental'
        , incremental_strategy='merge'
        , unique_key='transaction_key'
        , partition_by={
            "field": "transaction_date"
            , "data_type": "date"
            , "granularity": "day"
        }
        , cluster_by=[
            'product_id'
            , 'customer_id'
            , 'store_id'
        ]
        , on_schema_change='sync_all_columns'
        , tags=['sales_fact']
    )
}}

WITH source AS (
    SELECT
        {{ dbt_utils.star(from=ref('stg_sales_adworks')) }}
    FROM 
        {{ ref('stg_sales_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        transaction_date > (
            SELECT MAX(transaction_date) 
            FROM {{ this }}
        )
    {% endif %}
),

transformed_data AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(
            ['transaction_date', 'product_id', 'customer_id', 'store_id', 'quantity']
        ) }} AS transaction_key
        
        -- All transaction fact columns
        , {{ dbt_utils.star(
            from=ref('stg_sales_adworks'), 
            relation_alias='s', 
            except=['_extracted_at']
        ) }}
        
        -- Foreign keys to dimensions
        , {{ dbt_utils.generate_surrogate_key(['product_id']) }} AS product_key
        , {{ dbt_utils.generate_surrogate_key(['customer_id']) }} AS customer_key
        , {{ dbt_utils.generate_surrogate_key(['store_id']) }} AS store_key
        
        -- Metadata
        , _extracted_at
    FROM 
        source s
),

metrics AS (
    SELECT
        t.*
        
        -- Business metrics calculations
        , DATE_DIFF(transaction_date, stock_date, DAY) AS days_in_stock
        , CASE
            WHEN EXTRACT(DAYOFWEEK FROM transaction_date) IN (1, 7) THEN 'Weekend'
            ELSE 'Weekday'
          END AS day_type
    FROM 
        transformed_data t
)

SELECT 
    * 
FROM 
    metrics