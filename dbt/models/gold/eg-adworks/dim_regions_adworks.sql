{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='region_key',
        partition_by={
            "field": "_valid_from", 
            "data_type": "timestamp", 
            "granularity": "day"
        },
        cluster_by=['region_key'],
        tags=['eg']
    )
}}

SELECT
    *
FROM 
    {{ ref('stg_regions_adworks') }}

{% if is_incremental() %}
    WHERE _valid_from > (
        SELECT MAX(_valid_from) 
        FROM {{ this }}
    )
{% endif %}