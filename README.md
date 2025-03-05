## Prequisites

## Testing and Validation

### Testing inside a container
- Make sure that docker container is installed.
- Run the docker compose dbt file.
```
docker compose -f compose.dbt.yml up
```
- Run the following commands:
```
docker-compose exec dbt dbt run
docker-compose exec dbt dbt test
docker-compose exec dbt dbt docs generate
```

### Testing inside a dependency management

- Easier to setup for local development.
- Make sure python 3.11 or higher is installed.
- Make sure that uv is installed.

```
uv run dbt run
```

## References
- 