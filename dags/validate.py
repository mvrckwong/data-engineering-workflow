from airflow.models.dag import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timezone

from settings.callbacks import GoogleChatNotifier

# Define static variables and functions
default_args = {
	'start_date': datetime(2025, 4, 1, tzinfo=timezone.utc),
	'schedule': None,
	'catchup': False,
	'tags': ['sql', 'example', 'native-datetime']
}
gchat_notifier = GoogleChatNotifier()

with DAG(
	dag_id='validate_db_connections',
	dag_display_name='Validate DB Connections',
	description='Validate DB Connections',
	on_failure_callback=[gchat_notifier.on_failure],
	on_success_callback=[gchat_notifier.on_success],
	**default_args
) as dag:

    	# Define the operator within the DAG context
	task_1 = SQLExecuteQueryOperator(
		task_id="validate_neon_prod",
		conn_id="neon-postgresdb-prod",
		on_success_callback=[gchat_notifier.on_success_task],
		sql="SELECT 1",
	)

	task_2 = SQLExecuteQueryOperator(
		task_id="validate_neon_dev",
		conn_id="neon-postgresdb-dev",
		sql="SELECT 1",
	)

	task_3 = SQLExecuteQueryOperator(
		task_id="validate_neon_test",
		conn_id="neon-postgresdb-test",
		sql="SELECT 1",
	)

	# Set task dependencies
	task_1 >> task_2 >> task_3

