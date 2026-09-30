import requests
from utils.logger import log

def send_alert(service_name, error_message, webhook_url=None):
    if not webhook_url:
        return
    try:
        response = requests.post(webhook_url,
                                 json={'content': f'{service_name} ALERT: {error_message}'},
                                 timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        # Never put the webhook URL (which contains a secret) into logs.
        log(service_name, 'ALERT_ERROR', 'Webhook delivery failed')
