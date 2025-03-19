import base64
import json
import requests

headers = {
    'Content-Type': 'application/json'
}

data = {}
data['one'] = 'MISSISSIPPI'
data['two'] = 'MISSISSIPPI'
data['three'] = 'MISSISSIPPI'

r = requests.post(
    'https://tf9tx7jk2b.execute-api.us-east-1.amazonaws.com//logs?verify=<VERIFY>',
    headers = headers,
    data = data
)

print(r.status_code)
print(json.dumps(r.json(), indent=4))

encoded = base64.b64encode(str(data).encode('utf-8')).decode('utf-8')

r = requests.post(
    'https://tf9tx7jk2b.execute-api.us-east-1.amazonaws.com//logs?verify=<VERIFY>',
    headers = headers,
    data = encoded
)

print(r.status_code)
print(json.dumps(r.json(), indent=4))
