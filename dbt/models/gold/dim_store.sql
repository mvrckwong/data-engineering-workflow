{{
  config(
    materialized='table',
    unique_key='store_key',
    dataset='gold'
  )
}}

select
  {{ dbt_utils.generate_surrogate_key(['store_id', 'dbt_valid_from']) }} as store_key,
  store_id,
  region_id,
  store_type,
  store_name,
  store_street_address,
  store_city,
  store_state,
  store_country,
  store_phone,
  total_sqft,
  grocery_sqft,
  -- Validity windows
  dbt_valid_from as valid_from,
  dbt_valid_to as valid_to,
  case 
    when dbt_valid_to is null then true 
    else false 
  end as is_current
from {{ ref('store_snapshot') }}