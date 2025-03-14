{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='product_key',
        partition_by={
            "field": "valid_from",
            "data_type": "timestamp",
            "granularity": "day"
        },
        cluster_by=['product_id', 'is_current'],
        dataset='gold'
    )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['product_id', 'dbt_valid_from']) }} as product_key,
    {{ dbt_utils.star(
        from=ref('stg_adworks_products_snapshot'),
        except=['dbt_valid_from', 'dbt_valid_to']
    ) }},
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
    (dbt_valid_to is null) as is_current
FROM 
    {{ ref('stg_adworks_products_snapshot') }}

{% if is_incremental() %}
    WHERE dbt_valid_from > (
        SELECT max(valid_from) 
        FROM {{ this }}
    )
{% endif %}