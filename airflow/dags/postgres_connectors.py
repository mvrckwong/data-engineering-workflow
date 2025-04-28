from __future__ import annotations

# Use standard datetime
from datetime import datetime, timezone
import logging

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.connection import Connection # Optional: for type hinting

# Define your Postgres Connection ID configured in Airflow
POSTGRES_CONN_ID = 'your_postgres_conn_id' # <-- IMPORTANT: Replace with your actual connection ID

def retrieve_and_print_connection_details(**kwargs):
    """
    Retrieves connection details using PostgresHook and prints them.
    """
    logging.info(f"Attempting to retrieve connection details for conn_id: {POSTGRES_CONN_ID}")

    try:
        # 1. Instantiate the Hook
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

        # 2. Get the Airflow Connection object
        # The get_connection method is inherited from BaseHook
        connection: Connection = pg_hook.get_connection(conn_id=pg_hook.postgres_conn_id)

        # 3. Access connection attributes
        host = connection.host
        port = connection.port
        schema = connection.schema # Database name
        login = connection.login   # Username
        password = connection.get_password() # Use get_password() to handle potential secrets backend integration

        # For demonstration purposes: Print details (Be VERY careful printing passwords in production logs!)
        logging.info("--- Connection Details ---")
        logging.info(f"Conn Id:  {POSTGRES_CONN_ID}")
        logging.info(f"Host:     {host}")
        logging.info(f"Port:     {port}")
        logging.info(f"Schema:   {schema}") # This corresponds to the 'Database' field in the UI
        logging.info(f"Login:    {login}")
        # Avoid logging passwords in production! This is just for illustration.
        # Consider masking or omitting if needed for debugging.
        logging.info(f"Password: {'*' * len(password) if password else 'None'}")
        logging.info(f"Extra:    {connection.extra_dejson}") # Any JSON extras defined
        logging.info("-------------------------")

        # You can now use these details if needed, e.g., pass them to another tool
        # or construct a connection string manually (though usually letting the hook
        # manage the connection is preferred).

    except Exception as e:
        logging.error(f"Failed to retrieve connection details for {POSTGRES_CONN_ID}: {e}")
        raise # Re-raise the exception to fail the task

# Define the DAG
with DAG(
    dag_id='postgres_connection_retrieval_example_no_pendulum',
    # Use standard datetime for start_date
    start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    schedule=None, # Or your desired schedule
    tags=['example', 'postgres', 'connections'],
) as dag:
    get_connection_task = PythonOperator(
        task_id='get_postgres_connection_details',
        python_callable=retrieve_and_print_connection_details,
    )