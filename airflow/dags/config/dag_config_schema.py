# airflow/dags/config/schemas/dag_config_schema.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import timedelta

# Replicate relevant fields from default_args for potential override validation
class DefaultArgsSchema(BaseModel):
    owner: Optional[str] = None
    depends_on_past: Optional[bool] = None
    start_date: Optional[str] = None # Keep as str for simple loading, validation below
    email: Optional[List[str]] = None
    email_on_failure: Optional[bool] = None
    email_on_retry: Optional[bool] = None
    retries: Optional[int] = Field(None, ge=0)
    retry_delay_minutes: Optional[int] = Field(None, ge=0) # Use minutes for simplicity in config
    tags: Optional[List[str]] = None

    @validator('start_date', pre=True, always=True)
    def validate_start_date(cls, v):
        if v:
            # Add more robust date parsing/validation if needed
            pass
        return v

class DagConfigSchema(BaseModel):
    dag_id: str = Field(..., min_length=1)
    description: str = "No description provided"
    schedule_interval: Optional[str] = None # Airflow accepts cron strings, timedelta, None
    catchup: bool = False
    is_paused_upon_creation: bool = True
    default_args_override: Optional[DefaultArgsSchema] = None
    # Add any other DAG-level parameters you want to configure
    params: Optional[Dict[str, Any]] = {} # For Airflow params

    # Example of a custom validation if needed
    # @validator('schedule_interval')
    # def validate_schedule(cls, v):
    #     # Add cron validation logic if desired
    #     return v

# If loading from CSV or other formats, you might have a top-level model
# class AllDagConfigs(BaseModel):
#     dags: List[DagConfigSchema]
