# airflow/dags/core/paths.py
from pathlib import Path

# Define the root of the project. Assumes paths.py is in airflow/dags/core
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()

# Airflow specific paths
AIRFLOW_DIR = PROJECT_ROOT / 'airflow'
DAGS_DIR = AIRFLOW_DIR / 'dags'
CORE_DIR = DAGS_DIR / 'core'
AIRFLOW_CONFIG_DIR = AIRFLOW_DIR / 'config' # For Airflow-level config like CSVs
DAG_SPECIFIC_CONFIG_DIR = DAGS_DIR / 'config' # For DAG-specific config/schemas

# Other potential project directories (relative to project root)
# Ensure these directories exist or are created when needed by your application/DAGs
DATA_DIR = PROJECT_ROOT / 'data'
LOGS_DIR = PROJECT_ROOT / 'logs'
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
TESTS_DIR = PROJECT_ROOT / 'tests'
# Add other directories like DBT_DIR if needed:
# DBT_DIR = PROJECT_ROOT / 'dbt'

# Example usage:
# from .paths import DATA_DIR, AIRFLOW_CONFIG_DIR
# input_file = DATA_DIR / 'raw' / 'my_data.csv'
# config_file = AIRFLOW_CONFIG_DIR / 'config_dag.csv'
