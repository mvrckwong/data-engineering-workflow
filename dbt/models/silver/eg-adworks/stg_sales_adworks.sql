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
            "store_id", "product_id"
        ],
        on_schema_change='sync_all_columns',
        tags=['eg']
    )
}}

WITH source AS (
    SELECT
        CONCAT(
            FORMAT_DATE('%Y%m%d', PARSE_DATE('%m/%d/%Y', transaction_date)),
            '-',
            product_id,
            '-', 
            customer_id,
            '-',
            store_id
        ) AS transaction_id
        , PARSE_DATE('%m/%d/%Y', transaction_date) AS transaction_date
        , PARSE_DATE('%m/%d/%Y', stock_date) AS stock_date
        , CAST(product_id AS INT64) AS product_id
        , CAST(customer_id AS INT64) AS customer_id
        , CAST(store_id AS INT64) AS store_id
        , CAST(quantity AS INT64) AS quantity
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        {{ ref('raw_sales_adworks') }}
    
    {% if is_incremental() %}
        WHERE PARSE_DATE('%m/%d/%Y', transaction_date) > (
            SELECT 
                MAX(transaction_date) 
            FROM 
                {{ this }}
        )
    {% endif %}
)

SELECT 
    * 
FROM 
    source