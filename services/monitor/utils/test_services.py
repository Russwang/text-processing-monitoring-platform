import requests

def test_service(service_name, url, test_case):
    params = {k: v for k, v in test_case.items() if k != 'expected_answer'}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict) or type(data.get('answer')) is not int:
            return False, 'Invalid response: integer answer required'
        if 'expected_answer' in test_case and data['answer'] != test_case['expected_answer']:
            return False, f"Incorrect answer: expected {test_case['expected_answer']}, got {data['answer']}"
        return True, data
    except (requests.RequestException, ValueError):
        return False, 'HTTP request failed or invalid JSON response'
