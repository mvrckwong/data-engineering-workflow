from pathlib import Path
from typing import Final

CORE_DIR = Path(__file__).parent
DAGS_DIR = CORE_DIR.parent

PROJ_DIR = DAGS_DIR.parent
DATA_DIR = PROJ_DIR / 'data'
LOGS_DIR = PROJ_DIR / 'logs'
DBT_DIR = PROJ_DIR / 'dbt'
CONFIG_DIR = PROJ_DIR / 'config'

if __name__ == "__main__":
      None