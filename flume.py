import boto3
import datetime
import json
import os
from botocore.vendored import requests

def handler(event, context):

    print(event)
    #print(type(event))

    epoch = datetime.datetime.now(datetime.timezone.utc).timestamp()

    payload = {}
    payload['time'] = epoch                         # @timestamp
    #payload['timezone'] = 'Z'                      # @timezone
    #payload['index'] = 'Connector Name'            #repo
    #payload['sourcetype'] = 'Parser Name'          #type    
    #payload['source'] = 'Log Location'             # @source
    #payload['host'] = 'Origin Host'                # @host
    payload['event'] = event['body']                # @rawstring
    #payload['fields'] = {"#key":"value"}           #tags
    
    #print(payload)
    #print(type(payload))

    secretmgr = boto3.client('secretsmanager')

    secret = secretmgr.get_secret_value(
        SecretId = os.environ['SECRET_MGR']
    )

    hec = json.loads(secret['SecretString'])

    headers = {
        'Authorization': 'Bearer '+hec['token'],
        'Content-Type': 'application/json'
    }

    r = requests.post(
        hec['url'],
        headers = headers,
        data = payload
    )

    print(r.json())
    #print(r.status_code)

    return {
        'statusCode': 200,
        'body': json.dumps('Log Shipped!')
    }