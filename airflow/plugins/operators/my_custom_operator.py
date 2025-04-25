# airflow/plugins/operators/my_custom_operator.py
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
# Adjust import path based on your structure if needed. 
# This assumes Airflow recognizes the plugins directory correctly.
from airflow.plugins.hooks.my_custom_hook import MyCustomHook 

class MyCustomOperator(BaseOperator):
    """
    Example custom operator using the MyCustomHook.
    """
    template_fields = ('endpoint', 'api_params') # Fields that support Jinja templating

    @apply_defaults
    def __init__(
        self,
        *,
        endpoint: str,
        custom_conn_id: str = 'my_custom_default',
        api_params: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.endpoint = endpoint
        self.custom_conn_id = custom_conn_id
        self.api_params = api_params or {}

    def execute(self, context):
        """Called when the task executes."""
        hook = MyCustomHook(custom_conn_id=self.custom_conn_id)
        try:
            self.log.info(f"Calling API endpoint: {self.endpoint}")
            # Pass rendered fields from context if using templating
            rendered_endpoint = self.endpoint # Templating handled by Airflow
            rendered_params = self.api_params
            result = hook.call_api(endpoint=rendered_endpoint, params=rendered_params)
            self.log.info(f"API Result: {result}")
            # Optionally push result to XCom
            # context['ti'].xcom_push(key='api_result', value=result)
            return result # Operator execute methods should often return something
        except Exception as e:
            self.log.error(f"Operator failed: {e}")
            raise

# In your DAG file:
# from airflow.plugins.operators.my_custom_operator import MyCustomOperator
#
# api_call_task = MyCustomOperator(
#     task_id='call_my_api',
#     endpoint='/data/items',
#     api_params={'filter': 'active', 'date': '{{ ds }}'}, # Example templating
#     custom_conn_id='my_specific_api_conn', # Optional override
#     dag=dag,
# )
