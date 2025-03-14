-- models/silver/fct_sales.sql
{{
    config(
        materialized='incremental',
        cluster_by=['transaction_date'],
        partition_by={
            'field': 'transaction_date', 
            'data_type': 'date'
        },
        dataset='silver'
    )
}}

WITH raw_transactions AS (
    SELECT
        *,
        PARSE_DATE('%m/%d/%Y', transaction_date) AS transaction_date,
        PARSE_DATE('%m/%d/%Y', stock_date) AS stock_date
    FROM {{ ref('raw_adworks_transactions') }}
    {% if is_incremental() %}
        WHERE PARSE_DATE('%m/%d/%Y', transaction_date) > (
            SELECT MAX(transaction_date) 
            FROM {{ this }}
        )
    {% endif %}
)

SELECT
    {{ dbt_utils.generate_surrogate_key([
        'transaction_date',
        'product_id',
        'customer_id',
        'store_id',
        'quantity'
    ]) }} AS transaction_key,
    parsed_transaction_date AS transaction_date,
    parsed_stock_date AS stock_date,
    product_id,
    customer_id,
    store_id,
    quantity
FROM 
    raw_transactions