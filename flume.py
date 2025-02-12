import boto3
import datetime
import gzip
import json
import os
import uuid

def handler(event, context):

    print(event)

    secretmgr = boto3.client('secretsmanager')

    secret = secretmgr.get_secret_value(
        SecretId = os.environ['SECRET']
    )

    verify = json.loads(secret['SecretString'])

    try:

        if event['queryStringParameters']['verify'] == verify['verify']:

            uniq = str(uuid.uuid4())

            with gzip.open('/tmp/'+uniq+'.json.gz', 'wb') as g:
                g.write((str(event)+str('\n')).encode())
            g.close()

            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            hour = datetime.datetime.now().hour

            s3 = boto3.client('s3')

            bucket = os.environ['BUCKET']
            prefix = os.environ['PREFIX']
            key = f'{prefix}/year={year}/month={month}/day={day}/hour={hour}/{uniq}.json.gz'

            s3.upload_file('/tmp/'+uniq+'.json.gz', bucket, key)

            code = 200
            msg = 'Shipped: '+key

        else:

            code = 404
            msg = 'Where the Internet Ends'

    except:
        
        code = 404
        msg = 'Where the Internet Ends'

    return {
        'statusCode': code,
        'body': json.dumps(msg)
    }