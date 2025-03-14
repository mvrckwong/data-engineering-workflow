{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='store_key',
        partition_by={
            "field": "valid_from", 
            "data_type": "timestamp", 
            "granularity": "day"
        },
        cluster_by=['store_key'],
        tags=['tests']
    )
}}

SELECT
    *
FROM 
    {{ ref('stg_stores_adworks') }}

{% if is_incremental() %}
    WHERE valid_from > (
        SELECT MAX(valid_from) 
        FROM {{ this }}
    )
{% endif %}