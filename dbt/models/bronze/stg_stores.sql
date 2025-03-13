{{
	config(
		materialized='view',
		dataset='bronze'
	) 
}}

SELECT
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
  grocery_sqft
FROM 
	{{ ref('Stores') }}