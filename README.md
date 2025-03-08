# Data Engineering - Workflow
<a name="readme-top"></a>
The project implements general workflow for data engineering projects. This aims to create a general workflow for data engineering projects.

## Getting Started

### Prequisite

Before running the application or pipeline, you should have the following installed in your local machine or server.
- Python 3.11 or higher
- UV package
- Docker

This is required in developing, testing and deploying the application in local or remote server. Moreover, this can be tested inside the CLI using the `uv` package and `docker compose` command for local and production environments.

### Running the Application

You can run the pipeline using `uv` package by running the following command:

```bash
uv run dbt run
```

## Reference
- [dbt](https://docs.getdbt.com/docs/introduction)

<!-- ## Prequisites

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

```bash
uv run dbt run
```

## References
-  -->