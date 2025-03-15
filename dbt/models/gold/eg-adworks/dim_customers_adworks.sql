{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_key',
        on_schema_change='sync_all_columns',
        partition_by={
            "field": "_valid_from", 
            "data_type": "timestamp", 
            "granularity": "day"
        },
        cluster_by=[
            'customer_key', 
            '_is_current'
        ],
        tags=['eg']
    )
}}

WITH source AS (
    SELECT
        {{ dbt_utils.star(from=ref('snap_customers_adworks')) }}, 
        (dbt_valid_to IS NULL) AS is_current
    FROM 
        {{ ref('snap_customers_adworks') }}
    
    {% if is_incremental() %}
    WHERE dbt_valid_from > (
        SELECT MAX(_valid_from) 
        FROM {{ this }}
    )
    {% endif %}
)

-- Final dimension table with enriched attributes
SELECT
    {{ dbt_utils.generate_surrogate_key(['s.customer_id', 's.dbt_valid_from']) }} AS customer_key,
    {{ dbt_utils.star(
        from=ref('snap_customers_adworks'), 
        relation_alias='s', 
        except=['dbt_valid_from', 'dbt_valid_to']
    ) }},
    
    -- SCD metadata
    s.dbt_valid_from AS _valid_from,
    s.dbt_valid_to AS _valid_to,
    s.is_current AS _is_current

FROM source s