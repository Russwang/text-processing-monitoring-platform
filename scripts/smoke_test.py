"""Exercise all six APIs and persistence through the frontend's Nginx routes."""
import json
import sys
import time
import uuid
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.client import HTTPException

base = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080').rstrip('/')

def call(route, body=None):
    data = None if body is None else json.dumps(body).encode()
    request = Request(base + route, data=data, headers={'Content-Type':'application/json'})
    with urlopen(request, timeout=10) as response:
        return json.load(response)

def wait_for_services(attempts=60, interval=2):
    states = {}
    for attempt in range(attempts):
        try:
            states = call('/api/count/check-services')
            if len(states) == 6 and all(s['status'] == 'Online' for s in states.values()):
                return
        except (OSError, HTTPException, ValueError):
            # A published port may briefly reset connections during Nginx startup.
            pass
        time.sleep(interval)
    raise RuntimeError(f'Counting services did not become ready: {states}')

def main():
    wait_for_services()
    for service, text, expected in [('wordcount','Hello world',2),('charcount','hello',5),('vowelcount','AEIOU',5),('commacount','a,b,c',2),('andcount','and AND candy',2),('palindromecount','Madam & noon + wow',3)]:
        from urllib.parse import urlencode
        data = call('/api/count/' + service + '?' + urlencode({'text':text}))
        assert data['answer'] == expected, (service, data)
        print('PASS', service)
    text_id = 'smoke-' + uuid.uuid4().hex
    text = 'Madam & cloud + 你好'
    call('/api/text/saveText', {'id':text_id,'text':text})
    assert call('/api/text/getText?id='+text_id)['text'] == text
    try:
        call('/api/text/saveText', {'id':text_id,'text':text})
    except HTTPError as error:
        assert error.code == 409
    else:
        raise AssertionError('Duplicate ID was accepted')
    call('/api/count/reload-config', {})
    for attempt in range(45):
        states = call('/api/monitor/service-status')
        if len(states) == 6 and all(s['status'] in ('SUCCESS','SLOW') for s in states):
            break
        time.sleep(2)
    else:
        raise AssertionError(('Monitor did not report six healthy services',states))
    assert isinstance(call('/api/monitor/recent-performance'),list)
    print('PASS storage, duplicate protection, config reload and monitoring')

if __name__ == "__main__":
    main()
