{% snapshot snap_regions_adworks %}

{{
    config(
        unique_key='region_id',
        strategy='check',
        check_cols=[
            'sales_district',
			'sales_region'
        ],
        invalidate_hard_deletes=True,
        tags=['eg'],
        enabled=false
    )
}}

SELECT 
    * 
FROM 
    {{ ref('stg_regions_adworks') }}

{% endsnapshot %}