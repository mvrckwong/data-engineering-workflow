from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='dbt_overall',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None
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