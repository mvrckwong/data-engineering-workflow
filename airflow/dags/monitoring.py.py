# dags/python_operator_native_datetime_sample.py

# --- Import native datetime and timezone ---
from datetime import datetime, timezone

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from flask_login import current_user

# --- 1. Define the Python function to be executed (same as before) ---
def my_python_function(input_message: str) -> str:
    """
    This is a simple Python function that will be executed by the operator.
    It prints the input message and returns a modified string.
    """
    print(f"Received message: {input_message}")
    output_message = f"Processed: {input_message}"
    print(f"Returning: {output_message}")
    # The return value is automatically pushed to Airflow's XCom
    return output_message

# --- 2. Define the DAG ---
# Use the DAG context manager
with DAG(
    dag_id='python_operator_native_datetime_example', # Unique identifier
    # --- Use native datetime with UTC timezone ---
    start_date=datetime(2025, 4, 27, tzinfo=timezone.utc), # Timezone-aware start date
    schedule=None, # Manual trigger only
    catchup=False, # Don't run past schedules
    tags=['example', 'python', 'native_datetime'], # Updated tags
    description='A simple example using PythonOperator with native datetime',
) as dag:

    # --- 3. Define the PythonOperator Task (same as before) ---
    run_this = PythonOperator(
        task_id='run_my_python_code', # Unique identifier for this task
        python_callable=my_python_function, # Reference to the Python function
        op_kwargs={'input_message': 'Hello from Airflow using native datetime!'}, # Arguments
    )


# Inside a Flask view function within your Airflow plugin/customization
def my_custom_view():
    if current_user.is_authenticated:
        user_roles = [role.name for role in current_user.roles]
        print(f"Current user roles: {user_roles}")
        
# Use the DAG context manager
with DAG(
    dag_id='sample_sample', # Unique identifier
    # --- Use native datetime with UTC timezone ---
    start_date=datetime(2025, 4, 27, tzinfo=timezone.utc), # Timezone-aware start date
    schedule=None, # Manual trigger only
    catchup=False, # Don't run past schedules
    tags=['example', 'python', 'native_datetime'], # Updated tags
    description='A simple example using PythonOperator with native datetime',
) as dag:

    # --- 3. Define the PythonOperator Task (same as before) ---
    run_this = PythonOperator(
        task_id='run_my_python_code', # Unique identifier for this task
        python_callable=my_custom_view, # Reference to the Python function
        op_kwargs={'input_message': 'Hello from Airflow using native datetime!'}, # Arguments
    )