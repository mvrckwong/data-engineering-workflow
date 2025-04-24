from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# The exact name of the running container you want to execute commands in
TARGET_CONTAINER_NAME = "dbt-instance-bigquery-prod-serve-1"

# The command you want to run inside that container
# Adapt this based on what dbt command you need and the setup inside the container
# (e.g., if WORKDIR is set correctly, you might just need 'dbt run')
COMMAND_TO_RUN = "dbt run --select tag:gold" # Example: Run dbt for a specific model
# COMMAND_TO_RUN = "dbt test" # Example: Run dbt tests
# COMMAND_TO_RUN = "dbt run --project-dir /path/in/container --profiles-dir /path/in/container" # If paths need specification

with DAG(
    dag_id="execute_in_existing_dbt_container",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    # As of April 16, 2025, Cainta, Calabarzon, Philippines
    schedule=None,
    catchup=False,
    tags=["dbt", "docker", "existing_container"],
) as dag:
    run_dbt_in_existing_container = BashOperator(
        task_id="run_dbt_in_existing_container",
        # Construct the docker exec command
        bash_command=f"docker exec {TARGET_CONTAINER_NAME} {COMMAND_TO_RUN}",
        # Optional: Add environment variables specifically for this execution if needed
        # env={'DBT_TARGET': 'prod', 'VAR_X': 'value_y'},
        # append_env=True # If you want to add to existing Airflow worker env vars
    )

    

    # You can add more tasks here, perhaps another docker exec command
    test_dbt_in_existing_container = BashOperator(
       task_id="test_dbt_in_existing_container",
       bash_command=f"docker exec {TARGET_CONTAINER_NAME} dbt test"
    )
    
    run_dbt_in_existing_container >> test_dbt_in_existing_container