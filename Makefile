install_init_reqs:
	pip install uv

reload_reqs:
	uv sync
	uv pip freeze > .devcontainer/requirements.txt
	@echo "Updated requirements.txt from pyproject.toml" 

deploy_airflow:
	docker compose -f compose.airflow.prod.yml --profile debug down
	docker compose -f compose.airflow.prod.yml up -d --build --remove-orphans --force-recreate
	@echo "Airflow deployed"

deploy_airflow_debug:
	docker compose -f compose.airflow.prod.yml --profile debug down
	docker compose -f compose.airflow.prod.yml --profile debug up -d --build --remove-orphans --force-recreate
	@echo "Airflow deployed in debug mode"
