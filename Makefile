install_init_reqs:
	pip install uv

reload_reqs:
	uv pip freeze > .devcontainer/requirements.txt

deploy_airflow:
	docker compose -f compose.airflow.prod.yml down
	docker compose -f compose.airflow.prod.yml up -d --build --remove-orphans --force-recreate

deploy_airflow_debug:
	docker compose -f compose.airflow.yml down
	docker compose -f compose.airflow.yml up -d --build --profile flower,debug