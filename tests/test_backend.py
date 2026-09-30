"""Regression tests for gateway, persistence and monitoring failures."""
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import requests

ROOT = Path(__file__).resolve().parents[1]
TEMP = tempfile.TemporaryDirectory()
os.environ['TEXT_DB_PATH'] = str(Path(TEMP.name) / 'nested/text.db')
os.environ['MONITOR_DB_PATH'] = str(Path(TEMP.name) / 'other/monitor.db')
os.environ['DISCORD_WEBHOOK_URL'] = ''

def load(name, directory, filename):
    directory = ROOT / 'services' / directory
    sys.path.insert(0, str(directory))
    try:
        spec = importlib.util.spec_from_file_location(name, directory / filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)

proxy = load('gateway', 'proxy', 'proxy.py')
store = load('store', 'text-store', 'app.py')
monitor = load('monitor', 'monitor', 'monitor.py')
from utils import logger, test_services, alerts

class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.client = proxy.app.test_client()

    def test_unknown_service(self):
        self.assertEqual(self.client.get('/unknown').status_code, 404)

    def test_upstream_status_preserved_and_timeout_set(self):
        response = Mock(status_code=400)
        response.json.return_value = {'error': 'Bad input'}
        with patch.object(proxy.requests, 'get', return_value=response) as get:
            self.assertEqual(self.client.get('/vowelcount?text=a').status_code, 400)
            self.assertEqual(get.call_args.kwargs['timeout'], 5)
            self.assertEqual(get.call_args.kwargs['params']['text'], 'a')

    def test_upstream_timeout(self):
        with patch.object(proxy.requests, 'get', side_effect=requests.Timeout):
            self.assertEqual(self.client.get('/vowelcount').status_code, 504)

    def test_bad_json_and_unavailable(self):
        response = Mock(status_code=200)
        response.json.side_effect = ValueError('not JSON')
        with patch.object(proxy.requests, 'get', return_value=response):
            self.assertEqual(self.client.get('/vowelcount').status_code, 502)
        with patch.object(proxy.requests, 'get', side_effect=requests.ConnectionError):
            self.assertEqual(self.client.get('/vowelcount').status_code, 502)

    def test_failed_reload_retains_config(self):
        before = proxy.config
        with patch.object(proxy, 'config_file') as file:
            file.read_text.return_value = '{"services": []}'
            self.assertEqual(self.client.post('/reload-config').status_code, 400)
        self.assertIs(proxy.config, before)

    def test_health_offline_and_error(self):
        with patch.object(proxy.requests, 'get', side_effect=requests.Timeout):
            states = self.client.get('/check-services').json
            self.assertTrue(all(x['status'] == 'Offline' for x in states.values()))
        with patch.object(proxy.requests, 'get', return_value=Mock(status_code=503)):
            states = self.client.get('/check-services').json
            self.assertTrue(all(x['status'] == 'Error' for x in states.values()))

class StorageTests(unittest.TestCase):
    def setUp(self):
        self.client = store.app.test_client()
        with sqlite3.connect(store.DB_PATH) as conn:
            conn.execute('DELETE FROM text_store')

    def test_round_trip_and_duplicate(self):
        data = {'id': "quote'雪", 'text': 'Madam & cloud + 你好'}
        self.assertEqual(self.client.post('/saveText', json=data).status_code, 201)
        self.assertEqual(self.client.get('/getText', query_string={'id': data['id']}).json['text'], data['text'])
        self.assertEqual(self.client.post('/saveText', json=data).status_code, 409)
        self.assertEqual(self.client.get('/getText', query_string={'id': data['id']}).json['text'], data['text'])

    def test_invalid_payloads(self):
        for data in [None, [], 'text', {}, {'text': ['x'], 'id': 'a'}, {'text': 'x', 'id': 12}, {'text':'x','id':' '}, {'text':' ','id':'a'}]:
            with self.subTest(data=data):
                self.assertEqual(self.client.post('/saveText', json=data).status_code, 400)
        self.assertEqual(self.client.post('/saveText', data='{bad', content_type='application/json').status_code, 400)

    def test_missing_id_or_text(self):
        self.assertEqual(self.client.get('/getText').status_code, 400)
        self.assertEqual(self.client.get('/getText?id=absent').status_code, 404)

class MonitoringTests(unittest.TestCase):
    def setUp(self):
        with sqlite3.connect(logger.DB_PATH) as conn:
            conn.execute('DELETE FROM logs')

    def test_semantic_check_and_expected_not_forwarded(self):
        response = Mock()
        response.json.return_value = {'answer': 999}
        with patch.object(test_services.requests, 'get', return_value=response) as get:
            ok, message = test_services.test_service('vowelcount', 'http://vowelcount', {'text':'a','expected_answer':1})
            self.assertFalse(ok)
            self.assertIn('Incorrect answer', message)
            self.assertEqual(get.call_args.kwargs['params'], {'text':'a'})
            self.assertEqual(get.call_args.kwargs['timeout'], 5)

    def test_invalid_answer_and_failure(self):
        for data in [[], {}, {'answer': True}, {'answer':'1'}]:
            response = Mock()
            response.json.return_value = data
            with patch.object(test_services.requests, 'get', return_value=response):
                self.assertFalse(test_services.test_service('x','http://x',{})[0])
        with patch.object(test_services.requests,'get',side_effect=requests.Timeout):
            self.assertFalse(test_services.test_service('x','http://x',{})[0])

    def test_latest_health_uses_id_and_ignores_alert_logs(self):
        logger.log('x','FAILURE','first')
        logger.log('x','SUCCESS','latest in same second')
        logger.log('x','ALERT_ERROR','alert failed')
        response = monitor.app.test_client().get('/service-status')
        self.assertEqual(response.json[0]['status'],'SUCCESS')
        self.assertEqual(response.json[0]['message'],'latest in same second')

    def test_latency_uses_one_request_and_slow_alert(self):
        with patch.object(monitor,'services',{'x':'http://x'}), patch.object(monitor,'threshold',1), \
             patch.object(monitor,'test_service',return_value=(True,{'answer':1})) as check, \
             patch.object(monitor.time,'perf_counter',side_effect=[0,2]), \
             patch.object(monitor,'send_alert') as alert:
            monitor.monitor_services()
            check.assert_called_once()
            alert.assert_called_once()
        self.assertEqual(monitor.app.test_client().get('/service-status').json[0]['status'],'SLOW')

    def test_failure_health_not_overwritten_by_alert(self):
        with patch.object(monitor,'services',{'x':'http://x'}), \
             patch.object(monitor,'test_service',return_value=(False,'bad answer')), \
             patch.object(monitor,'send_alert') as alert:
            monitor.monitor_services()
            alert.assert_called_once()
        self.assertEqual(monitor.app.test_client().get('/service-status').json[0]['status'],'FAILURE')

    def test_webhook_disabled_and_secret_not_logged(self):
        with patch.object(alerts.requests,'post') as post:
            alerts.send_alert('x','failure','')
            post.assert_not_called()
        with patch.object(alerts.requests,'post',side_effect=requests.Timeout('SECRET')):
            alerts.send_alert('x','failure','http://example.invalid/SECRET')
        history = monitor.app.test_client().get('/recent-performance').json
        self.assertNotIn('SECRET', json.dumps(history))

if __name__ == '__main__':
    unittest.main()
