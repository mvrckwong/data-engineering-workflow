import requests
from airflow.models import Variable



class NotifyGChat:
	def __init__(self):
		"""Initialize the NotifyGChat class."""
		self.webhook_url = Variable.get("WEBHOOK_GCHAT_URL")
		if not self.webhook_url:
			raise ValueError("Webhook URL is not set in Airflow Variables.")
	
	def on_failure(self, context):
		"""Send a notification to Google Chat on task failure."""
		payload = {
			"text": "Hello from Airflow! We have a failure on class."
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




def notify_gchat_on_failure(context):
	"""Send a notification to Google Chat on task failure."""

	# Get the webhook URL from Airflow Variables
	webhook_url = Variable.get("WEBHOOK_GCHAT_URL")
	if not webhook_url:
		return None

	# Simplest possible payload
	payload = {
		"text": "Hello from Airflow! We have a failure."
	}

	# Send request
	try:
		response = requests.post(
			webhook_url,
			json=payload
		)
		print(f"Status code: {response.status_code}")
		print(f"Response text: {response.text}")
		return response.status_code
	except Exception as e:
		print(f"Exception occurred: {str(e)}")
		return None