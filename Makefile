run_prod:
	docker-compose -f compose.prod.yml down
	docker-compose -f compose.prod.yml up -d --build

run_stg:
	docker-compose -f compose.stg.yml down
	docker-compose -f compose.stg.yml up -d --build