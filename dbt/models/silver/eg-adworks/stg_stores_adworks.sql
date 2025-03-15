{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='store_key',
        tags=['eg']
    )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['store_id', 'dbt_valid_from']) }} AS store_key,
    {{ dbt_utils.star(
        from=ref('snap_stores_adworks'),
        except=[
            'dbt_valid_from',
            'dbt_valid_to'
        ]
    ) }},

    -- SCD columns
    dbt_valid_from AS _valid_from,
    dbt_valid_to AS _valid_to,
    (dbt_valid_to IS NULL) AS _is_current
FROM 
    {{ ref('snap_stores_adworks') }}