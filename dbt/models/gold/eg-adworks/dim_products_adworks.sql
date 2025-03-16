{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='product_key',
        on_schema_change='sync_all_columns',
        partition_by={
            "field": "_valid_from"
            , "data_type": "timestamp"
            , "granularity": "day"
        },
        cluster_by=[
            'product_brand'
        ],
        tags=['eg']
    )
}}

WITH source AS (
    SELECT
        {{ dbt_utils.star(from=ref('snap_products_adworks')) }}
        , (dbt_valid_to IS NULL) AS is_current
    FROM 
        {{ ref('snap_products_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        dbt_valid_from > (
            SELECT MAX(_valid_from) 
            FROM {{ this }}
        )
    {% endif %}
),

-- Final dimension table with enriched attributes
final AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(
            ['s.product_id', 's.dbt_valid_from']
        ) }} AS product_key
        , {{ dbt_utils.star(
            from=ref('snap_products_adworks'), 
            relation_alias='s', 
            except=['dbt_valid_from', 'dbt_valid_to']
        ) }}
        
        -- SCD metadata
        , s.dbt_valid_from AS _valid_from
        , s.dbt_valid_to AS _valid_to
        , s.is_current AS _is_current
    FROM 
        source s
)

SELECT 
    * 
FROM 
    final