{% snapshot snap_stores_adworks %}

{{
    config(
        unique_key='store_id',
        strategy='check',
        check_cols=[
            'region_id',
			'store_type',
			'store_name',
			'store_street_address',
			'store_city',
			'store_state',
			'store_country',
			'store_phone',
			'total_sqft',
			'grocery_sqft'
        ],
        invalidate_hard_deletes=True,
        tags=['eg']
    )
}}

SELECT 
    * 
FROM 
    {{ ref('stg_stores_adworks') }}

{% endsnapshot %}