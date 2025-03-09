from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.providers.slack.notifications.slack_webhook import \
    send_slack_webhook_notification

# Define default arguments that will be applied to all tasks
default_args = {
    'owner': 'analytics-team',  # Owner of the DAG
    'depends_on_past': False,    # Don't wait for previous DAG runs
#     'email': ['analytics-alerts@company.com'],  # Notification emails
#     'email_on_failure': True,    # Send email on task failure
#     'email_on_retry': False,     # No email on retry
    'retries': 2,                # Number of retries per task
    'retry_delay': timedelta(minutes=5),  # Time between retries
    'execution_timeout': timedelta(hours=2),  # Task timeout
    # 'on_failure_callback': callback_function,  # Add failure callback
    # 'on_success_callback': callback_function,  # Add success callback
	'doc_md':__doc__,               # Add documentation if available
	"tags":['dbt', 'tool-based', 'analytics'],
	'start_date':datetime(2024, 1, 1),
	'end_date':datetime(2024, 1, 1),
	'catchup': False,
	'description': 'Sample description'
}


__doc__ = 'sample sample sample'

with DAG(
    dag_id='test-dbt_test_all',
    default_args=default_args,    # Applies to all tasks
    start_date=datetime(2024, 1, 3), # Working
    end_date=datetime(2024, 1, 5), # Working
    schedule_interval=None,
    #on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based'], # Working
    doc_md=__doc__, # Working
    catchup=False,
    #is_active=False,	
    #is_paused_upon_creation=False,
    #is_subdag=False,
    description='Sample description by Airflow', # Working
    dag_display_name='Sample DAG', # Working
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt test'
	)
 

with DAG(
    dag_id='test-dbt_run_all',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    #on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run'
	)


with DAG(
    dag_id='test-dbt_overall',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    #on_success_callback=[on_success_callback],
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
    dag_id='test-dbt_layer_bronze',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    #on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run --select tag:bronze'
	)
 
with DAG(
    dag_id='test-dbt_layer_silver',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    #on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run --select tag:silver'
	)
 
with DAG(
    dag_id='test-dbt_layer_gold',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    #on_success_callback=[on_success_callback],
    tags=['dbt', 'tool-based']
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_deps',
		bash_command='cd /opt/airflow/dbt && dbt run --select tag:gold'
	)