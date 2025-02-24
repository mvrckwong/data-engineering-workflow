from setuptools import find_packages, setup

setup(
    name="etl",
    packages=find_packages(exclude=["etl_tests"]),
    install_requires=[
        "dagster",
        "dagster-webserver",
        "dagit",
        "dagster-postgres",
        "dagster-dbt",
        "SQLAlchemy==1.4.49",
        "pandas",
        "pyarrow",
        "dbt-bigquery"
    ],
    extras_require={"dev": ["pytest"]},
)