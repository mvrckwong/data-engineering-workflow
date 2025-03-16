{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='return_key',
        partition_by={
            "field": "return_date",
            "data_type": "date",
            "granularity": "day",
        },
        cluster_by=[
            'product_id',
            'store_id',
        ],
        on_schema_change='sync_all_columns'
    )
}}

WITH source AS (
    SELECT
        {{ dbt_utils.star(from=ref('stg_returns_adworks')) }}
    FROM 
        {{ ref('stg_returns_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        return_date > (
            SELECT MAX(return_date) 
            FROM {{ this }}
        )
    {% endif %}
),

transformed_data AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(
            ['return_date', 'product_id', 'store_id', 'quantity']
        ) }} AS return_key
        
        -- All return fact columns
        , {{ dbt_utils.star(
            from=ref('stg_returns_adworks'), 
            relation_alias='r', 
            except=['_extracted_at']
        ) }}
        
        -- Foreign keys to dimensions
        , {{ dbt_utils.generate_surrogate_key(['product_id']) }} AS product_key
        , {{ dbt_utils.generate_surrogate_key(['store_id']) }} AS store_key
        
        -- Metadata
        , _extracted_at
    FROM 
        source r
),

metrics AS (
    SELECT
        t.*
        
        -- Business metrics calculations
        , CASE
            WHEN EXTRACT(DAYOFWEEK FROM return_date) IN (1, 7) THEN 'Weekend'
            ELSE 'Weekday'
          END AS day_type
        , EXTRACT(MONTH FROM return_date) AS return_month
        , EXTRACT(YEAR FROM return_date) AS return_year
    FROM 
        transformed_data t
)

SELECT 
    * 
FROM 
    metrics