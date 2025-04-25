from core.paths import CONFIG_DIR
from datetime import timedelta
import pandas as pd

# Reading the dags config
try:
      _config_df = pd.read_csv(CONFIG_DIR / 'config_dag.csv', dtype=str)
except:
      raise Exception('Could not read config_dag.csv')

DEFAULT_DAG_ARGS = {
      'owner': 'data-team',
      'depends_on_past': False,
      'retries': 3,
      'retry_delay': timedelta(minutes=5),
      'execution_timeout': timedelta(minutes=30),
}

def get_dag_config(id: str) -> dict:
      """Returns the row config for the given id"""

      # Filter based on the id
      filtered_df = _config_df[_config_df['dag_id'] == id]
      if filtered_df.empty:
            raise Exception(f'No config found for dag_id: {id}')
      
      # Convert the datatypes
      filtered_df['start_date'] = pd.to_datetime(filtered_df['start_date'])
      filtered_df['end_date'] = pd.to_datetime(filtered_df['end_date'])
      
      # Fill missing values
      filtered_df.fillna('', inplace=True)
      
      # Convert numpy types to native Python types and return as dict
      return filtered_df.iloc[0].to_dict()

if __name__ == "__main__":
      None