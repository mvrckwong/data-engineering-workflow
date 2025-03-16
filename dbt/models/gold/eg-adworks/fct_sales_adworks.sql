{{
    config(
        materialized = 'incremental',
        incremental_strategy='merge',
        unique_key = 'transaction_id',
        partition_by = {
            "field": "transaction_date",
            "data_type": "date"
        },
        cluster_by = [
            "store_id", 
            "product_id"
        ],
        on_schema_change='sync_all_columns',
        tags=['gold', 'sales']
    )
}}

WITH sales_data AS (
    SELECT
        transaction_id,
        transaction_date,
        stock_date,
        product_id,
        customer_id,
        store_id,
        quantity,
        _extrated_date
    FROM 
        {{ ref('stg_sales_adworks') }}
    
    {% if is_incremental() %}
        WHERE _extrated_date > (
            SELECT 
                MAX(_extrated_date) 
            FROM 
                {{ this }}
        )
    {% endif %}
),

-- Add date keys for efficient joins to date dimension
sales_with_date_keys AS (
    SELECT
        *,
        FORMAT_DATE('%Y%m%d', transaction_date) AS transaction_date_key,
        FORMAT_DATE('%Y%m%d', stock_date) AS stock_date_key
    FROM
        sales_data
)

SELECT
    -- Original transaction ID serves as a natural key
    transaction_id,
    
    -- Date information with keys for joining to date dimension
    transaction_date,
    transaction_date_key,
    stock_date,
    stock_date_key,
    
    -- Dimension IDs for joining directly to dimension tables
    -- BigQuery performs efficiently with these joins when properly clustered
    product_id,
    customer_id,
    store_id,
    
    -- Metrics
    quantity,
    
    -- Derived metrics (add more as needed)
    1 AS transaction_count,  -- Count of transactions

    _extrated_date,
FROM
    sales_with_date_keys