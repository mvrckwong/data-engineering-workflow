run_airflow:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build

run_airflow_debug:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build --profile flower,debug

# Used for testing and developing outside the airflow environment.
run_local_dbt:
	uv run dbt run

# Used for testing and developing outside the airflow environment
run_dbt_debug:
	docker compose -f compose.dbt.yml down
	docker compose -f compose.dbt.yml up -d --build

run_dbt_gold:
	uv run dbt run --select tag:gold

run_dbt_silver:
	uv run dbt run --select tag:silver

run_dbt_bronze:
	uv run dbt run --select tag:bronze

reload_reqs:
	uv pip freeze > .devcontainer/requirements.txt