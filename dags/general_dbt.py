from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.providers.slack.notifications.slack_webhook import \
    send_slack_webhook_notification

with DAG(
    dag_id='dbt_test_all',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt test'
	)
 

with DAG(
    dag_id='dbt_run_all',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run'
	)


with DAG(
    dag_id='dbt_overall',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt deps'
	)

	dbt_run = BashOperator(
		task_id='dbt_run',
		bash_command='cd /opt/airflow/dbt && dbt run'
	)

	dbt_test = BashOperator(
		task_id='dbt_test',
		bash_command='cd /opt/airflow/dbt && dbt test'
	)

	dbt_deps >> dbt_run >> dbt_test
 
 

with DAG(
    dag_id='dbt_layer_bronze',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run --select tag:bronze'
	)
 
with DAG(
    dag_id='dbt_layer_silver',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run --select tag:silver'
	)
 
with DAG(
    dag_id='dbt_layer_gold',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run --select tag:gold'
	)