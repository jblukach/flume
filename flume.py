import boto3
import datetime
import json
import os
from botocore.vendored import requests

def handler(event, context):

    secretmgr = boto3.client('secretsmanager')

    secret = secretmgr.get_secret_value(
        SecretId = os.environ['SECRET_MGR']
    )

    print(secret['SecretString'])


    now = datetime.datetime.now()
    epoch = datetime.datetime.now(datetime.timezone.utc).timestamp()
    print(epoch)

    print(event)

    payload = {}


    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }