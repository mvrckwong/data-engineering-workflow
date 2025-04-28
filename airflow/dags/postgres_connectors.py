from __future__ import annotations

# Use standard datetime
from datetime import datetime, timezone
import traceback # Import traceback for detailed error logging

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.connection import Connection # Optional: for type hinting
from airflow.exceptions import AirflowNotFoundException # For more specific exception handling

# Define your Postgres Connection ID configured in Airflow
POSTGRES_CONN_ID = 'neon-postgresdb-dev'

print(f"[INFO] Starting DAG: {__file__}")
print(f"[INFO] Using Postgres Connection ID: {POSTGRES_CONN_ID}")

def retrieve_and_print_connection_details(**kwargs):
    """
    Retrieves connection details using PostgresHook and prints them
    with enhanced logging for debugging.
    """
    print(f"[INFO] Task started. Attempting to retrieve connection details for conn_id: '{POSTGRES_CONN_ID}'")

    pg_hook = None # Initialize to None
    connection = None # Initialize to None

    try:
        # 1. Instantiate the Hook
        print(f"[INFO] STEP 1: Instantiating PostgresHook(postgres_conn_id='{POSTGRES_CONN_ID}')")
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        print("[INFO] STEP 1: PostgresHook instantiated successfully.")

        # 2. Get the Airflow Connection object
        print(f"[INFO] STEP 2: Attempting pg_hook.get_connection(conn_id='{pg_hook.postgres_conn_id}')")
        # The get_connection method is inherited from BaseHook
        connection: Connection = pg_hook.get_connection(conn_id=pg_hook.postgres_conn_id)
        print("[INFO] STEP 2: pg_hook.get_connection() successful.")

        if connection:
            print("[INFO] STEP 3: Connection object retrieved. Accessing attributes...")
            # 3. Access connection attributes
            host = connection.host
            port = connection.port
            schema = connection.schema # Database name
            login = connection.login   # Username
            password = connection.get_password() # Use get_password() to handle potential secrets backend integration
            extra = connection.extra_dejson

            print("[INFO] STEP 3: Attributes accessed successfully.")

            # 4. Print details
            print("[INFO] STEP 4: Printing connection details...")
            print("--- Connection Details ---")
            print(f"Conn Id:  {POSTGRES_CONN_ID}")
            print(f"Host:     {host}")
            print(f"Port:     {port}")
            print(f"Schema:   {schema}") # This corresponds to the 'Database' field in the UI
            print(f"Login:    {login}")
            # Avoid printing passwords in production! Masking it here.
            print(f"Password: {'*' * len(password) if password else 'None'}")
            print(f"Extra:    {extra}") # Any JSON extras defined
            print("-------------------------")
            print(f"[SUCCESS] Successfully retrieved and printed details for '{POSTGRES_CONN_ID}'. Task finished.")
        else:
            # This case is unlikely as get_connection usually raises if not found, but good to have
            print(f"[WARN] pg_hook.get_connection() returned None for '{POSTGRES_CONN_ID}'. Cannot print details.")
            # Consider raising an error here if a None connection is unexpected
            # raise ValueError(f"Connection object for '{POSTGRES_CONN_ID}' was None.")

    except AirflowNotFoundException as anfe:
        print(f"[ERROR] Failed to find Airflow Connection with conn_id='{POSTGRES_CONN_ID}'.")
        print(f"[ERROR] Please ensure a connection with this exact ID exists in Airflow -> Admin -> Connections.")
        print(f"[ERROR] Exception details: {anfe}")
        traceback.print_exc() # Print full traceback to logs
        raise # Re-raise the exception to fail the task
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while processing conn_id='{POSTGRES_CONN_ID}'.")
        # Print details about where it might have failed based on pg_hook and connection status
        if pg_hook is None:
            print("[ERROR] Failure likely occurred during PostgresHook instantiation.")
        elif connection is None:
             print("[ERROR] Failure likely occurred during pg_hook.get_connection(). Check connection details or Airflow/DB connectivity.")
        else:
             print("[ERROR] Failure likely occurred while accessing connection attributes or printing details.")
        print(f"[ERROR] Exception details: {e}")
        traceback.print_exc() # Print full traceback to logs
        raise # Re-raise the exception to fail the task

# Define the DAG
with DAG(
    dag_id='postgres_connection_retrieval_example_debug_print', # Updated dag_id
    # Use standard datetime for start_date
    start_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    schedule=None, # Or your desired schedule
    tags=['example', 'postgres', 'connections', 'debug', 'print'],
) as dag:
    print(f"[INFO] DAG '{dag.dag_id}' instantiated.")
    get_connection_task = PythonOperator(
        task_id='get_postgres_connection_details_debug_print', # Updated task_id
        python_callable=retrieve_and_print_connection_details,
    )