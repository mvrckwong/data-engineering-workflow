{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='region_key',
        partition_by={
            "field": "valid_from", 
            "data_type": "timestamp", 
            "granularity": "day"
        },
        cluster_by=['region_key'],
        tags=['tests']
    )
}}

SELECT
    *
FROM 
    {{ ref('stg_regions_adworks') }}

{% if is_incremental() %}
    WHERE valid_from > (
        SELECT MAX(valid_from) 
        FROM {{ this }}
    )
{% endif %}