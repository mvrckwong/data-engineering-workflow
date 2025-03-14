{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_key',
        partition_by={
            "field": "valid_from",
            "data_type": "timestamp",
            "granularity": "day"
        },
        cluster_by=['customer_id', 'is_current'],
        dataset='gold'
    )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} as customer_key,
    {{ dbt_utils.star(
        from=ref('stg_adworks_customers_snapshot'),
        except=['dbt_valid_from', 'dbt_valid_to']
    ) }},
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
    (dbt_valid_to is null) as is_current
FROM 
    {{ ref('stg_adworks_customers_snapshot') }}

{% if is_incremental() %}
    WHERE dbt_valid_from > (
        SELECT max(valid_from) 
        FROM {{ this }}
    )
{% endif %}