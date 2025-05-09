import requests

def notify_gchat_on_failure(context):
    # Google Chat Webhook URL
    webhook_url = ""
    
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