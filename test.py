import requests

headers = {
    'Content-Type': 'application/json'
}

data = {}
data['flume'] = 'log shipment test'

r = requests.post(
    'https://2kntqoktkg.execute-api.us-east-2.amazonaws.com/prod/ingest',
    headers = headers,
    data = data
)

print(r.json())
print(r.status_code)