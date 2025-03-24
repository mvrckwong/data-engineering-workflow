{% snapshot snap_customers_adworks %}

{{
    config(
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
        invalidate_hard_deletes=True,
        tags=['eg'],
        enabled=false
    )
}}

SELECT 
    * 
FROM 
    {{ ref('stg_customers_adworks') }}

{% endsnapshot %}