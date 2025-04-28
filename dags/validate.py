from airflow.models.dag import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from datetime import datetime, timezone

default_args = {
	'start_date': datetime(2025, 4, 1, tzinfo=timezone.utc),
	'schedule': None,
	'catchup': False,
	'tags': ['sql', 'example', 'native-datetime'],
}

with DAG(
    dag_id='validate_db_connections',
    dag_display_name='Validate DB Connections',
    **default_args
) as dag:

    	# Define the operator within the DAG context
	task_1 = SQLExecuteQueryOperator(
		task_id="validate_neon_prod",
		conn_id="neon-postgresdb-prod",
		sql="SELECT 1",
	)

	task_2 = SQLExecuteQueryOperator(
		task_id="validate_neon_dev",
		conn_id="neon-postgresdb-dev",
		sql="SELECT 1",
	)

	# Set task dependencies
	task_1 >> task_2