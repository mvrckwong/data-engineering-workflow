# # airflow/dags/config/dag_config.py
# import csv
# import yaml # Requires PyYAML installation
# from typing import List, Dict, Any, Optional
# from pydantic import ValidationError
# from pathlib import Path

# # Assuming you have the schemas defined as shown previously
# from airflow.dags.config.schemas.dag_config_schema import DagConfigSchema, DefaultArgsSchema
# from airflow.dags.core.paths import AIRFLOW_CONFIG_DIR, DAG_SPECIFIC_CONFIG_DIR
# from airflow.dags.core.logging import get_task_logger

# logger = get_task_logger(__name__)

# # --- Option 1: Loading from the existing CSV ---
# def load_dag_configs_from_csv(file_path: Path = AIRFLOW_CONFIG_DIR / 'config_dag.csv') -> List[Dict[str, Any]]:
#     """
#     Loads DAG configurations from a CSV file.
#     Note: This is a basic implementation. Complex types (lists, dicts, nested args)
#           are hard to represent cleanly in standard CSV. Consider YAML or JSON.
#     """
#     configs = []
#     try:
#         with open(file_path, mode='r', encoding='utf-8') as infile:
#             reader = csv.DictReader(infile)
#             for row in reader:
#                 # Basic type conversion (add more as needed)
#                 processed_row = {}
#                 for key, value in row.items():
#                     if value.lower() in ['true', 'false']:
#                         processed_row[key] = value.lower() == 'true'
#                     elif value.isdigit():
#                         processed_row[key] = int(value)
#                     elif value == '' or value.lower() == 'none':
#                          processed_row[key] = None
#                     else:
#                         processed_row[key] = value
#                 configs.append(processed_row)
#         logger.info(f"Loaded {len(configs)} DAG configurations from CSV: {file_path}")
#         return configs
#     except FileNotFoundError:
#         logger.error(f"Configuration file not found: {file_path}")
#         return []
#     except Exception as e:
#         logger.error(f"Error loading configuration from CSV {file_path}: {e}", exc_info=True)
#         return []

# # --- Option 2: Loading from YAML (Recommended for structure) ---
# # Example YAML structure (e.g., airflow/config/dags.yaml):
# # dags:
# #   - dag_id: "my_example_dag_1"
# #     description: "An example DAG"
# #     schedule_interval: "0 0 * * *"
# #     catchup: false
# #     default_args_override:
# #       owner: "data_team"
# #       retries: 3
# #       tags: ["example", "production"]
# #     params:
# #       input_path: "/data/raw/input.csv"
# #   - dag_id: "another_dag"
# #     schedule_interval: "@daily"
# #     # ... other params

# def load_dag_configs_from_yaml(file_path: Path = AIRFLOW_CONFIG_DIR / 'dags.yaml') -> List[Dict[str, Any]]:
#     """Loads DAG configurations from a YAML file."""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as stream:
#             # Safely load YAML
#             yaml_content = yaml.safe_load(stream)
#             if yaml_content and 'dags' in yaml_content:
#                 configs = yaml_content['dags']
#                 logger.info(f"Loaded {len(configs)} DAG configurations from YAML: {file_path}")
#                 return configs
#             else:
#                 logger.warning(f"YAML file {file_path} is empty or missing 'dags' key.")
#                 return []
#     except FileNotFoundError:
#         logger.error(f"Configuration file not found: {file_path}")
#         return []
#     except yaml.YAMLError as e:
#         logger.error(f"Error parsing YAML file {file_path}: {e}", exc_info=True)
#         return []
#     except Exception as e:
#         logger.error(f"Error loading configuration from YAML {file_path}: {e}", exc_info=True)
#         return []


# # --- Validation Function ---
# def validate_and_get_dag_config(dag_id: str, config_source: str = 'yaml') -> Optional[DagConfigSchema]:
#     """
#     Loads all DAG configs (from CSV or YAML) and returns the validated config
#     for the specified dag_id.
#     """
#     all_configs: List[Dict[str, Any]] = []
#     if config_source.lower() == 'csv':
#         all_configs = load_dag_configs_from_csv()
#     elif config_source.lower() == 'yaml':
#         # Make sure you create the YAML file (e.g., airflow/config/dags.yaml)
#         all_configs = load_dag_configs_from_yaml()
#     else:
#         logger.error(f"Unsupported config_source: {config_source}. Use 'csv' or 'yaml'.")
#         return None

#     target_config_dict = next((c for c in all_configs if c.get('dag_id') == dag_id), None)

#     if not target_config_dict:
#         logger.warning(f"No configuration found for dag_id='{dag_id}' in {config_source} source.")
#         return None

#     try:
#         # Handle nested default_args_override dictionary
#         if 'default_args_override' in target_config_dict and isinstance(target_config_dict['default_args_override'], dict):
#              # Convert retry_delay_minutes back if necessary or handle in schema/DAG creation
#              pass # Pydantic handles the sub-model directly if types match

#         validated_config = DagConfigSchema(**target_config_dict)
#         logger.info(f"Successfully validated configuration for dag_id='{dag_id}'")
#         return validated_config
#     except ValidationError as e:
#         logger.error(f"Validation error for dag_id='{dag_id}':
# {e}", exc_info=True)
#         return None
#     except Exception as e:
#          logger.error(f"Unexpected error validating config for dag_id='{dag_id}': {e}", exc_info=True)
#          return None

# # Example usage within a DAG file:
# # from airflow.dags.config.dag_config import validate_and_get_dag_config
# #
# # DAG_ID = "my_configured_dag"
# # config = validate_and_get_dag_config(DAG_ID, config_source='yaml') # or 'csv'
# #
# # if config:
# #     # Convert default_args_override Pydantic model back to dict for Airflow DAG
# #     default_args_override_dict = config.default_args_override.dict(exclude_unset=True) if config.default_args_override else None
# #     # You might need to manually convert timedelta back here if you stored it as minutes
# #     if default_args_override_dict and 'retry_delay_minutes' in default_args_override_dict:
# #         from datetime import timedelta
# #         minutes = default_args_override_dict.pop('retry_delay_minutes')
# #         if minutes is not None:
# #             default_args_override_dict['retry_delay'] = timedelta(minutes=minutes)
# #
# #     with create_dag(
# #         dag_id=DAG_ID, # Use DAG_ID from config? config.dag_id
# #         description=config.description,
# #         schedule_interval=config.schedule_interval,
# #         default_args_override=default_args_override_dict,
# #         catchup=config.catchup,
# #         is_paused_upon_creation=config.is_paused_upon_creation,
# #         params=config.params,
# #         # Any other DAG params from config
# #     ) as dag:
# #         # Define tasks using config.params if needed
# #         pass
# # else:
# #     # Handle case where config is missing or invalid - maybe raise AirflowSkipException
# #     from airflow.exceptions import AirflowSkipException
# #     logger.error(f"DAG {DAG_ID} could not be created due to invalid/missing config.")
# #     raise AirflowSkipException(f"Skipping DAG {DAG_ID} due to configuration issues.")
