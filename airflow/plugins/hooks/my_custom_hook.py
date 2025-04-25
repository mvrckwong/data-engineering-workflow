# airflow/plugins/hooks/my_custom_hook.py
from airflow.hooks.base import BaseHook
import requests # Example dependency

class MyCustomHook(BaseHook):
    """
    Example custom hook to interact with a hypothetical API.
    """
    def __init__(self, custom_conn_id: str = 'my_custom_default'):
        super().__init__()
        self.custom_conn_id = custom_conn_id
        self.connection = None
        self.base_url = None

    def get_conn(self):
        """Initializes the connection based on Airflow connection settings."""
        if not self.connection:
            # Get connection details from Airflow Connections
            self.connection = self.get_connection(self.custom_conn_id)
            self.base_url = self.connection.host # Assuming host stores the base URL
            # You might need other details like login, password, schema, extra
        return self.connection # Or maybe return a session object, etc.

    def call_api(self, endpoint: str, params: dict = None) -> dict:
        """Calls a specific endpoint on the API."""
        self.get_conn() # Ensure connection is established
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.connection.password}"} # Example Auth
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log.error(f"API call failed: {e}")
            raise

# You would need to add an Airflow connection named 'my_custom_default' 
# or 'my_specific_api_conn' with connection type 'HTTP', appropriate Host, and Password.
