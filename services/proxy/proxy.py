"""Configuration-driven gateway for the six counting services."""
import json
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
config_file = Path(__file__).with_name('config.json')
TIMEOUT = 5

def load_config():
    data = json.loads(config_file.read_text())
    services = data.get('services')
    if not isinstance(services, dict) or not services:
        raise ValueError('services must be a nonempty mapping')
    if any(not isinstance(url, str) or not url.startswith(('http://', 'https://'))
           for url in services.values()):
        raise ValueError('service URLs must use HTTP or HTTPS')
    return data

config = load_config()

@app.post('/reload-config')
def reload_config():
    global config
    try:
        replacement = load_config()
    except (OSError, ValueError):
        return jsonify(error='Invalid configuration; previous configuration retained'), 400
    config = replacement
    return jsonify(message='Config reloaded successfully')

@app.get('/check-services')
def check_services():
    statuses = {}
    for name, url in config['services'].items():
        try:
            response = requests.get(url, timeout=2)
            statuses[name] = dict(status='Online' if response.status_code == 200 else 'Error',
                                  http_code=response.status_code)
        except requests.RequestException:
            statuses[name] = dict(status='Offline', error='Service unavailable')
    return jsonify(statuses)

@app.get('/<service_name>')
def proxy_request(service_name):
    url = config['services'].get(service_name)
    if url is None:
        return jsonify(error='Service not found'), 404
    try:
        response = requests.get(url, params=request.args, timeout=TIMEOUT)
        data = response.json()
        return jsonify(data), response.status_code
    except requests.Timeout:
        return jsonify(error='Upstream service timed out'), 504
    except (requests.RequestException, ValueError):
        return jsonify(error='Upstream service unavailable or returned invalid JSON'), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
