import requests
from airflow.models import Variable


class GoogleChatNotifier:
	def __init__(self):
		"""Initialize the AirflowChatNotifier class."""
		self.webhook_url = Variable.get("WEBHOOK_GCHAT_URL")
		if not self.webhook_url:
			raise ValueError("Webhook URL is not set in Airflow Variables.")
		
	"""
	TODO: Add more methods to handle different types of notifications.
	- on_failure: Send a notification to Google Chat on task failure.
	- on_success: Send a notification to Google Chat on task success.
	- on_retry: Send a notification to Google Chat on task retry.
	"""

	def on_success(self, context):
		"""Send a notification to Google Chat on task failure."""
		payload = {
			"text": "\n".join([
				"Data pipeline or task has succeeded.",
				"No context available."
			])
		}

		return requests.post(self.webhook_url, json=payload)

	def on_failure(self, context):
		"""Send a notification to Google Chat on task failure."""
		payload = {
			"text": "\n".join([
				"Data pipeline or task has failed.",
				"No context available."
			])
		}

		return requests.post(self.webhook_url, json=payload)
	

if __name__ == "__main__":
	None