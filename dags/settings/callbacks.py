import requests
from airflow.models import Variable


class GoogleChatNotifier:
	def __init__(self):
		"""Initialize the AirflowChatNotifier class."""
		self._webhook_gchat_url = Variable.get("WEBHOOK_GCHAT_URL")
		if not self._webhook_gchat_url:
			raise ValueError("Webhook URL is not set in Airflow Variables.")
		
	"""
	TODO: Add more methods to handle different types of notifications.
	- on_failure: Send a notification to Google Chat on task failure.
	- on_success: Send a notification to Google Chat on task success.
	- on_retry: Send a notification to Google Chat on task retry.
	"""

	def on_success_task(self, context):
		payload = {
			"text": "\n".join([
				f"Task has succeeded.\n",
				f"Run ID: {context['run_id']}",
				f"DAG: {context['dag']}"
			])
		}

		return requests.post(self._webhook_gchat_url, json=payload)
	
	def on_failure_task(self, context):
		payload = {
			"text": "\n".join([
				f"Task has failed.\n",
				f"Run ID: {context['run_id']}",
				f"DAG Run Params: {context['dag_run']}"
			])
		}

		return requests.post(self._webhook_gchat_url, json=payload)

	def on_success(self, context):
		"""Send a notification to Google Chat on task failure."""

		payload = {
			"text": "\n".join([
				f"Pipeline has succeeded."
			])
		}

		return requests.post(self._webhook_gchat_url, json=payload)

	def on_failure(self, context):
		"""Send a notification to Google Chat on task failure."""
		payload = {
			"text": "\n".join([
				f"Pipeline has failed."
			])
		}

		return requests.post(self._webhook_gchat_url, json=payload)
	

if __name__ == "__main__":
	None