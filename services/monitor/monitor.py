"""Periodic semantic checks and latency measurement with SQLite history."""
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import threading
import time
import schedule
from flask import Flask, jsonify
from flask_cors import CORS
from utils.test_services import test_service
from utils.alerts import send_alert
from utils.logger import DB_PATH, init_db, log

app = Flask(__name__)
CORS(app)
init_db()
config = json.loads(Path(__file__).with_name('config.json').read_text())
services = config['services']
test_cases = config['test_cases']
threshold = config['performance_threshold']
webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', '')

def read_logs(query):
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(query)]

@app.get('/recent-performance')
def recent_performance():
    return jsonify(read_logs('SELECT service_name, status, message, timestamp FROM logs ORDER BY id DESC LIMIT 12'))

@app.get('/service-status')
def service_status():
    # Health samples only; an alert delivery log must not replace health state.
    return jsonify(read_logs("""
        SELECT service_name, status, message, timestamp FROM logs
        WHERE id IN (SELECT MAX(id) FROM logs
                     WHERE status IN ('SUCCESS', 'FAILURE', 'SLOW') GROUP BY service_name)
        ORDER BY service_name
    """))

def monitor_services():
    for name, url in services.items():
        started = time.perf_counter()
        success, result = test_service(name, url, test_cases.get(name, {}))
        elapsed = time.perf_counter() - started
        if not success:
            log(name, 'FAILURE', str(result))
            send_alert(name, str(result), webhook_url)
        elif elapsed > threshold:
            message = f'Response time: {elapsed:.3f}s exceeds {threshold:.3f}s'
            log(name, 'SLOW', message)
            send_alert(name, message, webhook_url)
        else:
            log(name, 'SUCCESS', f'Response time: {elapsed:.3f}s; answer: {result["answer"]}')

def run_scheduler():
    monitor_services()
    schedule.every(1).minutes.do(monitor_services)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.get('/')
def home():
    return jsonify(status='Monitoring service is running')

if __name__ == '__main__':
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host='0.0.0.0', port=7000)
