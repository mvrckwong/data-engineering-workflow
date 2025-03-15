{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_key',
        partition_by={
            "field": "_valid_from", 
            "data_type": "timestamp", 
            "granularity": "day"
        },
        cluster_by=[
            'customer_id', 
            '_is_current'
        ],
        tags=['tests']
    )
}}
SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_id', 'dbt_valid_from']) }} AS customer_key,
    {{ dbt_utils.star(
        from=ref('snap_customers_adworks'),
        except=[
            'dbt_valid_from',
            'dbt_valid_to'
        ]
    ) }},
    
    -- metadata
    dbt_valid_from AS _valid_from,
    dbt_valid_to AS _valid_to,
    (dbt_valid_to IS NULL) AS _is_current,
    CURRENT_TIMESTAMP AS _last_updated

FROM {{ ref('snap_customers_adworks') }}

{% if is_incremental() %}
WHERE dbt_valid_from > (
    SELECT MAX(_valid_from) 
    FROM {{ this }}
)
{% endif %}