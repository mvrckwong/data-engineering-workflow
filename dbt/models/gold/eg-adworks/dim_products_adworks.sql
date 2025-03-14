{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='product_key',
        partition_by={
            "field": "_valid_from", 
            "data_type": "timestamp", 
            "granularity": "day"
        },
        cluster_by=['product_key'],
        tags=['tests']
    )
}}

SELECT
    *
FROM 
    {{ ref('stg_products_adworks') }}

{% if is_incremental() %}
    WHERE _valid_from > (
        SELECT MAX(_valid_from) 
        FROM {{ this }}
    )
{% endif %}