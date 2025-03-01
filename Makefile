run_airflow:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build

reload_reqs:
	uv pip freeze > requirements.txt