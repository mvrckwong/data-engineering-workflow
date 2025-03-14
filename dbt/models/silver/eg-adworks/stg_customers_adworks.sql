{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_key',
        dataset='silver',
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

    -- SCD columns
    dbt_valid_from AS valid_from,
    dbt_valid_to AS valid_to,
    (dbt_valid_to IS NULL) AS is_current
FROM 
    {{ ref('snap_customers_adworks') }}