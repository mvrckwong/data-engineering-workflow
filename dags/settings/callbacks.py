import requests
from airflow.models import Variable


class AirflowChatNotifier:
	def __init__(self):
		"""Initialize the AirflowChatNotifier class."""
		self.webhook_url = Variable.get("WEBHOOK_GCHAT_URL")
		if not self.webhook_url:
			raise ValueError("Webhook URL is not set in Airflow Variables.")
		
	# TODO: Add more methods to handle different types of notifications.
	# Data pipeline or task has failed.
	# Data pipeline or task has succeeded.
	# Data pipeline or task on retry.

	def on_failure(self, context):
		"""Send a notification to Google Chat on task failure."""
		payload = {
			"text": "\n".join([
				"Data pipeline or task has failed."
			])
		}
	
		try:
			response = requests.post(
				self.webhook_url,
				json=payload
			)
			print(f"Status code: {response.status_code}")
			print(f"Response text: {response.text}")
			return response.status_code
		except Exception as e:
			print(f"Exception occurred: {str(e)}")
			return None