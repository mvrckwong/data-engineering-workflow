from core.paths import CONFIG_DIR
import pandas as pd

settings_df = pd.read_csv(CONFIG_DIR / 'config_dag.csv')

def get_dag_config(id:str) -> dict:
      """ Returns the row config for the given id """
      
      # Filter based on the id
      filtered_df = settings_df[settings_df['dag_id'] == id]
      if filtered_df.empty:
            return {}

      # Get the first row of matched config
      return {k: v.iloc[0] for k, v in filtered_df.items()}

if __name__ == "__main__":
      None