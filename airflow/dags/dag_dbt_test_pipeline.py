from core.paths import DAGS_DIR
from config.dag_config import get_dag_config, DEFAULT_DAG_ARGS

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


# Deploying dbt test
current_dag_id = 'test-dbt_test_all'
current_dag_config = get_dag_config(current_dag_id)

with DAG(
    default_args=DEFAULT_DAG_ARGS,
    
    # id and name
    dag_id=current_dag_id,
    dag_display_name=current_dag_config.get('dag_display_name'),
    
    # dates and times
    start_date=current_dag_config.get('start_date'),
    end_date=current_dag_config.get('end_date'),
    #schedule_interval=current_dag_config.get('schedule_interval'),
    
    # documentation
    doc_md=current_dag_config.get('doc_md'),
    description=current_dag_config.get('description'),
    
    # tags
    tags=[tag.strip() for tag in current_dag_config.get('tags').split(',')],
    
    # settings
    catchup=False,
    
) as dag:

	dbt_deps = BashOperator(
		task_id='dbt_run_test',
		bash_command=f'cd {DAGS_DIR} && dbt test'
	)
 
 
# Deploying run
current_dag_id = 'test-dbt_run_all'
current_dag_config = get_dag_config(current_dag_id)

with DAG(
    default_args=DEFAULT_DAG_ARGS,
    
    # id and name
    dag_id=current_dag_id,
    dag_display_name=current_dag_config.get('dag_display_name'),
    
    # dates and times
    start_date=current_dag_config.get('start_date'),
    end_date=current_dag_config.get('end_date'),
    #schedule_interval=current_dag_config.get('schedule_interval'),
    
    # documentation
    doc_md=current_dag_config.get('doc_md'),
    description=current_dag_config.get('description'),
    
    # tags
    tags=[tag.strip() for tag in current_dag_config.get('tags').split(',')],
    
    # settings
    catchup=False,
    
) as dag:

	dbt_run_test = BashOperator(
		task_id='dbt_run_test',
		bash_command=f'cd {DAGS_DIR} && dbt run'
	)
 
 
# Deploying deps, run, test
current_dag_id = 'test-dbt_overall'
current_dag_config = get_dag_config(current_dag_id)

with DAG(
    default_args=DEFAULT_DAG_ARGS,
    
    # id and name
    dag_id=current_dag_id,
    dag_display_name=current_dag_config.get('dag_display_name'),
    
    # dates and times
    start_date=current_dag_config.get('start_date'),
    end_date=current_dag_config.get('end_date'),
    #schedule_interval=current_dag_config.get('schedule_interval'),
    
    # documentation
    doc_md=current_dag_config.get('doc_md'),
    description=current_dag_config.get('description'),
    
    # tags
    tags=[tag.strip() for tag in current_dag_config.get('tags').split(',')],
    
    # settings
    catchup=False,
    
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
 
# Remove the static
del current_dag_id
del current_dag_config


if __name__ == '__main__':
    None