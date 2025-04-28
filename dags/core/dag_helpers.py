
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG # Added import
from airflow.decorators import task # Added for @task decorator

def get_default_args():
    """
    Returns a dictionary of default arguments for Airflow DAGs.
    """
    default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2023, 1, 1),
        'email': ['your_email@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'catchup': False,
        'tags': ['core'],
    }
    return default_args

def create_python_task(dag, task_id, python_callable, **kwargs):
    """
    Creates a PythonOperator task with the given parameters.
    """
    return PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
        dag=dag,
        **kwargs,
    )

def create_dag(dag_id, description, schedule_interval, default_args_override=None, **kwargs):
    """
    Creates an Airflow DAG instance with default arguments and optional overrides.

    Args:
        dag_id (str): The unique identifier for the DAG.
        description (str): A description for the DAG.
        schedule_interval (str | timedelta | None): The scheduling interval for the DAG.
        default_args_override (dict, optional): Dictionary to override default arguments. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the DAG constructor.

    Returns:
        DAG: An instance of the Airflow DAG.
    """
    default_args = get_default_args()
    if default_args_override:
        # Special handling for retry_delay if provided as minutes in override
        if 'retry_delay_minutes' in default_args_override:
            minutes = default_args_override.pop('retry_delay_minutes')
            if minutes is not None:
                 default_args['retry_delay'] = timedelta(minutes=minutes)
            else:
                 # Handle case where it's explicitly set to None, perhaps remove from default_args?
                 if 'retry_delay' in default_args: del default_args['retry_delay']

        default_args.update(default_args_override)

    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        description=description,
        schedule_interval=schedule_interval,
        catchup=kwargs.pop('catchup', default_args.get('catchup', False)), # Use default_args catchup if not overridden
        tags=kwargs.pop('tags', default_args.get('tags', [])), # Use default_args tags if not overridden
        **kwargs
    )
    return dag


# --- Decorator Examples --- 

@task # Basic example decorator usage
def simple_python_task_decorator(some_input: str):
    """Task defined using the @task decorator."""
    print(f"Received input: {some_input}")
    # ... logic ...
    return {"result": f"Processed {some_input}"}

@task.virtualenv # Example running in a virtual environment
def python_task_in_venv(reqs: list, python_version: str, some_input: str):
     """Task defined to run in a virtual environment."""
     import sys
     # This code runs *inside* the dynamically created virtual environment
     print(f"Running with Python {sys.version}") 
     print(f"Received input: {some_input}")
     # Example: Import a library specified in reqs
     try:
         import pandas as pd
         print("Pandas version:", pd.__version__)
     except ImportError:
         print("Pandas not found (or not requested)")
     
     # ... logic using installed libraries ...
     return {"result": f"Processed {some_input} in venv"}

# Usage in DAG file:
# from airflow.dags.core.dag_helpers import simple_python_task_decorator, python_task_in_venv
#
# with my_dag:
#     simple_task_instance = simple_python_task_decorator("hello world")
#     venv_task_instance = python_task_in_venv(
#         reqs=["pandas==1.5.3"], # Example requirements
#         python_version="3.9", # Ensure this python is available to Airflow worker
#         some_input="data_file.csv"
#     )
#     simple_task_instance >> venv_task_instance

