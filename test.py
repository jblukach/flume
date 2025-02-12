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
    'https://jm782ict1g.execute-api.us-east-1.amazonaws.com/prod/ingest?verify=<VERIFY>',
    headers = headers,
    data = data
)

print(r.status_code)
print(json.dumps(r.json(), indent=4))
