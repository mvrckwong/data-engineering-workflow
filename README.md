# Data Engineering - Workflow
<a name="readme-top"></a>
The project implements general workflow for data engineering projects. This aims to create a general workflow for data engineering projects.

Improve test. Improve test. test. test. test

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

In addition, you can run the `dbt` pipeline using `docker compose` command. This enables to check the dbt pipelines inside a docker container. You can run the pipeline inside the `dbt` container by running the following command:

```bash
docker compose -f compose.dbt.yml up -d --build
```

Finally, you can run the pipeline inside the `airflow` container by running the following command:

```bash
docker compose -f compose.airflow.yml up -d --build
```

## Reference
- [dbt](https://docs.getdbt.com/docs/introduction)
- [airflow](https://airflow.apache.org/)

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