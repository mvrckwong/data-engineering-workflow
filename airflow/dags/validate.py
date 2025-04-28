from airflow.models.dag import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
# Import Python's native datetime and timezone
from datetime import datetime, timezone

# Define DAG parameters
dag_args = {
    # Use timezone-aware native datetime (UTC is standard practice for Airflow)
    'start_date': datetime(2025, 4, 1, tzinfo=timezone.utc),
    'schedule': None,
    'catchup': False,
    'tags': ['sql', 'example', 'native-datetime'],
}

# Use a 'with' statement to define the DAG context
with DAG(
    dag_id='parameterized_query_native_datetime', # Updated dag_id slightly
    **dag_args # Unpack the dictionary of arguments
) as dag:

    # Define the operator within the DAG context
    opr_param_query = SQLExecuteQueryOperator(
        task_id="param_query",
        conn_id="neon-postgresdb-prod", # Ensure this connection_id exists in Airflow
        sql="SELECT (1 + 1) AS result",
    )

    # Define task dependencies here if needed
    # Example: task1 >> opr_param_query