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

generate_fernet_key:
	uv run --group scripts python scripts/generate_fernet_key.py
	@echo "Fernet key generated"

create_docker_network:
	docker network create shared-airflow-network
	docker network create shared-db-network
	@echo "Docker network created"

create_db_backup:
	docker compose -f compose.db-service.yml down
	docker compose -f compose.db-service.yml up -d --build --remove-orphans --force-recreate
	@echo "DB Backup deployed"