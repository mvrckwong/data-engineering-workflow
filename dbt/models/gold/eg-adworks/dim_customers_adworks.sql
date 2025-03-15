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
            'customer_id', 
            '_is_current'
        ],
        tags=['gold', 'customers', 'dimension']
    )
}}

WITH customer_source AS (
    SELECT
        {{ dbt_utils.star(from=ref('snap_customers_adworks')) }},
        (dbt_valid_to IS NULL) AS is_current
    FROM {{ ref('snap_customers_adworks') }}
    
    {% if is_incremental() %}
    WHERE dbt_valid_from > (
        SELECT MAX(_valid_from) 
        FROM {{ this }}
    )
    {% endif %}
),

-- Customer demographics segmentation
customer_segments AS (
    SELECT
        customer_id,
        -- Age group calculation
        CASE
            WHEN DATE_DIFF(CURRENT_DATE(), CAST(birthdate AS DATE), YEAR) < 25 THEN 'Under 25'
            WHEN DATE_DIFF(CURRENT_DATE(), CAST(birthdate AS DATE), YEAR) BETWEEN 25 AND 34 THEN '25-34'
            WHEN DATE_DIFF(CURRENT_DATE(), CAST(birthdate AS DATE), YEAR) BETWEEN 35 AND 44 THEN '35-44'
            WHEN DATE_DIFF(CURRENT_DATE(), CAST(birthdate AS DATE), YEAR) BETWEEN 45 AND 54 THEN '45-54'
            WHEN DATE_DIFF(CURRENT_DATE(), CAST(birthdate AS DATE), YEAR) BETWEEN 55 AND 64 THEN '55-64'
            ELSE '65+'
        END AS age_group,
        
        -- Income tier simplification
        CASE
            WHEN yearly_income LIKE '%$30K%' THEN 'Low'
            WHEN yearly_income LIKE '%$50K%' OR yearly_income LIKE '%$70K%' THEN 'Medium'
            WHEN yearly_income LIKE '%$90K%' OR yearly_income LIKE '%$110K%' THEN 'High'
            ELSE 'Very High'
        END AS income_tier,
        
        -- Family status
        CASE
            WHEN marital_status = 'M' AND num_children_at_home > 0 THEN 'Married with children'
            WHEN marital_status = 'M' AND num_children_at_home = 0 THEN 'Married no children'
            WHEN marital_status = 'S' AND num_children_at_home > 0 THEN 'Single parent'
            ELSE 'Single no children'
        END AS family_status,
        
        -- Customer tenure in years
        DATE_DIFF(CURRENT_DATE(), CAST(acct_open_date AS DATE), YEAR) AS customer_tenure_years,
        
        -- Loyalty tier based on member_card and tenure
        CASE
            WHEN member_card = 'Gold' THEN 'Premium'
            WHEN member_card = 'Silver' AND DATE_DIFF(CURRENT_DATE(), CAST(acct_open_date AS DATE), YEAR) >= 5 THEN 'Loyal'
            WHEN member_card = 'Bronze' AND DATE_DIFF(CURRENT_DATE(), CAST(acct_open_date AS DATE), YEAR) >= 10 THEN 'Loyal'
            ELSE 'Standard'
        END AS loyalty_tier
    FROM customer_source
)

-- Final dimension table with enriched attributes
SELECT
    {{ dbt_utils.generate_surrogate_key(['c.customer_id', 'c.dbt_valid_from']) }} AS customer_key,
    {{ dbt_utils.star(from=ref('snap_customers_adworks'), relation_alias='c', except=['dbt_valid_from', 'dbt_valid_to']) }},
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    DATE_DIFF(CURRENT_DATE(), CAST(c.birthdate AS DATE), YEAR) AS age,
    
    -- Enriched business attributes
    s.age_group,
    s.income_tier,
    s.family_status,
    s.customer_tenure_years,
    s.loyalty_tier,
    
    -- Geographic aggregation
    CASE
        WHEN c.customer_country = 'USA' THEN 
            CASE
                WHEN c.customer_state_province IN ('CA', 'OR', 'WA') THEN 'West Coast'
                WHEN c.customer_state_province IN ('NY', 'NJ', 'CT', 'MA') THEN 'Northeast'
                WHEN c.customer_state_province IN ('FL', 'GA', 'SC', 'NC') THEN 'Southeast'
                ELSE 'Other US'
            END
        WHEN c.customer_country = 'Canada' THEN 'Canada'
        ELSE 'International'
    END AS market_region,
    
    -- Customer persona based on demographics
    CASE
        WHEN c.homeowner = 'Y' AND s.income_tier IN ('High', 'Very High') AND c.occupation = 'Professional' THEN 'Affluent Professional'
        WHEN s.family_status LIKE '%with children%' THEN 'Family Focused'
        WHEN s.age_group IN ('55-64', '65+') THEN 'Senior Consumer'
        WHEN s.age_group IN ('Under 25', '25-34') AND s.income_tier = 'Low' THEN 'Young Value Seeker'
        ELSE 'General Consumer'
    END AS customer_persona,
    
    -- SCD metadata
    c.dbt_valid_from AS _valid_from,
    c.dbt_valid_to AS _valid_to,
    c.is_current AS _is_current

FROM customer_source c
LEFT JOIN customer_segments s 
    ON c.customer_id = s.customer_id