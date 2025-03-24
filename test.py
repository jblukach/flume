import json
import requests

headers = {
    'Content-Type': 'application/json'
}

data = '{"one": "MISSISSIPPI", "two": "MISSISSIPPI", "three": "MISSISSIPPI"}'

r = requests.post(
    'https://1c3tvs3c52.execute-api.us-east-1.amazonaws.com/logs?verify=<VERIFY>',
    headers = headers,
    data = data
)

print(r.status_code)
print(json.dumps(r.json(), indent=4))