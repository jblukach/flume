import base64
import boto3
import datetime
import gzip
import json
import os
import uuid

def decoder(data):
    try:
        data = base64.b64decode(data).decode('utf-8')
    except:
        pass
    return data

def handler(event, context):

    print(event)

    try:

        if event['queryStringParameters']['verify'] == os.environ['VERIFY']:

            uniq = str(uuid.uuid4())
            data = decoder(event['body'])

            with gzip.open('/tmp/'+uniq+'.json.gz', 'wb') as g:
                g.write((str(data)+str('\n')).encode())
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