{% snapshot stg_adworks_products_snapshot %}

{{
	config(
		dataset='silver',
		unique_key='product_id',
		strategy='check',
		check_cols=[
			'product_name',
			'product_brand',
			'product_sku',
			'product_retail_price',
			'product_cost',
			'product_weight'
		],
		invalidate_hard_deletes=True
	)
}}

SELECT 
	*
FROM 
	{{ ref('raw_adworks_products') }}

{% endsnapshot %}