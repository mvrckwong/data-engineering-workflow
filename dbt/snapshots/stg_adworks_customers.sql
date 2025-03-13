{% snapshot stg_adworks_customers_snapshot %}

{{
	config(
		dataset='silver',
		unique_key='customer_id',
		strategy='check',
		check_cols=[
			'customer_acct_num',
			'customer_address',
			'customer_city',
			'customer_state_province',
			'customer_postal_code',
			'customer_country'
		],
		invalidate_hard_deletes=True
	)
}}

SELECT 
	*
FROM 
	{{ ref('raw_adworks_customers') }}

{% endsnapshot %}