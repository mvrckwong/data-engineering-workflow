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
        cluster_by=['store_id', 'is_current'],
        dataset='gold'
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['store_id', 'dbt_valid_from']) }} as store_key,
    {{ dbt_utils.star(
        from=ref('stg_adworks_stores_snapshot'),
        except=['dbt_valid_from', 'dbt_valid_to']
    ) }},
    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,
    (dbt_valid_to is null) as is_current
from {{ ref('stg_adworks_stores_snapshot') }}

{% if is_incremental() %}
    where dbt_valid_from > (select max(valid_from) from {{ this }})
{% endif %}