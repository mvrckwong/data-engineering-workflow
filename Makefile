run_airflow:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build

run_airflow_debug:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build --profile flower,debug

reload_reqs:
	uv pip freeze > .devcontainer/requirements.txt