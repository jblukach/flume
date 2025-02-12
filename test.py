import requests

headers = {
    'Content-Type': 'application/json'
}

data = {}
data['one'] = 'MISSISSIPPI'
data['two'] = 'MISSISSIPPI'
data['three'] = 'MISSISSIPPI'

r = requests.post(
    'https://u5v9xs6baj.execute-api.us-east-1.amazonaws.com/prod/ingest',
    headers = headers,
    data = data
)

print(r.json())
print(r.status_code)