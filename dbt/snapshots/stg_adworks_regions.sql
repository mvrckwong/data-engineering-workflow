{% snapshot stg_adworks_regions_snapshot %}

{{
	config(
		dataset='silver',
		unique_key='region_id',
		strategy='check',
		check_cols=[
			'sales_district',
			'sales_region'
		],
		invalidate_hard_deletes=True
	)
}}

SELECT 
	*
FROM 
	{{ ref('raw_adworks_regions') }}

{% endsnapshot %}