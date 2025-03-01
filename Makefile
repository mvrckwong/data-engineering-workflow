run_airflow:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build