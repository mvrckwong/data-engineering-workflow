{{
    config(
        materialized='incremental',
        unique_key='region_key',
        dataset='silver',
        tags=['tests']
    )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['region_id', 'dbt_valid_from']) }} AS region_key,
    {{ dbt_utils.star(
        from=ref('snap_regions_adworks'),
        except=[
            'dbt_valid_from',
            'dbt_valid_to'
        ]
    ) }},

    -- SCD columns
    dbt_valid_from AS valid_from,
    dbt_valid_to AS valid_to,
    (dbt_valid_to IS NULL) AS is_current
FROM 
    {{ ref('snap_regions_adworks') }}