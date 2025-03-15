{% snapshot snap_customers_adworks %}

{{
    config(
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
        invalidate_hard_deletes=True,
        tags=['tests']
    )
}}

SELECT 
    * 
FROM 
    {{ ref('stg_products_adworks') }}

{% endsnapshot %}