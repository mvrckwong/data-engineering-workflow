{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='customer_id',
        cluster_by=[
            'member_card', 
            'customer_country'
        ],
        on_schema_change='sync_all_columns',
        tags=['eg'],
        enabled=false
    )
}}

WITH source AS (
    SELECT
        *
    FROM 
        {{ ref('raw_customers_adworks') }}
    
    {% if is_incremental() %}
    WHERE
        -- This assumes your source data has an updated_at or similar field
        -- Change the field name to match your actual data
        -- updated_at > (
        --     SELECT MAX(updated_at) 
        --     FROM {{ this }}
        -- )
        
        -- Alternatively, if you don't have an updated_at field:
        customer_id NOT IN (
            SELECT customer_id 
            FROM {{ this }}
        )
    {% endif %}
),

transformed_source AS (
    SELECT
        CAST(customer_id AS INT64) AS customer_id
        , customer_acct_num
        , first_name
        , last_name
        , customer_address
        , customer_city
        , customer_state_province
        , customer_postal_code
        , customer_country
        , PARSE_DATE('%m/%d/%Y', birthdate) AS birthdate
        , marital_status
        , yearly_income
        , gender
        , CAST(total_children AS INT64) AS total_children
        , CAST(num_children_at_home AS INT64) AS num_children_at_home
        , education
        , PARSE_DATE('%m/%d/%Y', acct_open_date) AS acct_open_date
        , member_card
        , occupation
        , CASE WHEN homeowner = 'Y' THEN TRUE ELSE FALSE END AS is_homeowner
        , CURRENT_TIMESTAMP() AS _extrated_date
    FROM 
        source
)

SELECT 
    * 
FROM 
    transformed_source